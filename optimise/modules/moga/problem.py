"""
 Title:         Problem
 Description:   For defining the MOGA problem
 Author:        Janzen Choi

"""

# Libraries
import warnings
import numpy as np
from pymoo.core.problem import ElementwiseProblem

# The Problem class
class Problem(ElementwiseProblem):

    # Constructor
    def __init__(self, objective, recorder):
        
        # Initialise
        self.objective  = objective
        self.model      = objective.get_model()
        self.recorder   = recorder

        # Define the element wise problem
        super().__init__(
            n_var    = len(self.model.get_param_info()),
            n_obj    = len(self.objective.get_error_names()),
            n_constr = 0,
            xl       = np.array(self.model.get_param_lower_bounds()),
            xu       = np.array(self.model.get_param_upper_bounds())
        )
    
    # Minimises expression "F" such that the expression "G <= 0" is satisfied
    def _evaluate(self, params, out, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore") # ignore warnings
            prd_curves = self.model.get_prd_curves(*params)
            error_values = self.objective.get_error_values(prd_curves)
            self.recorder.update_results(params, error_values)
            out["F"] = error_values