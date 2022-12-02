"""
 Title:         Main
 Description:   Wrapper for Neper for creating RVEs
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Constants
EQ_RADIUS   = [2.94032, 0.99847, 2.60941, 302.370]
SPHERICITY  = [-1.6229, 0.40402, 0.02316, 0.57725]
TWIN_WIDTH  = [1.46831, 0.79859, 1.21113, 284.433]

# Code
api = API()
# api.load_parents("results/rve500.tess")
api.define_domain(120, 3)
api.add_parents(EQ_RADIUS, SPHERICITY)
api.visualise()
# api.add_twins(TWIN_WIDTH)
api.orient_random()
api.get_stats(["orientation"], False)
api.export_file("stl:bycell")
# api.orient_csl("3")
api.commence(False)