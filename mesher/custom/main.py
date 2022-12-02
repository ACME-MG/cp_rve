"""
 Title:         Shaper
 Description:   For creating non-large geometries for samples 
 Author:        Janzen Choi

"""

# Library
from modules.api import API

api = API(fancy=True)
api.read_pixels("data.csv", 0.15)
api.rotate_CW_90()

api.redefine_domain(2, 43, 2.5, 30)
api.clean_pixels(5)
api.smoothen_edges(3)
api.pad_edges(20)
api.visualise()

api.increase_resolution(4)
api.decrease_resolution(2)
api.redefine_domain(0, 41, 0, 25) # (41 x 25)
api.visualise()

api.cut_rectangle(10, 31, 0, 7.75)
api.cut_rectangle(10, 31, 17.25, 25)
api.cut_rectangle(13, 28, 6.75, 9.75)
api.cut_rectangle(13, 28, 15.25, 18.25)
api.cut_circle(13, 6.75, 3)
api.cut_circle(28, 6.75, 3)
api.cut_circle(13, 18.25, 3)
api.cut_circle(28, 18.25, 3)
api.clean_pixels(1)
api.visualise()

# api.mesh("~/cubit/psculpt.exe", 10)
# api.export(["q1", "q2", "q3", "q4"], include_header=False)