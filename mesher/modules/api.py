"""
 Title:         Mesher API
 Description:   API for meshing SPN files with coarse
 Author:        Janzen Choi

"""

# Libraries
import subprocess, sys
from modules.improver import smooth_corners
from modules.mesher import spn_mesh
from modules.converter import tess_2_tesr, tesr_2_grid, grid_2_spn
from modules.orientation import get_orientations, renumber_grain_ids

# Helper libraries
sys.path.append("../__common__")
from api_template import APITemplate
from general import write_to_csv

# API Class
class API(APITemplate):

    # Constructor
    def __init__(self, title="", display=2):
        super().__init__(title, display)

    # Reads voxel information from a tessellation
    def read_tessellation(self, tess_file, length):
        self.add(f"Converting {tess_file} into a {length}^3 voxellation")
        self.length = length
        tess_path = self.get_input(tess_file)
        self.tesr_path = self.get_output("rve.tesr")
        tess_2_tesr(tess_path, self.tesr_path, length)
        self.grain_grid = tesr_2_grid(self.tesr_path)
  
    # Smooths the corners of grains
    def smooth_corners(self, iterations=1):
        self.add(f"Smoothing the corner of grains for {iterations} iteration(s)")
        for _ in range(iterations):
            self.grain_grid = smooth_corners(self.grain_grid)

    # Visualises a raster tessellation
    def visualise(self):
        self.add("Visualising the raster tessellation")
        self.image_path = self.get_output("raster")
        command = f"neper -V {self.tesr_path} -print {self.image_path}"
        subprocess.run([command], shell = True, check = True)

    # Conducts the mesh
    def mesh(self, psculpt_path, num_processors):
        self.add("Generating adaptive mesh from spn file")
        self.spn_path = self.get_output("rve.spn")
        self.exodus_path = self.get_output("mesh.e")
        self.sculpt_path = self.get_output("sculpt_input.i")
        scale_factor = 1
        grid_2_spn(self.grain_grid, self.spn_path)
        renumber_grain_ids(self.spn_path)
        spn_mesh(self.spn_path, self.exodus_path, self.sculpt_path, psculpt_path,
                 num_processors, self.length, scale_factor)

    # Gets the new orientations
    def export_orientations(self, stats_file, tess_length):
        self.add("Calculating and exporting the orientations")
        stats_path = self.get_input(stats_file)
        self.orientation_path = self.get_output("input_orientations.csv")
        orientation_list = get_orientations(stats_path, [tess_length]*3, self.spn_path,
                                            [self.length]*3, self.exodus_path)
        write_to_csv(self.orientation_path, orientation_list)