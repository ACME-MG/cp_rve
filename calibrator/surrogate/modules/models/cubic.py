"""
 Title:         Cubic Model
 Description:   Simple cubic model for testing the surrogate model
 Author:        Janzen Choi

"""

# Libraries
from modules.models.__model__ import Model

# Constants
STEP_SIZE   = 1
MAX_X       = 20

# Cubic Model
class Cubic(Model):

    # Constructor
    def __init__(self):
        super().__init__(
            name = "cubic",
            param_info = [
                {"name": "a_0",  "min": -1.0e1, "max": 1.0e1},
                {"name": "a_1",  "min": -1.0e1, "max": 1.0e1},
                {"name": "a_2",  "min": -1.0e1, "max": 1.0e1},
                {"name": "a_3",  "min": -1.0e1, "max": 1.0e1},
            ]
        )
    
    # Gets the curve
    def get_curve(self, a_0, a_1, a_2, a_3):
        x_list = range(0, MAX_X, STEP_SIZE)
        y_list = [a_0 + a_1*x + a_2*x**2 + a_3*x**3 for x in x_list]
        return {
            "x": x_list,
            "y": y_list,
        }