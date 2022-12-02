"""
 Title:         Results plotter
 Description:   For plotting the results of the optibrated model
 Author:        Janzen Choi

"""

# Libraries
from modules.optimiser import Optimiser

# Parameters
PARAM_STR   = "0.671972514	25.7499735	43.16881374	4.487884698	1669.850786"
PARAM_LIST  = [float(param) for param in PARAM_STR.split("\t")]

# Code
opt = Optimiser(True)
opt.read_data(["G32", "G33", "G44", "G25"]) # ["G32", "G33", "G44", "G25"] # ["G59", "G45", "G50", "G22"]
# opt.remove_damage()
opt.define_model("evp")
opt.plot_results(PARAM_LIST)
# opt.define_errors(["y_area", "dy_area"])
# opt.get_errors(PARAM_LIST)
opt.start()