"""
 Title:         Main
 Description:   For simulating creep behaviour
 Author:        Janzen Choi

"""

# Libraries
from modules.simulator import Simulator

# Parameters
DEER_PATH           = "~/moose/deer/deer-opt"
NUM_PROCESSORS      = 4
MESH_FILE           = "sculpt.e"
ORIENTATION_FILE    = "stats.csv"
VERBOSE_DISPLAY     = True

# Code
sim = Simulator(DEER_PATH, NUM_PROCESSORS, MESH_FILE, ORIENTATION_FILE, VERBOSE_DISPLAY)
sim.define_material()
sim.define_simulation()
sim.commence()
