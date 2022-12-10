"""
 Title:         Shaper
 Description:   For creating non-large geometries for samples 
 Author:        Janzen Choi

"""

# Library
from modules.api import API

api = API(fancy=True)
api.read_pixels("ebsd.csv", 0.15)
api.rotate_CW_90()
api.rotate_CW_90()
api.visualise()

api.redefine_domain(1.5, 29, 0, 47)
api.clean_pixels(5)
api.smoothen_edges(3)
api.pad_edges(20)
api.visualise()

# api.decrease_resolution(2)
api.redefine_domain(0, 25, 4, 45) # (25 x 41)
api.visualise()

api.cut_rectangle(0, 7.75, 10, 31)
api.cut_rectangle(17.25, 25, 10, 31)
api.cut_rectangle(6.75, 9.75, 13, 28)
api.cut_rectangle(15.25, 18.25, 13, 28)
api.cut_circle(6.75, 13, 3)
api.cut_circle(6.75, 28, 3)
api.cut_circle(18.25, 13, 3)
api.cut_circle(18.25, 28, 3)
api.visualise()

# api.mesh("~/cubit/psculpt.exe", 1) # post-processting, scale by 10
# api.export(["q1", "q2", "q3", "q4"], include_header=False)
