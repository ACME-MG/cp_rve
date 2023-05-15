from modules.api import API
folder = "500/16_s1"
api = API(f"{folder}", 0)
api.define_mesh(f"{folder}/mesh.e", f"{folder}/input_orientations.csv")
api.define_params(simulation_params=[])
api.define_material("")
api.define_simulation("no_czm")
api.simulate("~/moose/deer/deer-opt", 8)
