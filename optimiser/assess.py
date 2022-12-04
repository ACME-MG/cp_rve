"""
 Title:         Results plotter
 Description:   For plotting the results of the optibrated model
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Parameters
PARAM_STR   = "0.671972514	25.7499735	43.16881374	4.487884698	1669.850786"
PARAM_LIST  = [float(param) for param in PARAM_STR.split("\t")]

# Code
api = API(True)
api.read_data(["G32", "G33", "G44", "G25"]) # ["G32", "G33", "G44", "G25"] # ["G59", "G45", "G50", "G22"]
# api.remove_damage()
api.define_model("evpwd")
api.plot_results(PARAM_LIST)
# api.define_errors(["y_area", "dy_area"])
# api.get_errors(PARAM_LIST)