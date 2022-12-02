"""
 Title:         Coarse Mesher
 Description:   For meshing SPN files with coarse
 Author:        Janzen Choi

"""


# Libraries
import subprocess, os

# Converts a microstructure file (.spn) into an adaptive hexahedral mesh
def spn_mesh(spn_file, exodus_file, input_file, psculpt_path, num_processors, num_voxels):
    
    # Define input file
    input_file_content = f"""
    BEGIN SCULPT
        nelx = {num_voxels}
        nely = {num_voxels}
        nelz = {num_voxels}

        pillow = 3
        smooth = 2
        
        laplacian_iters = 10
        max_opt_iters = 100
        adapt_type = 5
        adapt_levels = 3

        defeature = 1
        micro_shave = true
        remove_bad = 0.0
        
        input_spn = {spn_file}
        exodus_file = {exodus_file}
    END SCULPT
    """

    # Create input file
    with open(input_file, "w+", newline = "") as file:
        file.write(input_file_content)

    # Run mesh command
    command = f"mpiexec -n {num_processors} {psculpt_path} -j {num_processors} -i {input_file}"
    subprocess.run([command], shell = True, check = True)
    os.rename(exodus_file + ".e.1.0", exodus_file + ".e")