"""
 Title:         Crystallographic Misorienter
 Description:   Contains misorientation related functions
 Author:        Janzen Choi

"""

# Libraries
import numpy as np, math
from modules.helper.general import *
import modules.orientation.angle as angle
import modules.orientation.euler_converter as euler_converter
import modules.orientation.symmetry as symmetry
from scipy.optimize import minimize

# Generates a pair of random euler angles based on a misorientation (rads)
def generate_euler_pair(mori, type):
    euler = angle.random_euler()
    pairer = Pairer(euler, mori, type)
    pairing_euler = pairer.get_pairing_euler()
    return [euler, pairing_euler]

# Determines the misorientation of two sets of euler angles (rads)
def get_misorientation_angle(euler_1, euler_2, type):
    return min(get_misorientation_angles(euler_1, euler_2, type))

# Determines the misorientations of two sets of euler angles (rads)
def get_misorientation_angles(euler_1, euler_2, type):
    om_1 = euler_converter.euler_to_matrix(euler_1)
    om_2 = euler_converter.euler_to_matrix(euler_2)
    angle_list = []
    for sym in symmetry.get_symmetry_matrices(type):
        matrix_1 = get_matrix_product(sym, om_1)
        matrix_2 = get_inverted(matrix_1)
        matrix_3 = get_matrix_product(matrix_2, om_2)
        a_angle = (matrix_3[0][0] + matrix_3[1][1] + matrix_3[2][2] - 1) / 2
        a_angle = max(a_angle, -1)
        angle = math.acos(a_angle)
        angle_list.append(angle)
    return angle_list

# The Pairer Class
class Pairer:

    # Constructor
    def __init__(self, euler, mori, type):
        self.euler = euler
        self.mori = mori
        self.type = type

    # Determines a pairing set of euler angles from a misorientation angle (rads)
    def get_pairing_euler(self):
        x0 = np.array([1, 1, 1])
        res = minimize(self.pairing_euler_obj, x0, method="nelder-mead", options={"disp": False})
        return list(res.x)

    # Objective function for determining a pairing set of euler angles (rads)
    def pairing_euler_obj(self, euler):
        mori = get_misorientation_angle(self.euler, euler, self.type)
        return (self.mori - mori) ** 2