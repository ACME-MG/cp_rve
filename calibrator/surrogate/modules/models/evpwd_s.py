"""
 Title:         The Elastic Visco Plastic Work Damage Model (Separated)
 Description:   Predicts primary, secondary, and tertiary creep
 Author:        Janzen Choi

"""

# Libraries
import modules.models.__model__ as model
import sys; sys.path.append("/home/janzen/moose/neml")
from neml import models, elasticity, drivers, surfaces, hardening, visco_flow, general_flow, damage
from neml.nlsolvers import MaximumIterations

# Model Parameters
YOUNGS       = 157000.0
POISSONS     = 0.3
S_RATE       = 1.0e-4
E_RATE       = 1.0e-4
HOLD         = 11500.0 * 3600.0
NUM_STEPS    = 501
MIN_DATA     = 50

# The Elastic Visco Plastic Work Damage (Separated) Class
class EVPWD_S(model.Model):

    # Constructor
    def __init__(self):
        
        # Defines the model
        super().__init__(
            name = "evpwd_s",
            param_info = [
                {"name": "wd_wc",   "min": 2.0e1,   "max": 1.0e2},
                {"name": "wd_n",    "min": 2.0e0,   "max": 1.0e1},
            ],
        )

        # Fix plastic parameters
        evp_s0 = 0.671972514
        evp_R  = 25.74997349
        evp_d  = 43.16881374
        evp_n  = 4.487884698
        evp_eta = 1669.850786

        # Initialise
        self.elastic_model  = elasticity.IsotropicLinearElasticModel(YOUNGS, "youngs", POISSONS, "poissons")
        self.yield_surface  = surfaces.IsoJ2()
        iso_hardening   = hardening.VoceIsotropicHardeningRule(evp_s0, evp_R, evp_d)
        g_power         = visco_flow.GPowerLaw(evp_n, evp_eta)
        visco_model     = visco_flow.PerzynaFlowRule(self.yield_surface, iso_hardening, g_power)
        integrator      = general_flow.TVPFlowRule(self.elastic_model, visco_model)
        self.evp_model       = models.GeneralIntegrator(self.elastic_model, integrator, verbose=False)
    
    # Gets the predicted curve
    def get_curve(self, wd_wc, wd_n):

        # Define model
        wd_model        = damage.WorkDamage(self.elastic_model, wd_wc, wd_n)
        evpwd_model     = damage.NEMLScalarDamagedModel_sd(self.elastic_model, self.evp_model, wd_model, verbose=False)

        # Define stress and temperature
        stress = 80
        temp = 800

        # Get predictions
        try:
            creep_results = drivers.creep(evpwd_model, stress, S_RATE, HOLD, T=temp, verbose=False, check_dmg=False, dtol=0.95, nsteps_up=150, nsteps=NUM_STEPS, logspace=False)
            return {
                "x": list(creep_results['rtime'] / 3600),
                "y": list(creep_results['rstrain'] / 3600),
            }
        except MaximumIterations:
            return {"x": [], "y": []}
