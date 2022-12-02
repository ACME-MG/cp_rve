"""
 Title:         Sculpt Diatom
 Description:   Creates the sculpt diatom file
 Author:        Janzen Choi

"""

# Libraries
import os

# File name
DIATOM_FILE = "sculpt.diatom"

# Diatom file format
DIATOM_FORMAT = """
  diatoms
{subformats}
  enddia
"""
DIATOM_SUBFORMAT = """
    package '{name}'
      material {index}
      insert stl
        FILE = '{stl_file}'
      endinsert
    endp
"""

# For writing the diatom file
def write_diatom_file(stl_path, dest_path):

    # Get names of all STL files
    stl_files = [file for file in os.listdir(stl_path) if file.endswith(".stl")]

    # Create subformat string
    subformats = ""
    for i in range(len(stl_files)):
        subformats += DIATOM_SUBFORMAT.format(
            name      = "Volume_{}".format(i + 1),
            index     = i + 1,
            stl_file  = "../../{}/{}".format(stl_path, stl_files[i]),
        )
    
    # Write diatom file
    with open("{}/{}".format(dest_path, DIATOM_FILE), "w+") as file:
        file.write(DIATOM_FORMAT.format(
          subformats = subformats
        ))