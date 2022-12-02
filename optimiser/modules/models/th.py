"""
 Title:         Time Hardening model
 Description:   Predicts primary creep
 Author:        Janzen Choi

"""

# Libraries
import math
import modules.models._model as model

# Constants
TIME_STEP = 5
UNEXPECTED_BIG_NUMBER = 10000

# The Time Hardening Class
class TH(model.Model):

    # Constructor
    def __init__(self, exp_curves):
        
        # Defines the model
        super().__init__(
            name = "th",
            param_info = [
                {"name": "th_a",    "min": 1e-50,   "max": 1e0},
                {"name": "th_n",    "min": 1e-50,   "max": 1e2},
                {"name": "th_m",    "min": -1e0,    "max": -1e-50},
            ],
            exp_curves = exp_curves
        )

        # Define time limit
        self.time_limit_list = [exp_curve["x"][-1] for exp_curve in exp_curves]

    # Gets the predicted curves
    def get_prd_curves(self, th_a, th_n, th_m):
        prd_curves = super().get_prd_curves()

        # Get each predicted curve
        for i in range(len(prd_curves)):
            stress = self.exp_curves[i]["stress"]

            # Calculate predicted curve at each stress
            for time in range(0, round(self.time_limit_list[i]), TIME_STEP):
                th_strain = th_a*stress**th_n/(th_m+1)*time**(th_m+1)
                if math.isnan(th_strain) or abs(th_strain) > UNEXPECTED_BIG_NUMBER:
                    break
                prd_curves[i]["x"].append(time)
                prd_curves[i]["y"].append(th_strain)

        # Return predicted curves
        return prd_curves