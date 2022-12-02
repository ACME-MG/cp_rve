"""
 Title:         The dy_area objective function
 Description:   The objective function for calculating the vertical areas between the derivatives of two curves
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import modules.errors._error as error

# Constants
POLY_DEG_ODD    = 15
POLY_DEG_EVEN   = POLY_DEG_ODD + 1
NUM_POINTS      = 50

# The DyArea class
class DyArea(error.Error):

    # Constructor
    def __init__(self, exp_curves):
        super().__init__("dy_area", exp_curves)
        poly_deg_list           = [POLY_DEG_ODD if exp_curve["type"] == "creep" else POLY_DEG_EVEN for exp_curve in exp_curves]
        self.exp_polyder_list   = [list(np.polyder(np.polyfit(exp_curves[i]["x"], exp_curves[i]["y"], poly_deg_list[i]))) for i in range(len(exp_curves))]
        self.exp_x_end_list     = [exp_curve["x"][-1] for exp_curve in exp_curves]
        self.avg_dy_list        = [np.average(np.polyval(self.exp_polyder_list[i], exp_curves[i]["x"])) for i in range(len(exp_curves))]

    # Computes the error value
    def get_value(self, prd_curves):
        value_list = []
        for i in range(len(prd_curves)):
            thin_indexes = error.get_thin_indexes(len(prd_curves[i]["x"]), NUM_POINTS)
            prd_x_list = [prd_curves[i]["x"][j] for j in thin_indexes]
            prd_y_list = [prd_curves[i]["y"][j] for j in thin_indexes]
            prd_dy_list = error.get_fd(prd_x_list, prd_y_list)
            exp_dy_list = list(np.polyval(self.exp_polyder_list[i], prd_x_list))
            area = [abs(prd_dy_list[j] - exp_dy_list[j]) for j in range(NUM_POINTS-1) if prd_x_list[j] <= self.exp_x_end_list[i]]
            value_list.append(np.average(area) / self.avg_dy_list[i])
        return np.average(value_list)