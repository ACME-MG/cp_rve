"""
 Title:         tess_2_mesh file
 Description:   For converting a tessellation into a mesh
 Author:        Janzen Choi

"""

# Libraries
import os, subprocess

# Parallel Sculpt path
PSCULPT_PATH    = "~/cubit/psculpt.exe"

# Directories
RESULTS_DIR     = "./results"
INPUT_DIR       = "./input"

# Files
TESS_FILE       = f"{INPUT_DIR}/rve.tess"
TESR_FILE       = f"{RESULTS_DIR}/rve.tesr"
SPN_FILE        = f"{RESULTS_DIR}/rve.spn"
SCULPT_INPUT    = f"{RESULTS_DIR}/rve.i"
EXODUS_FILE     = f"{RESULTS_DIR}/sculpt" # .e

# Mesh parameters
VOLUME_LENGTH   = 150
NUM_VOXELS      = 16 # voxels
NUM_PROCESSORS  = 1

# Main function
def main():
    tess_2_tesr()
    tesr_2_spn()
    spn_2_mesh()

# Convert from tess to tesr
def tess_2_tesr():
    loadtess = f"-loadtess {TESS_FILE}"
    tesr_format = f"-format tesr -tesrsize {NUM_VOXELS} -tesrformat ascii"
    command = f"neper -T {loadtess} {tesr_format} -o {TESR_FILE}"
    subprocess.run([command], shell = True, check = True)

# Convert from tesr to spn
def tesr_2_spn():

    # Open files for reading and writing
    tesr_file = open(TESR_FILE, "r")
    spn_file = open(SPN_FILE, "w+", newline = "")

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

# Convert from spn to mesh
def spn_2_mesh():

    # Define input file
    input_file_content = f"""
    BEGIN SCULPT
        cell_size = {VOLUME_LENGTH/NUM_VOXELS}
        nelx = {NUM_VOXELS}
        nely = {NUM_VOXELS}
        nelz = {NUM_VOXELS}

        pillow = 3
        smooth = 2
        
        laplacian_iters = 10
        max_opt_iters = 100
        adapt_type = 5
        adapt_levels = 3

        defeature = 1
        micro_shave = true
        remove_bad = 0.0
        
        input_spn = {SPN_FILE}
        exodus_file = {EXODUS_FILE}
    END SCULPT
    """

    # Create input file
    with open(SCULPT_INPUT, "w+", newline = "") as file:
        file.write(input_file_content)

    # Run mesh command
    command = f"mpiexec -n {NUM_PROCESSORS} {PSCULPT_PATH} -j {NUM_PROCESSORS} -i {SCULPT_INPUT}"
    subprocess.run([command], shell = True, check = True)
    os.rename(EXODUS_FILE + ".e.1.0", EXODUS_FILE + ".e")

# Calls the main function
if __name__ == "__main__":
    main()