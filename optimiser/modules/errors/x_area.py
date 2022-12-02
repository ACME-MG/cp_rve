"""
 Title:         The x_area objective function
 Description:   The objective function for calculating the horizontal areas between two curves
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import modules.errors._error as error

# Constants
POLY_DEG_ODD    = 15
POLY_DEG_EVEN   = POLY_DEG_ODD + 1
NUM_POINTS      = 50

# The XArea class
class XArea(error.Error):

    # Constructor
    def __init__(self, exp_curves):
        super().__init__("x_area", exp_curves)
        poly_deg_list       = [POLY_DEG_EVEN if exp_curve["type"] == "creep" else POLY_DEG_ODD for exp_curve in exp_curves]
        self.exp_poly_list  = [list(np.polyfit(exp_curves[i]["y"], exp_curves[i]["x"], poly_deg_list[i])) for i in range(len(exp_curves))]
        self.exp_y_end_list = [exp_curve["y"][-1] for exp_curve in exp_curves]
        self.avg_x_list     = [np.average(exp_curve["x"]) for exp_curve in exp_curves]

    # Computing the error
    def get_value(self, prd_curves):
        value_list = []
        for i in range(len(prd_curves)):
            thin_indexes = error.get_thin_indexes(len(prd_curves[i]["x"]), NUM_POINTS)
            prd_x_list = [prd_curves[i]["x"][j] for j in thin_indexes]
            prd_y_list = [prd_curves[i]["y"][j] for j in thin_indexes]
            exp_x_list = list(np.polyval(self.exp_poly_list[i], prd_y_list))
            area = [abs(prd_x_list[j] - exp_x_list[j]) for j in range(NUM_POINTS) if prd_y_list[j] <= self.exp_y_end_list[i]]
            value_list.append(np.average(area) / self.avg_x_list[i])
        return np.average(value_list)