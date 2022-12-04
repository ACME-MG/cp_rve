"""
 Title:         Mesher
 Description:   For converting a tessellation into a mesh
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Code
api = API(True, "64", verbose=True)
api.tess_2_tesr("rve_700.tess", 64)
api.visualise()
api.tesr_2_spn()
api.mesh("~/cubit/psculpt.exe", 1)
