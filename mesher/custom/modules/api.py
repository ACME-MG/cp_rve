"""
 Title:         Shaper API
 Description:   API for shaping sample-esque geometries
 Author:        Janzen Choi

"""

# Libraries
import math, time
import modules.imager as imager
import modules.improver as improver
import modules.reader as reader
import modules.maths.pixel_maths as pixel_maths
import modules.mesher as mesher
import modules.exporter as exporter

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
    def __init__(self, fancy=False, name=""):
        
        # Initialise
        self.pixel_grid = []
        self.grain_map  = {}
        self.prog       = Progressor(fancy, name)
        self.img_count  = 1

        # Set up environment
        name = "" if name == "" else f" ({name})"
        self.output_dir  = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        self.output_path = f"{RESULTS_DIR}/{self.output_dir}{name}"
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_path)

    # Reads the sample data from the csv file
    def read_pixels(self, csv_file, step_size=1):
        self.prog.add("Reading pixel data from CSV file")
        self.step_size = step_size
        self.pixel_grid, self.grain_map = reader.read_pixels(f"{INPUT_DIR}/{csv_file}", step_size)

    # Cleans the pixels
    def clean_pixels(self, iteration=1):
        self.prog.add("Cleaning up the pixels")
        for _ in range(iteration):
            self.pixel_grid = improver.clean_pixel_grid(self.pixel_grid)

    # Smoothens the grain edges
    def smoothen_edges(self, iteration=1):
        self.prog.add("Smoothing the grain edges")
        for _ in range(iteration):
            self.pixel_grid = improver.smoothen_edges(self.pixel_grid)

    # Pads the grain edges
    def pad_edges(self, iteration=1):
        self.prog.add("Padding the grain edges")
        for _ in range(iteration):
            self.pixel_grid = improver.pad_edges(self.pixel_grid)

    # Rotates the pixels CW by 90 degrees
    def rotate_CW_90(self):
        self.prog.add("Rotating the pixels CW 90 degrees")
        self.pixel_grid = list(zip(*self.pixel_grid[::-1])) # no idea how
    
    # Vertically flips the pixels
    def vertical_flip(self):
        self.prog.add("Vertically flips the pixels")
        self.pixel_grid = self.pixel_grid[::-1]

    # Redefines the domain
    def redefine_domain(self, x_min, x_max, y_min, y_max):
        self.prog.add("Redefining the domain")
        x_min = round(x_min / self.step_size)
        x_max = round(x_max / self.step_size)
        y_min = round(y_min / self.step_size)
        y_max = round(y_max / self.step_size)
        new_pixel_grid = pixel_maths.get_dead_pixel_grid(x_max - x_min, y_max - y_min)
        for row in range(y_min, y_max):
            for col in range(x_min, x_max):
                try:
                    new_pixel_grid[row - y_min][col - x_min] = self.pixel_grid[row][col]
                except IndexError:
                    pass
        self.pixel_grid = new_pixel_grid

    # Decreases the resolution of the sample
    def decrease_resolution(self, factor):
        self.prog.add("Decreasing the sample resolution")
        self.step_size *= factor
        new_x_size = math.ceil(len(self.pixel_grid[0]) / factor)
        new_y_size = math.ceil(len(self.pixel_grid) / factor)
        new_pixel_grid = pixel_maths.get_dead_pixel_grid(new_x_size, new_y_size)
        for row in range(new_y_size):
            for col in range(new_x_size):
                new_pixel_grid[row][col] = self.pixel_grid[row * factor][col * factor]
        self.pixel_grid = new_pixel_grid

    # Increases the resolution of the sample
    def increase_resolution(self, factor):
        self.prog.add("Increasing the sample resolution")
        self.step_size /= factor
        new_x_size = len(self.pixel_grid[0]) * factor
        new_y_size = len(self.pixel_grid) * factor
        new_pixel_grid = pixel_maths.get_dead_pixel_grid(new_x_size, new_y_size)
        for row in range(new_y_size):
            for col in range(new_x_size):
                new_pixel_grid[row][col] = self.pixel_grid[math.floor(row / factor)][math.floor(col / factor)]
        self.pixel_grid = new_pixel_grid

    # Creates a circular cut (doesn't handle x_step != y_step)
    def cut_circle(self, x_centre, y_centre, radius):
        self.prog.add("Performing circular cut")
        x_centre = round(x_centre / self.step_size)
        y_centre = round(y_centre / self.step_size)
        radius = round(radius / self.step_size)
        coordinates_list = pixel_maths.get_coordinates_within_circle(x_centre, y_centre, radius)
        self.pixel_grid = pixel_maths.remove_pixels(self.pixel_grid, coordinates_list)

    # Creates a rectangular cut
    def cut_rectangle(self, x_min, x_max, y_min, y_max):
        self.prog.add("Performing rectangular cut")
        x_min = round(x_min / self.step_size)
        x_max = round(x_max / self.step_size)
        y_min = round(y_min / self.step_size)
        y_max = round(y_max / self.step_size)
        coordinates_list = pixel_maths.get_coordinates_within_rectangle(x_min, x_max, y_min, y_max)
        self.pixel_grid = pixel_maths.remove_pixels(self.pixel_grid, coordinates_list)

    # Creates a custom cut by reading from a file (and looking for black pixels)
    def cut_mask(self, png_file):
        self.prog.add("Performing cut using a mask")
        coordinates_list = imager.get_dead_pixels(f"{INPUT_DIR}/{png_file}")
        self.pixel_grid = pixel_maths.remove_pixels(self.pixel_grid, coordinates_list)

    # Creates an image of the sample
    def visualise(self, png_file="sample"):
        self.prog.add("Visualising the sample")
        imager.generate_image(self.pixel_grid, f"{self.output_path}/{png_file}_{self.img_count}")
        self.img_count += 1

    # Generates a mesh
    def mesh(self, psculpt_path, thickness):
        self.prog.add("Meshing the sample")
        thickness = round(thickness / self.step_size)
        mesher.coarse_mesh(psculpt_path, self.output_path, self.pixel_grid, thickness)

    # Exports statistics
    def export(self, statistics, file = "stats.csv", include_header=True):
        self.prog.add("Exporting grain statistics")
        exporter.export_statistics(self.pixel_grid, self.grain_map, statistics, f"{self.output_path}/{file}", include_header)