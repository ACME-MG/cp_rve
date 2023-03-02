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

        # Dimensions
        nelx = {num_voxels}
        nely = {num_voxels}
        nelz = {num_voxels}

        # Fixed mesh improvement
        smooth = 2
        pillow_curves = true
        pillow_boundaries = true
        micro_shave = true
        # scale = 2

        # Variable mesh improvement
        # defeature = 1
        opt_threshold = 0.7
        pillow_curve_layers = 3
        pillow_curve_thresh = 0.3
        
        # Solver
        laplacian_iters = 5
        max_opt_iters = 50
        
        # Output files
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
    os.rename(exodus_file + ".e.1.0", exodus_file)