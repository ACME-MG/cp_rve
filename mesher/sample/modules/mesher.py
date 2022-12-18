"""
 Title:         Mesher
 Description:   For converting the pixels into a mesh
 Author:        Janzen Choi

"""

# Libraries
import subprocess, os, math
from modules.maths.pixel_maths import VOID_PIXEL_ID

# Input file
INPUT_FILE_CONTENT = """
BEGIN SCULPT
    
    # Dimensions
    nelx = {x_cells}
    nely = {y_cells}
    nelz = {z_cells}

    # Mesh Improvement
    smooth = 2
    defeature = 1
    remove_bad = 0.0

    # Remove cuts if any
    void_mat = {void_id}
    
    # Solver
    laplacian_iters = 10
    max_opt_iters = 100
    # adapt_type = 5
    # adapt_levels = {levels}
    
    # Output
    input_spn = {spn_file}
    exodus_file = {exodus_file}

END SCULPT
"""

# Mesh Parameters
NUM_PROCESSORS = 1

# Add void thickness
def add_void_thickness(file, pixel_grid, num_pixels):
    for _ in range(num_pixels):
        for pixel_list in pixel_grid:
            for _ in pixel_list:
                file.write(f"{VOID_PIXEL_ID} ")
    return num_pixels

# Generates the mesh
def coarse_mesh(psculpt_path, i_path, spn_path, exodus_path, pixel_grid, thickness):

    # Get dimensions
    y_size = round(len(pixel_grid))
    x_size = round(len(pixel_grid[0]))

    # Start writing
    file = open(spn_path, "w+")
    for _ in range(thickness):
        for pixel_list in pixel_grid:
            for pixel in pixel_list:
                file.write(f"{pixel} ")
    # thickness += add_void_thickness(file, pixel_grid, 3)
    file.close()

    # Calculate number of coarsenings (2^levels <= thickness)
    levels = min(3, math.floor(math.log(thickness, 2))) # max 3 levels

    # Create input file
    with open(i_path, "w+", newline = "") as file:
        file.write(INPUT_FILE_CONTENT.format(
            x_cells     = thickness,
            y_cells     = y_size,
            z_cells     = x_size,
            void_id     = VOID_PIXEL_ID,
            levels      = levels,
            spn_file    = spn_path,
            exodus_file = exodus_path,
        ))

    # Run mesh command
    command = f"mpiexec -n {NUM_PROCESSORS} {psculpt_path} -j {NUM_PROCESSORS} -i {i_path}"
    subprocess.run([command], shell = True, check = True)
    os.rename(f"{exodus_path}.e.1.0", f"{exodus_path}")