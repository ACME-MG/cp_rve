"""
 Title:         Horizontal Sample
 Description:   For creating a horizontally symmetrical sample
 Author:        Janzen Choi

"""

# Library
from modules.api import API

api = API(fancy=True)
api.read_pixels("p91_ebsd.csv", 0.15)
api.rotate_CW_90()
api.visualise()

api.redefine_domain(4, 45, 1.5, 29)
api.clean_pixels(5)
api.smoothen_edges(3)
api.pad_edges(50)
api.visualise()

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
api.visualise()

api.mesh("~/cubit/psculpt.exe", 1) # post-processting, scale by 10 # volume all scale x 10
# api.export(["q1", "q2", "q3", "q4"], include_header=False)
