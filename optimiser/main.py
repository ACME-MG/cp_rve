"""
 Title:         Optimiser
 Description:   For calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Code
api = API(False, "evpwd 25,44 eta 1e6")
api.read_data(["G44", "G25"]) # ["G32", "G33", "G44", "G25"] # ["G59", "G45", "G50", "G22"]
# api.remove_damage()
api.define_model("evpwd")
api.define_errors(["dy_area", "y_area", "x_end", "y_end"]) # ["dy_area", "x_area", "y_area", "x_end", "y_end"]
api.prepare_objective()
api.prepare_recorder(10, 10)
api.optimise(1000, 400, 400, 0.65, 0.35)
