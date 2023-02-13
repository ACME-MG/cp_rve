from modules.api import API
for length in [32]:
    api = API(str(length), 2)
    api.read_tessellation("rve_500.tess", length)
    api.visualise()
    api.smooth_corners(3)
    api.mesh("~/cubit/psculpt.exe", 1)
    api.export_orientations("stats_500.csv", 500)