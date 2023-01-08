"""
 Title:         Coincidence Site Lattice
 Description:   For generating euler angles that satisfy CSL criteria
                More information can be found at http://pajarito.materials.cmu.edu/lectures/L14-CSL_Theory_GBE-17Mar16.pdf
 Author:        Janzen Choi

"""

# Libraries
import numpy as np, math, random
from scipy.optimize import minimize

# Returns symmetry matrices
def get_symmetry_matrices(type = "cubic"):
    if type == "cubic":
        return get_cubic_symmetry_matrices()
    elif type == "hexagonal":
        return get_hexagonal_symmetry_matrices()
    elif type == "tetrahedral":
        return get_tetrahedral_symmetry_matrices()

# Returns the cubic symmetry matrices
def get_cubic_symmetry_matrices():
    return [
        [[1,0,0], [0,1,0], [0,0,1]],
        [[0,0,1], [1,0,0], [0,1,0]],
        [[0,1,0], [0,0,1], [1,0,0]],
        [[0,-1,0], [0,0,1], [-1,0,0]],
        [[0,-1,0], [0,0,-1], [1,0,0]],
        [[0,1,0], [0,0,-1], [-1,0,0]],
        [[0,0,-1], [1,0,0], [0,-1,0]],
        [[0,0,-1], [-1,0,0], [0,1,0]],
        [[0,0,1], [-1,0,0], [0,-1,0]],
        [[-1,0,0], [0,1,0], [0,0,-1]],
        [[-1,0,0], [0,-1,0], [0,0,1]],
        [[1,0,0], [0,-1,0], [0,0,-1]],
        [[0,0,-1], [0,-1,0], [-1,0,0]],
        [[0,0,1], [0,-1,0], [1,0,0]],
        [[0,0,1], [0,1,0], [-1,0,0]],
        [[0,0,-1], [0,1,0], [1,0,0]],
        [[-1,0,0], [0,0,-1], [0,-1,0]],
        [[1,0,0], [0,0,-1], [0,1,0]],
        [[1,0,0], [0,0,1], [0,-1,0]],
        [[-1,0,0], [0,0,1], [0,1,0]],
        [[0,-1,0], [-1,0,0], [0,0,-1]],
        [[0,1,0], [-1,0,0], [0,0,1]],
        [[0,1,0], [1,0,0], [0,0,-1]],
        [[0,-1,0], [1,0,0], [0,0,1]],
    ]

# Returns the hexagonal symmetry matrices
def get_hexagonal_symmetry_matrices():
    a = (3 ** 0.5) / 2
    return [
        [[1,0,0], [0,1,0], [0,0,1]],
        [[-0.5,a,0], [-a,-0.5,0], [0,0,1]],
        [[-0.5,-a,0], [a,-0.5,0], [0,0,1]],
        [[0.5,a,0], [-a,0.5,0], [0,0,1]],
        [[-1,0,0], [0,-1,0], [0,0,1]],
        [[0.5,-a,0], [a,0.5,0], [0,0,1]],
        [[-0.5,-a,0], [-a,0.5,0], [0,0,-1]],
        [[1,0,0], [0,-1,0], [0,0,-1]],
        [[-0.5,a,0], [a,0.5,0], [0,0,-1]],
        [[0.5,a,0], [a,-0.5,0], [0,0,-1]],
        [[-1,0,0], [0,1,0], [0,0,-1]],
        [[0.5,-a,0], [-a,-0.5,0], [0,0,-1]],
    ]

# Returns the tetrahedral symmetry matrices
def get_tetrahedral_symmetry_matrices():
    return [
        [[1,0,0], [0,1,0], [0,0,1]],
        [[-1,0,0], [0,1,0], [0,0,-1]],
        [[1,0,0], [0,-1,0], [0,0,-1]],
        [[-1,0,0], [0,-1,0], [0,0,1]],
        [[0,1,0], [-1,0,0], [0,0,1]],
        [[0,-1,0], [1,0,0], [0,0,1]],
        [[0,1,0], [1,0,0], [0,0,-1]],
        [[0,-1,0], [-1,0,0], [0,0,-1]],
    ]

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
    euler_1 = euler_1 if euler_1 != [] else random_euler()
    
    # Specify rotational offset
    euler_offset = deg_to_rad(CSL_DICT[csl_sigma]["euler"])

    # Determine second set of euler angles
    matrix_1 = euler_to_matrix(euler_1)
    matrix_offset = euler_to_matrix(euler_offset)
    matrix_2 = get_matrix_product(matrix_offset, matrix_1)
    euler_2 = matrix_to_euler(matrix_2)

    # Return
    return [euler_1, euler_2]

# Generates a pair of random euler angles based on a misorientation (rads)
def generate_euler_pair(mori, type):
    euler = random_euler()
    pairer = Pairer(euler, mori, type)
    pairing_euler = pairer.get_pairing_euler()
    return [euler, pairing_euler]

# Determines the misorientation of two sets of euler angles (rads)
def get_misorientation_angle(euler_1, euler_2, type):
    return min(get_misorientation_angles(euler_1, euler_2, type))

# Determines the misorientations of two sets of euler angles (rads)
def get_misorientation_angles(euler_1, euler_2, type):
    om_1 = euler_to_matrix(euler_1)
    om_2 = euler_to_matrix(euler_2)
    angle_list = []
    for sym in get_symmetry_matrices(type):
        matrix_1 = get_matrix_product(sym, om_1)
        matrix_2 = get_inverted(matrix_1)
        matrix_3 = get_matrix_product(matrix_2, om_2)
        a_angle = (matrix_3[0][0] + matrix_3[1][1] + matrix_3[2][2] - 1) / 2
        a_angle = max(a_angle, -1)
        angle = math.acos(a_angle)
        angle_list.append(angle)
    return angle_list

# Performs a 3x3 matrix multiplication
def get_matrix_product(matrix_1, matrix_2):
    result = [[0,0,0], [0,0,0], [0,0,0]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += matrix_1[i][k] * matrix_2[k][j]
    return result

# Inverts a matrix
def get_inverted(matrix):
    matrix = np.array(matrix)
    inverted = [list(i) for i in np.linalg.inv(matrix)]
    return inverted

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

# Determines the orientation matrix of a set of euler-bunge angles (rads)
def euler_to_matrix(euler):
    om_11 = math.cos(euler[0])*math.cos(euler[2]) - math.sin(euler[0])*math.sin(euler[2])*math.cos(euler[1])
    om_12 = math.sin(euler[0])*math.cos(euler[2]) + math.cos(euler[0])*math.sin(euler[2])*math.cos(euler[1])
    om_13 = math.sin(euler[2])*math.sin(euler[1])
    om_21 = -math.cos(euler[0])*math.sin(euler[2]) - math.sin(euler[0])*math.cos(euler[2])*math.cos(euler[1])
    om_22 = -math.sin(euler[0])*math.sin(euler[2]) + math.cos(euler[0])*math.cos(euler[2])*math.cos(euler[1])
    om_23 = math.cos(euler[2])*math.sin(euler[1])
    om_31 = math.sin(euler[0])*math.sin(euler[1])
    om_32 = -math.cos(euler[0])*math.sin(euler[1])
    om_33 = math.cos(euler[1])
    om = [[om_11, om_12, om_13],
          [om_21, om_22, om_23],
          [om_31, om_32, om_33]]
    return om

# Determines the possible sets of euler-bunge angles based on an orientation matrix (rads)
def matrix_to_euler(matrix):
    Phi = math.acos(matrix[2][2])
    if Phi == 0:
        phi_1 = math.atan2(-matrix[1][0], matrix[0][0])
        phi_2 = 0
    elif Phi == math.pi:
        phi_1 = math.atan2(matrix[1][0], matrix[0][0])
        phi_2 = 0
    else:
        phi_1 = math.atan2(matrix[2][0], -matrix[2][1])
        phi_2 = math.atan2(matrix[0][2], matrix[1][2])
    phi_1 = phi_1 if phi_1 >= 0 else phi_1 + 2 * math.pi
    phi_2 = phi_2 if phi_2 >= 0 else phi_2 + 2 * math.pi
    return [phi_1, Phi, phi_2]

# Converts radians to degrees
def rad_to_deg(radians):
    if isinstance(radians, list):
        return [rad_to_deg(r) for r in radians]
    return radians * 180 / math.pi

# Converts degrees to radians
def deg_to_rad(degrees):
    if isinstance(degrees, list):
        return [deg_to_rad(d) for d in degrees]
    return degrees * math.pi / 180

# Generates a set of (uniformly) random euler-bunge angles 
# https://github.com/heprom/pymicro/blob/master/pymicro/crystal/microstructure.py
def random_euler():
    phi_1 = random.random() * 360.
    Phi = 180. * math.acos(2 * random.random() - 1) / np.pi
    phi_2 = random.random() * 360.
    return [phi_1, Phi, phi_2]

# Generates a (uniformly) random quaternion
def random_quat():
    u = [random.uniform(0, 1) for _ in range(3)]
    x = math.sqrt(1 - u[0]) * math.sin(2 * math.pi * u[1])
    y = math.sqrt(1 - u[0]) * math.cos(2 * math.pi * u[1])
    z = math.sqrt(u[0]) * math.sin(2 * math.pi * u[2])
    w = math.sqrt(u[0]) * math.cos(2 * math.pi * u[2])
    return [x, y, z, w]

# Converts a set of euler-bunge angles into a quaternion (rads)
def euler_to_quat(phi_1, Phi, phi_2):
    cy = math.cos(phi_2 * 0.5)
    sy = math.sin(phi_2 * 0.5)
    cp = math.cos(Phi * 0.5)
    sp = math.sin(Phi * 0.5)
    cr = math.cos(phi_1 * 0.5)
    sr = math.sin(phi_1 * 0.5)
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy
    w = cr * cp * cy + sr * sp * sy
    return [x, y, z, w]

# Converts a quaternion into a set of euler-bunge angles (rads)
def quat_to_euler(x, y, z, w):
    phi_1 = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    Phi   = math.asin(max([min([2 * (w * y - z * x), 1]), -1]))
    phi_2 = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
    return [phi_1, Phi, phi_2]
