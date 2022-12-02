"""
 Title:         Main
 Description:   For simulating creep behaviour
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Parameters
DEER_PATH           = "~/moose/deer/deer-opt"
NUM_PROCESSORS      = 4
MESH_FILE           = "sculpt.e"
ORIENTATION_FILE    = "stats.csv"
VERBOSE_DISPLAY     = True

# Code
api = API(DEER_PATH, NUM_PROCESSORS, MESH_FILE, ORIENTATION_FILE, VERBOSE_DISPLAY)
api.define_material()
api.define_simulation()
api.commence()
