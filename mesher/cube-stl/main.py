"""
 Title:         Main
 Description:   Wrapper for Cubit Coreform to create hexahedral meshes
 Author:        Janzen Choi

"""

# Libraries
from modules.mesher import Mesher

# Parameters
PSCULPT_PATH    = "~/cubit/psculpt.exe" # "C:/Program Files/Coreform Cubit 2022.4/bin/psculpt.exe"
EPU_PATH        = "~/cubit/epu.exe" # "C:/Program Files/Coreform Cubit 2022.4/bin/epu.exe"
NUM_PROCESSORS  = 1
VOLUME_LENGTH   = 150
NUM_CELLS       = 6
VERBOSE_DISPLAY = True

# Creates the hex mesh
mesher = Mesher(PSCULPT_PATH, EPU_PATH, NUM_PROCESSORS, NUM_CELLS, VOLUME_LENGTH, VERBOSE_DISPLAY)
mesher.write_diatom_file()
mesher.write_input_file()
mesher.sculpt_hex_mesh()
mesher.commence_mesh()
