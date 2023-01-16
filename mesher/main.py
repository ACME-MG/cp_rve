"""
 Title:         Mesher
 Description:   For converting a tessellation into a mesh
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Code
length = 64
api = API(True, str(length), verbose=True)
api.read_tessellation("rve_1000.tess", length)
api.visualise()
api.smooth_corners(3)
api.mesh("~/cubit/psculpt.exe", 1)
api.export_orientations("stats_1000.csv", 1000)