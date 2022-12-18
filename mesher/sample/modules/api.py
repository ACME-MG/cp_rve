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
import modules.orientation as orientation

# Helper libraries
import sys; sys.path.append("../../__common__")
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
        self.pixel_grid = []
        self.grain_map  = {}
        self.prog       = Progressor(fancy, title, verbose)
        self.img_count  = 1

        # Set up environment
        title = "" if title == "" else f" ({title})"
        self.output_dir  = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        self.output_path = f"{RESULTS_DIR}/{self.output_dir}{title}"
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_path)

        # Define paths
        self.i_path      = f"{self.output_path}/sample.i"
        self.spn_path    = f"{self.output_path}/sample.spn"
        self.exodus_path = f"{self.output_path}/sample.e"

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
        new_pixel_grid = pixel_maths.get_void_pixel_grid(x_max - x_min, y_max - y_min)
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
        new_pixel_grid = pixel_maths.get_void_pixel_grid(new_x_size, new_y_size)
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
        new_pixel_grid = pixel_maths.get_void_pixel_grid(new_x_size, new_y_size)
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
        coordinates_list = imager.get_void_pixels(f"{INPUT_DIR}/{png_file}")
        self.pixel_grid = pixel_maths.remove_pixels(self.pixel_grid, coordinates_list)

    # Creates an image of the sample
    def visualise(self, png_file="sample"):
        self.prog.add("Visualising the sample")
        imager.generate_image(self.pixel_grid, f"{self.output_path}/{png_file}_{self.img_count}")
        self.img_count += 1

    # Generates a mesh
    def mesh(self, psculpt_path, thickness):
        self.prog.add("Meshing the sample")

        # Renumber grains
        self.pixel_grid, self.grain_map = reader.renumber_grains(self.pixel_grid, self.grain_map)
        
        # Mesh renumbered grains
        if thickness < self.step_size:
            self.prog.fail()
        self.thickness = round(thickness / self.step_size)
        mesher.coarse_mesh(psculpt_path, self.i_path, self.spn_path, self.exodus_path, self.pixel_grid, self.thickness)

    # Exports the grain orientations (after meshing)
    def export_orientations(self, form="quaternion", file="input_orientations.csv"):
        self.prog.add(f"Exporting orientations in {form} form")
        
        # Fix grain mapping
        spn_size = [self.thickness, len(self.pixel_grid), len(self.pixel_grid[0])]
        self.grain_map = orientation.reorient_grains(self.exodus_path, self.spn_path, spn_size, self.grain_map)

        # Export
        orientations = orientation.get_quaternions(self.grain_map)
        if form in ["eb", "euler", "euler-bunge"]:
            orientations = [orientation.quat_to_euler(*q) for q in orientations]
            orientations = orientation.rad_to_deg(orientations)
        write_to_csv(f"{self.output_path}/{file}", orientations)

    # Exports spn dimensions
    def export_dimensions(self, file="dim.txt"):
        self.dim_path = f"{self.output_path}/{file}"
        with open(self.dim_path, "w+") as file:
            if self.thickness != None:
                file.write(f"x: {self.thickness}\n")
            file.write(f"y: {len(self.pixel_grid)}\n")
            file.write(f"z: {len(self.pixel_grid[0])}\n")