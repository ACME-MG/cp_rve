"""
 Title:         Sculpt Input
 Description:   Creates the sculpt input file
 Author:        Janzen Choi

"""

# Libraries
from modules.sculpt_diatom import DIATOM_FILE

# File name
INPUT_FILE  = "sculpt.i"
DIATOM_FILE = DIATOM_FILE
EXODUS_FILE = "sculpt"

# Input file format
INPUT_FORMAT = """
BEGIN SCULPT

  cell_size = {cell_size}
  xmin = 0
  ymin = 0
  zmin = 0
  xmax = {volume_length}
  ymax = {volume_length}
  zmax = {volume_length}
  nelx = {num_cells}
  nely = {num_cells}
  nelz = {num_cells}
  
  pillow = 3
  smooth = 2
  csmooth = 5
  defeature = 1
  laplacian_iters = 10
  max_opt_iters = 100

  quality = true
  micro_shave = true
  remove_bad = 0.0
  
  diatom_file = {diatom}
  exodus_file = {exodus}

END SCULPT
"""

# For writing the input file
def write_input_file(num_cells, volume_length, dest_path):
    with open("{}/{}".format(dest_path, INPUT_FILE), "w+") as file:
        file.write(INPUT_FORMAT.format(
            cell_size     = volume_length/num_cells,
            num_cells     = num_cells,
            volume_length = volume_length,
            diatom        = DIATOM_FILE,
            exodus        = EXODUS_FILE,
        ))