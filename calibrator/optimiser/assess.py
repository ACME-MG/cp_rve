"""
 Title:         Results plotter
 Description:   For plotting the results of the optibrated model
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Parameters
PARAM_STR   = "16.69852911	36.87999523	59.36330643	1.603296796	630113.2177	47.1806713	2.804294642"
PARAM_LIST  = [float(param) for param in PARAM_STR.split("\t")]

# Code
api = API(True)
api.read_data(["G32", "G33", "G44", "G25"]) # ["G32", "G33", "G44", "G25"] # ["G59", "G45", "G50", "G22"]
# api.remove_damage()
api.define_model("evpwd")
api.plot_results(PARAM_LIST)
# api.define_errors(["y_area", "dy_area"])
# api.get_errors(PARAM_LIST)