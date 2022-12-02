"""
 Title:         Generator
 Description:   Useful calculation-based functions for aiding in the tessellation process
 Author:        Janzen Choi

"""

# Libraries
import modules.orientation.angle as angle
import modules.orientation.csl as csl

# Constants
MAX_EXPECTED_TWINS = 5

# Generates and returns lamellae widths as a string
def generate_lamellae_widths(diameter_list, distribution, shape_length):
    width_str = ""
    max_parent_diameter = max(diameter_list)
    for i in range(len(diameter_list)):
        num_twins = round(MAX_EXPECTED_TWINS * diameter_list[i] / max_parent_diameter)
        if num_twins == 0 or i == 0:
            width_str += f"{i + 1} {shape_length}\n"
        else:
            twin_widths = distribution.get_vals(num_twins)
            twin_gaps = distribution.get_norm_vals(num_twins, diameter_list[i] - sum(twin_widths))
            lamellae = [[twin_widths[i]] + [twin_gaps[i]] for i in range(num_twins)]
            lamellae = [value for sublist in lamellae for value in sublist] + [shape_length]
            width_str += f"{i + 1} {':'.join([str(l) for l in lamellae])}\n"
    return width_str

# Generates the crystallographic orientation randomly
def generate_random_orientations(num_grains, has_twins):
    ori_str_list = []
    for _ in range(num_grains):
        parent_ori = angle.rad_to_deg(angle.random_euler())
        parent_ori = " ".join(str(ori) for ori in parent_ori)
        twin_ori = angle.rad_to_deg(angle.random_euler())
        twin_ori = " ".join(str(ori) for ori in twin_ori)
        ori_str = (parent_ori + "\n" + twin_ori + "\n") * MAX_EXPECTED_TWINS if has_twins else parent_ori
        ori_str_list.append(ori_str)
    return ori_str_list

# Generates the crystallographic orientates based on CSL (coincidence site lattice)
def generate_csl_orientations(num_grains, csl_sigma):
    ori_str_list = []
    for _ in range(num_grains):
        euler_pair = csl.get_csl_euler_angles(csl_sigma)
        euler_pair = angle.rad_to_deg(euler_pair)
        parent_ori = " ".join(str(ori) for ori in euler_pair[0])
        twin_ori   = " ".join(str(ori) for ori in euler_pair[1])
        ori_str = (parent_ori + "\n" + twin_ori + "\n") * MAX_EXPECTED_TWINS
        ori_str_list.append(ori_str)
    return ori_str_list