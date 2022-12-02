"""
 Title:         Mesher
 Description:   For converting a tessellation into a mesh
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Code
api = API(fancy=True)
api.tess_2_tesr("rve.tess", 16)
api.tesr_2_spn()
api.mesh("~/cubit/psculpt.exe", 1)
