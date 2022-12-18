"""
 Title:         Mesher
 Description:   For converting a tessellation into a mesh
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Code
resolution = 16
api = API(True, str(resolution), verbose=True)
api.tess_2_tesr("rve_1000.tess", resolution)
api.visualise()
api.tesr_2_spn()
api.mesh("~/cubit/psculpt.exe", 1)
api.export_orientations("stats_1000.csv", 1000)

exit()

for resolution in [8, 12, 16, 24, 32, 48, 64, 96]:
    api = API(True, str(resolution), verbose=True)
    api.tess_2_tesr("rve_1000.tess", resolution)
    api.visualise()
    api.tesr_2_spn()
    api.mesh("~/cubit/psculpt.exe", 1)
    api.export_orientations("stats_1000.csv", 1000)