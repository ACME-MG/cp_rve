"""
 Title:         Simplifier
 Description:   For simplifying creep curves into several points 
 Author:        Janzen Choi

"""

# Libraries
import numpy as np

# Simplifier Class
class Simplifier:

    # Constructor
    def __init__(self, restore_size=100):
        self.restore_size   = restore_size
        self.l_bounds       = [0, 0]
        self.u_bounds       = [10000, 1]

    # Converts a creep curve into representational points
    def simplify_curve(self, curve):

        # Get rupture time and strain
        x_list, y_list = curve["x"], curve["y"]
        x_end = x_list[-1]
        y_end = y_list[-1]

        # Return
        return [x_end, y_end]

    # Converts representational points into a creep curve
    def restore_curve(self, points):

        return {"x": [points[0]], "y": [points[1]]}
