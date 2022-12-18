"""
 Title:         Mesher API
 Description:   API for meshing SPN files with coarse
 Author:        Janzen Choi

"""

# Libraries
import time, subprocess
import modules.converter as converter
import modules.mesher as mesher
import modules.orientation as orientation

# Helper libraries
import sys; sys.path.append("../../__common__")
from progressor import Progressor
from general import safe_mkdir

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

    # Converts from tessellation to raster tessellation
    def tess_2_tesr(self, tess_file, num_voxels):
        self.prog.add("Converting tessellation into raster tessellation")
        tess_path = f"{INPUT_DIR}/{tess_file}"
        self.num_voxels = num_voxels
        converter.tess_2_tesr(tess_path, self.tesr_path, num_voxels)
  
    # Visualises a raster tessellation
    def visualise(self):
        self.prog.add("Visualising the raster tessellation")
        command = f"neper -V {self.tesr_path} -print {self.image_path}"
        subprocess.run([command], shell = True, check = True)

    # Converts from raster tessellation to spn file
    def tesr_2_spn(self):
        self.prog.add("Converting raster tessellation into spn file")
        converter.tesr_2_spn(self.tesr_path, self.spn_path)

    # Conducts the mesh
    def mesh(self, psculpt_path, num_processors):
        self.prog.add("Generating adaptive mesh from spn file")
        mesher.spn_mesh(self.spn_path, self.exodus_path, self.input_path, psculpt_path, num_processors, self.num_voxels)

    # Gets the new orientations
    def export_orientations(self, stats_file, tess_length):
        self.prog.add("Exporting the orientations")
        stats_path  = f"{INPUT_DIR}/{stats_file}"
        orientation.export_orientations(stats_path, self.exodus_path, self.orientation_path, tess_length)