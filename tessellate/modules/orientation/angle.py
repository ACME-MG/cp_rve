"""
 Title:         Angle related operations
 Description:   Dealing with angle related operations (in the Euler-bunge notation where relevant)
 Author:        Janzen Choi

"""

# Libraries
import math, random

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
def random_euler():
    quat = random_quat()
    euler = quat_to_euler(*quat) 
    return euler

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

