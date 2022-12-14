"""
 Title:         Continuity
 Description:   Plots the continuity of a model
 Author:        Janzen Choi
 
"""

# Libraries
import random
import matplotlib.pyplot as plt
from modules.models.__model_factory__ import get_model
from modules.sampler import Sampler

# Get model information
model = get_model("evpwd_s")
l_bounds = model.get_param_lower_bounds()
u_bounds = model.get_param_upper_bounds()

# Get parameters
sampler = Sampler(l_bounds, u_bounds)
params = sampler.sample_centre()[0] # absolute centre

# Define changing parameter indices
PARAM_1 = 0
PARAM_2 = 1

# Continuously query the parameter space
count = 0
while True:

    # Only alter two parameters
    params[PARAM_1] = random.uniform(l_bounds[PARAM_1], u_bounds[PARAM_1])
    params[PARAM_2] = random.uniform(l_bounds[PARAM_2], u_bounds[PARAM_2])

    # Get curve
    curve = model.get_curve(*params)
    if len(curve["x"]) == 0 or len(curve["y"]) == 0:
        plt.scatter(params[PARAM_1], params[PARAM_2], marker='o', color="r", linewidth=1)
    else:
        plt.scatter(params[PARAM_1], params[PARAM_2], marker='o', color="b", linewidth=1)

    # Save
    print(f"Conducting {count + 1}th evaluation")
    plt.savefig("continuity.png")
    count += 1
