from modules.api import API
api = API("test", 0)
api.define_mesh("mesh.e", "input_orientations.csv")
api.define_params()
api.simulate("~/moose/deer/deer-opt", 24)
