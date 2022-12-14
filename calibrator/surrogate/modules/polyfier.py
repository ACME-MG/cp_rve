"""
 Title:         Surrogate Model
 Description:   For creating the surrogate model
 Author:        Janzen Choi
 
"""

# Libraries
import numpy as np
import warnings

# Constants
POLY_ODD_DEGREE     = 15
POLY_EVEN_DEGREE    = 16
INVALID_VALUE       = 0
DEFAULT_STEP_SIZE   = 10
DEFAULT_MAX_X_VALUE = 10000

# Polyfier class
class Polyfier:

    # Constructor
    def __init__(self, step=DEFAULT_STEP_SIZE, max=DEFAULT_MAX_X_VALUE):
        self.step = step
        self.max = max

    # Converts a curve into a polynomial
    def curve_to_poly(self, curve):
        x_end = curve["x"][-1]
        with warnings.catch_warnings(record=True) as w:
            try:
                polynomial = np.polyfit(curve["x"], curve["y"], POLY_ODD_DEGREE)
            except RuntimeWarning:
                polynomial = np.polyfit(curve["x"], curve["y"], POLY_EVEN_DEGREE)
        return { "x_end": x_end, "poly": polynomial }

    # Returns an x_list
    def get_x_list(self):
        x_list = [x for x in range(0, self.max, self.step)]
        return x_list

    # Converts a polynomial to a curve
    def poly_to_curve(self, poly):
        x_list, y_list = [], []
        for x in range(0, self.max, self.step):
            y = np.polyval(poly["poly"], [x]) if x < poly["x_end"] else [INVALID_VALUE]
            x_list.append(x)
            y_list.append(y[0])
        return { "x": x_list, "y": y_list }

    # Compresses a curve
    def compress_curve(self, curve):

        # If the curve is empty, then give zeros
        if curve["x"] == [] or curve["y"] == [] or np.nan in curve["y"]:
            x_list = self.get_x_list()
            return {
                "x": x_list,
                "y": [INVALID_VALUE] * len(x_list)
            }

        # Otherwise, compress
        poly = self.curve_to_poly(curve)
        curve = self.poly_to_curve(poly)
        return curve