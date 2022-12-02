"""
 Title:         Converter
 Description:   For converting files into various formats
 Author:        Janzen Choi

"""

# Libraries
import subprocess

# Converts a tessellation (.tess) into a raster tessellation (.tesr)
def tess_2_tesr(tess_file, tesr_file, num_voxels):
    loadtess = f"-loadtess {tess_file}"
    tesr_format = f"-format tesr -tesrsize {num_voxels} -tesrformat ascii"
    command = f"neper -T {loadtess} {tesr_format} -o {tesr_file}"
    subprocess.run([command], shell = True, check = True)

# Converts a raster tessellation (.tesr) to a microstructure file (SPN)
def tesr_2_spn(tesr_file, spn_file):

    # Open files for reading and writing
    tesr_file = open(tesr_file, "r")
    spn_file = open(spn_file, "w+", newline = "")

    # Initialise for tesr to spn conversion
    start_word = "ascii"
    end_word = "***end"
    started = False
    finished = False

    # Iterate line by line
    for line in tesr_file:
        if finished:
            break

        # Iterate word for word
        line = line.replace("\n", " ")
        for word in line.split(" "):
            if word == "":
                continue

            # If haven't started writing
            if not started and word == start_word:
                started = True
                continue

            # If still writing
            if started and word != end_word:
                spn_file.write(f"{int(word)} ")

            # If finished writing
            if started and word == end_word:
                finished = True
                break

    # Close files
    spn_file.close()
    tesr_file.close()