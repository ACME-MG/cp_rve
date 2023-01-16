"""
 Title:         Mesher API
 Description:   API for meshing SPN files with coarse
 Author:        Janzen Choi

"""

# Libraries
import time, subprocess, sys
import modules.converter as converter
import modules.improver as improver
import modules.mesher as mesher
import modules.orientation as orientation

# Helper libraries
sys.path.append("../__common__")
from progressor import Progressor
from general import safe_mkdir, write_to_csv

# I/O directories
INPUT_DIR   = "./input"
RESULTS_DIR = "./results"

# API Class
class API:

    # Constructor
    def __init__(self, fancy=False, title="", verbose=False):
        
        # Initialise
        self.prog = Progressor(fancy, title, verbose)

        # Set up paths
        self.output_dir  = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        self.output_path = f"{RESULTS_DIR}/{self.output_dir}_{title}"
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_path)

        # Define file paths
        self.tesr_path      = f"{self.output_path}/rve.tesr"
        self.image_path     = f"{self.output_path}/raster"
        self.spn_path       = f"{self.output_path}/rve.spn"
        self.exodus_path    = f"{self.output_path}/mesh.e"
        self.input_path     = f"{self.output_path}/sculpt_input.i"
        self.orientation_path = f"{self.output_path}/input_orientations.csv"

    # Reads voxel information from a tessellation
    def read_tessellation(self, tess_file, length):
        self.prog.add(f"Converting {tess_file} into a {length}x{length}x{length} voxellation")
        tess_path = f"{INPUT_DIR}/{tess_file}"
        self.length = length
        converter.tess_2_tesr(tess_path, self.tesr_path, length)
        self.grain_grid = converter.tesr_2_grid(self.tesr_path)
  
    # Smooths the corners of grains
    def smooth_corners(self, iterations=1):
        self.prog.add(f"Smoothing the corner of grains for {iterations} iteration(s)")
        for _ in range(iterations):
            self.grain_grid = improver.smooth_corners(self.grain_grid)

    # Visualises a raster tessellation
    def visualise(self):
        self.prog.add("Visualising the raster tessellation")
        command = f"neper -V {self.tesr_path} -print {self.image_path}"
        subprocess.run([command], shell = True, check = True)

    # Conducts the mesh
    def mesh(self, psculpt_path, num_processors):
        self.prog.add("Generating adaptive mesh from spn file")
        converter.grid_2_spn(self.grain_grid, self.spn_path)
        orientation.renumber_grain_ids(self.spn_path)
        mesher.spn_mesh(self.spn_path, self.exodus_path, self.input_path, psculpt_path, num_processors, self.length)

    # Gets the new orientations
    def export_orientations(self, stats_file, tess_length):
        self.prog.add("Calculating and exporting the orientations")
        stats_path = f"{INPUT_DIR}/{stats_file}"
        orientation_list = orientation.get_orientations(stats_path, [tess_length]*3, self.spn_path, [self.length]*3, self.exodus_path)
        write_to_csv(self.orientation_path, orientation_list)