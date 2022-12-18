"""
 Title:         Shaper
 Description:   For creating non-large geometries for samples 
 Author:        Janzen Choi

"""

# Library
from modules.api import API

api = API(fancy=True, verbose=True)
api.read_pixels("617b_ebsd.csv", 5.2)
# api.decrease_resolution(4)
api.clean_pixels(10)
api.smoothen_edges(5)
api.visualise()

x_shift = 850
y_shift = 100
api.redefine_domain(x_shift, 2200+x_shift, y_shift, 1700+y_shift) # 2200 x 1700
# api.cut_mask("617b_notch.png")
# api.cut_rectangle(1050, 1150, 0, 560)
# api.cut_circle(1100, 560, 50)
api.visualise()

api.rotate_CW_90()
api.rotate_CW_90()
# api.mesh("~/cubit/psculpt.exe", 19*5.2)
api.export_euler_bunge()
