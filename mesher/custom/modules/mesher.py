"""
 Title:         Mesher
 Description:   For converting the pixels into a mesh
 Author:        Janzen Choi

"""

# Libraries
import subprocess, os, math

# File Names
SPN_FILE    = "sample.spn"
INPUT_FILE  = "sample.i"
EXODUS_FILE = "sample"

# Input file
INPUT_FILE_CONTENT = """
BEGIN SCULPT
    nelx = {x_cells}
    nely = {y_cells}
    nelz = {z_cells}
    
    smooth = 2
    defeature = 1
    remove_bad = 0.0
    
    laplacian_iters = 10
    max_opt_iters = 100
    adapt_type = 5
    adapt_levels = {levels}
    
    input_spn = {spn_file}
    exodus_file = {exodus_file}
END SCULPT
"""

# Mesh Parameters
NUM_PROCESSORS = 1

# Generates the mesh
def coarse_mesh(psculpt_path, results_dir, pixel_grid, thickness):
    
    # Get dimensions
    y_size = round(len(pixel_grid))
    x_size = round(len(pixel_grid[0]))

    # Start writing
    with open(f"{results_dir}/{SPN_FILE}", "w+") as file:
        for _ in range(thickness):
            for pixel_list in pixel_grid:
                for pixel in pixel_list:
                    file.write(f"{pixel} ")

    # Calculate number of coarsenings (2^levels <= thickness)
    levels = min(5, math.floor(math.log(thickness, 2))) # max 5 levels

    # Create input file
    with open(f"{results_dir}/{INPUT_FILE}", "w+", newline = "") as file:
        file.write(INPUT_FILE_CONTENT.format(
            x_cells     = thickness,
            y_cells     = y_size,
            z_cells     = x_size,
            levels      = levels,
            spn_file    = f"{results_dir}/{SPN_FILE}",
            exodus_file = f"{results_dir}/{EXODUS_FILE}",
        ))

    # Run mesh command
    command = f"mpiexec -n {NUM_PROCESSORS} {psculpt_path} -j {NUM_PROCESSORS} -i {results_dir}/{INPUT_FILE}"
    subprocess.run([command], shell = True, check = True)
    os.rename(f"{results_dir}/{EXODUS_FILE}.e.1.0", f"{results_dir}/{EXODUS_FILE}.e")
    exit() # DELETE ME