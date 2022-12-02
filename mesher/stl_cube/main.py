"""
 Title:         Main
 Description:   Wrapper for Cubit Coreform to create hexahedral meshes
 Author:        Janzen Choi

"""

# Libraries
from modules.api import API

# Parameters
PSCULPT_PATH    = "~/cubit/psculpt.exe" # "C:/Program Files/Coreform Cubit 2022.4/bin/psculpt.exe"
EPU_PATH        = "~/cubit/epu.exe" # "C:/Program Files/Coreform Cubit 2022.4/bin/epu.exe"
NUM_PROCESSORS  = 1
VOLUME_LENGTH   = 150
NUM_CELLS       = 6
VERBOSE_DISPLAY = True

# Creates the hex mesh
api = API(PSCULPT_PATH, EPU_PATH, NUM_PROCESSORS, NUM_CELLS, VOLUME_LENGTH, VERBOSE_DISPLAY)
api.write_diatom_file()
api.write_input_file()
api.sculpt_hex_mesh()
