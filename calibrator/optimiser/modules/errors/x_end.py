"""
 Title:         The x_end objective function
 Description:   The objective function for calculating the horizontal distance in which two curves end
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import modules.errors._error as error

# The XEnd class
class XEnd(error.Error):

    # Constructor
    def __init__(self, exp_curves):
        super().__init__("x_end", exp_curves)
        self.exp_x_end_list = [exp_curve["x"][-1] for exp_curve in exp_curves]
        self.multiplier_list = [1 if exp_curve["type"] == "creep" else 0 for exp_curve in exp_curves]
    
    # Computing the error
    def get_value(self, prd_curves):
        prd_x_end_list = [prd_curves[i]["x"][-1] for i in range(len(prd_curves))]
        value_list = [abs(prd_x_end_list[i] - self.exp_x_end_list[i]) / self.exp_x_end_list[i] for i in range(len(self.exp_x_end_list))]
        value_list = [value_list[i] * self.multiplier_list[i] for i in range(len(value_list))]
        return np.average(value_list)