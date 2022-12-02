"""
 Title:         Optimiser
 Description:   For calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
from modules.optimiser import Optimiser

# Code
opt = Optimiser("evpwd 25,44", fancy=True)
opt.read_data(["G44", "G25"]) # ["G32", "G33", "G44", "G25"] # ["G59", "G45", "G50", "G22"]
# opt.remove_damage()
opt.define_model("evpwd")
opt.define_errors(["dy_area", "y_area", "x_end", "y_end"]) # ["dy_area", "x_area", "y_area", "x_end", "y_end"]
opt.prepare_objective()
opt.prepare_recorder(10, 10)
opt.optimise(1000, 400, 400, 0.65, 0.35)
opt.start()
