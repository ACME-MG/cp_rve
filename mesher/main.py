from modules.api import API

length = 16
api = API(str(length), 0)
api.read_tessellation(f"rve_700.tess", length)
api.visualise()
api.smooth_corners(3)
api.mesh("~/cubit/psculpt.exe", 1)
api.export_orientations("stats_700.csv", 500)