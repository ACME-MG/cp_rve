"""
 Title:         Sampler
 Description:   For generating custom sample shapes
 Author:        Janzen Choi

"""

# Libraies
import subprocess

# Define sample and gap shapes
sample_length = 20000
sample_height = 5000
sample_width  = 1000
indent_length = 500
indent_height = 1500

sharp_length = 2000
sharp_height = 1500

# Define shapes
ecylinder_str = "ecylinder({ctr_x},0,{ctr_z},0,1,0,1,0,0,0,0,1,{rad_1},{rad_2})"
cut_shapes = [
    ecylinder_str.format(
        ctr_x = sample_length / 2,
        ctr_z = sample_height,
        rad_1 = indent_length / 2,
        rad_2 = indent_height),
    ecylinder_str.format(
        ctr_x = sample_length / 2,
        ctr_z = 0,
        rad_1 = indent_length / 2,
        rad_2 = indent_height),
    # ecylinder_str.format(
    #     ctr_x = sample_length / 2,
    #     ctr_z = sample_height,
    #     rad_1 = sharp_length / 2,
    #     rad_2 = sharp_height),
    # ecylinder_str.format(
    #     ctr_x = sample_length / 2,
    #     ctr_z = 0,
    #     rad_1 = sharp_length / 2,
    #     rad_2 = sharp_height),
]

# Create command
dimensions = "-dim 3"
domain = "-domain \"cube({},{},{})\"".format(sample_length, sample_width, sample_height)
transform = "-transform \"cut({})\"".format(",".join(cut_shapes))
regularisation = "-reg 1"

# Execute command
command = "neper -T -n 200 -morpho gg {} {} {} {} -o temp".format(dimensions, domain, transform, regularisation)
subprocess.run(["OMP_NUM_THREADS=1 " + command], shell = True, check = True)