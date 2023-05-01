from modules.api import API
folder = "700_16_s1"
api = API(f"{folder}", 0)
api.define_mesh(f"{folder}/mesh.e", f"{folder}/input_orientations.csv")
api.define_params()
api.simulate("~/moose/deer/deer-opt", 8)
