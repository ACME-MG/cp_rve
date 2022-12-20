"""
 Title:         Shaper
 Description:   For creating non-large geometries for samples 
 Author:        Janzen Choi

"""

# Library
from modules.api import API

api = API(fancy=True, verbose=True)
api.read_pixels("617b_ebsd.csv", 5.2)
api.clean_pixels(10)
api.smoothen_edges(5)
api.visualise()

api.redefine_domain(850, 2200+850, 100, 1700+100) # 2200 x 1700
api.decrease_resolution(4)
api.visualise()

api.mesh("~/cubit/psculpt.exe", 19*5.2)
api.export_orientations("euler")