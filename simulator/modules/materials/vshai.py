"""
 Title:         Voce Slip Hardening Asaro Inelasticity Model
 Description:   For creating the VSHAI material file
 Author:        Janzen Choi

"""

# Libraries
from modules.materials.__material__ import MaterialTemplate

# Fixed parameter values
YOUNGS          = 157000.0
POISSONS        = 0.30
SLIP_DIRECTION  = "1 1 0"
SLIP_PLANE      = "1 1 1"

# Format for defining materials
MATERIAL_FORMAT = """
<materials>
  <{material} type="SingleCrystalModel">
    <kinematics type="StandardKinematicModel">
      <emodel type="IsotropicLinearElasticModel">
        <m1_type>youngs</m1_type>
        <m1>{youngs}</m1>
        <m2_type>poissons</m2_type>
        <m2>{poissons}</m2>
      </emodel>
      <imodel type="AsaroInelasticity">
        <rule type="PowerLawSlipRule">
          <resistance type="VoceSlipHardening">
            <tau_sat>{VSH_tau_sat}</tau_sat>
            <b>{VSH_b}</b>
            <tau_0>{VSH_tau_0}</tau_0>
          </resistance>
          <gamma0>{AI_gamma0}</gamma0>
          <n>{AI_n}</n>
        </rule>
      </imodel>
    </kinematics>
    <lattice type="CubicLattice">
      <a>1.0</a>
      <slip_systems>
        {slip_direction} ; {slip_plane}
      </slip_systems>
    </lattice>
  </{material}>
</materials>
"""

# Voce Slip Hardening Asaro Inelasticity Class
class Material(MaterialTemplate):

    # Creates the file content
    def get_content(self, VSH_tau_sat, VSH_b, VSH_tau_0, AI_gamma0, AI_n):
        return MATERIAL_FORMAT.format(

            # Fixed parameter values
            youngs          = YOUNGS,
            poissons        = POISSONS,
            slip_direction  = SLIP_DIRECTION,
            slip_plane      = SLIP_PLANE,
            material        = self.name,

            # Parameter values to be optimised
            VSH_tau_sat     = VSH_tau_sat,
            VSH_b           = VSH_b,
            VSH_tau_0       = VSH_tau_0,
            AI_gamma0       = AI_gamma0,
            AI_n            = AI_n,
        )