"""
 Title:         Crystrallographic Orienter
 Description:   For generating crystallographic orientation
 Author:        Janzen Choi

"""

# Libraries
import math

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
