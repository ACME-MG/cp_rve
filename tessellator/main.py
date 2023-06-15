from modules.api import API
api = API("", 2)
api.define_domain(300, 3)
api.define_radius(2.94032, 0.99847, 2.60941, 302.370)
api.define_sphericity(-1.6229, 0.40402, 0.02316, 0.57725)
api.tessellate()
# api.load_tessellation("rve_1000.tess")
# api.visualise()
# api.orient_random()
# api.export(["x", "y", "z", "phi_1", "Phi", "phi_2"])
