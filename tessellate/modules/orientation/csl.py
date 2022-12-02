"""
 Title:         Coincidence Site Lattice
 Description:   For generating euler angles that satisfy CSL criteria
                More information can be found at http://pajarito.materials.cmu.edu/lectures/L14-CSL_Theory_GBE-17Mar16.pdf
 Author:        Janzen Choi

"""

# Libraries
from modules.helper.general import *
import modules.orientation.angle as angle
import modules.orientation.euler_converter as euler_converter

# Constants
CSL_DICT = {
    "3":    {"mori": 60.00, "euler": [45, 70.53, 45]},
    "5":    {"mori": 36.86, "euler": [0, 90, 36.86]},
    "7":    {"mori": 38.21, "euler": [26.56, 73.4, 63.44]},
    "9":    {"mori": 38.94, "euler": [26.56, 83.62, 26.56]},
    "11":   {"mori": 50.47, "euler": [33.68, 79.53, 33.68]},
    "13a":  {"mori": 22.62, "euler": [0, 90, 22.62]},
    "13b":  {"mori": 27.79, "euler": [18.43, 76.66, 71.57]},
    "15":   {"mori": 48.19, "euler": [19.65, 82.33, 42.27]},
    "17a":  {"mori": 28.07, "euler": [0, 90, 28.07]},
    "17b":  {"mori": 61.90, "euler": [45, 86.63, 45]},
    "19a":  {"mori": 26.53, "euler": [18.44, 89.68, 18.44]},
    "19b":  {"mori": 46.80, "euler": [33.69, 71.59, 56.31]},
    "21a":  {"mori": 21.78, "euler": [14.03, 79.02, 75.97]},
    "21b":  {"mori": 44.41, "euler": [22.83, 79.02, 50.91]},
    "23":   {"mori": 40.45, "euler": [15.25, 82.51, 52.13]},
    "25a":  {"mori": 16.26, "euler": [0, 90, 16.26]},
    "25b":  {"mori": 51.68, "euler": [36.87, 90, 53.13]},
    "27a":  {"mori": 31.59, "euler": [21.8, 85.75, 21.8]},
    "27b":  {"mori": 35.43, "euler": [15.07, 85.75, 31.33]},
    "29a":  {"mori": 43.60, "euler": [0, 90, 43.6]},
    "29b":  {"mori": 46.40, "euler": [33.69, 84.06, 56.31]},
    "31a":  {"mori": 17.90, "euler": [11.31, 80.72, 78.69]},
    "31b":  {"mori": 52.20, "euler": [27.41, 78.84, 43.66]},
    # "33a":  {"mori": 20.10, "euler": [12.34, 83.04, 58.73]}, # issue
    # "33b":  {"mori": 33.60, "euler": [37.51, 76.84, 37.51]}, # issue
    "33c":  {"mori": 59.00, "euler": [38.66, 75.97, 38.66]},
    "35a":  {"mori": 34.00, "euler": [16.86, 80.13, 60.46]},
    "35b":  {"mori": 43.20, "euler": [30.96, 88.36, 59.04]},
}

# For generating two sets of euler angles that conform to CSL3
def get_csl_euler_angles(csl_sigma, euler_1 = []):

    # Generate a set of random euler angles if none specified
    euler_1 = euler_1 if euler_1 != [] else angle.random_euler()
    
    # Specify rotational offset
    euler_offset = angle.deg_to_rad(CSL_DICT[csl_sigma]["euler"])

    # Determine second set of euler angles
    matrix_1 = euler_converter.euler_to_matrix(euler_1)
    matrix_offset = euler_converter.euler_to_matrix(euler_offset)
    matrix_2 = get_matrix_product(matrix_offset, matrix_1)
    euler_2 = euler_converter.matrix_to_euler(matrix_2)

    # Return
    return [euler_1, euler_2]