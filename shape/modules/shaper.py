"""
 Title:         Shaper
 Description:   For shaping sample-esque geometries
 Author:        Janzen Choi

"""

# Libraries
import os, math, time
import modules.imager as imager
import modules.reader as reader
import modules.visualise as visualise
import modules.maths.pixel_maths as pixel_maths
import modules.mesher as mesher
import modules.exporter as exporter

# Constants
INPUT_DIR       = "./input"
RESULTS_DIR     = "./results"
CTF_START_LINE  = 16
VOID_ID         = -1

# Shaper Class
class Shaper:

    # Constructor
    def __init__(self, fancy = False):
        
        # Initialise
        self.pixel_grid = []
        self.grain_map  = {}
        self.prog       = visualise.Progressor(fancy)
        self.img_count  = 1

        # Set up environment
        self.output_dir  = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        self.output_path = "{}/{}".format(RESULTS_DIR, self.output_dir)
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_path)

    # Reads the sample data from the csv file
    def read_pixels(self, csv_file, step_size=1):
        self.prog.queue(
            function    = self.__read_pixels__,
            arguments   = [csv_file, step_size],
            message     = "Reading pixel data from CSV file",
        )
    def __read_pixels__(self, csv_file, step_size):
        self.step_size = step_size
        self.pixel_grid, self.grain_map = reader.read_pixels(f"{INPUT_DIR}/{csv_file}", step_size)

    # Cleans the pixels
    def clean_pixels(self, num_cleans=1):
        self.prog.queue(
            function    = self.__clean_pixels__,
            arguments   = [num_cleans],
            message     = "Cleaning up the pixels",
        )
    def __clean_pixels__(self, num_cleans):
        for _ in range(num_cleans):
            self.pixel_grid = reader.clean_pixel_grid(self.pixel_grid)

    # Rotates the pixels CW by 90 degrees
    def rotate_CW_90(self):
        self.prog.queue(
            function    = self.__rotate_CW_90__,
            message     = "Rotating the pixels clockwise by 90 degrees",
        )
    def __rotate_CW_90__(self):
        self.pixel_grid = list(zip(*self.pixel_grid[::-1])) # no idea how
    
    # Vertically flips the pixels
    def vertical_flip(self):
        self.prog.queue(
            function    = self.__vertical_flip__,
            message     = "Vertically flips the pixels",
        )
    def __vertical_flip__(self):
        self.pixel_grid = self.pixel_grid[::-1]

    # Redefines the domain
    def redefine_domain(self, x_min, x_max, y_min, y_max):
        self.prog.queue(
            function    = self.__redefine__domain__,
            arguments   = [x_min, x_max, y_min, y_max],
            message     = "Redefining the domain",
        )
    def __redefine__domain__(self, x_min, x_max, y_min, y_max):
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
        self.prog.queue(
            function    = self.__decrease_resolution__,
            arguments   = [factor],
            message     = "Decreasing the sample resolution",
        )
    def __decrease_resolution__(self, factor):
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
        self.prog.queue(
            function    = self.__increase_resolution__,
            arguments   = [factor],
            message     = "Increasing the sample resolution",
        )
    def __increase_resolution__(self, factor):
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
        self.prog.queue(
            function    = self.__cut_circle__,
            arguments   = [x_centre, y_centre, radius],
            message     = "Performing circular cut",
        )
    def __cut_circle__(self, x_centre, y_centre, radius):
        x_centre = round(x_centre / self.step_size)
        y_centre = round(y_centre / self.step_size)
        radius = round(radius / self.step_size)
        coordinates_list = pixel_maths.get_coordinates_within_circle(x_centre, y_centre, radius)
        self.pixel_grid = pixel_maths.remove_pixels(self.pixel_grid, coordinates_list)

    # Creates a rectangular cut
    def cut_rectangle(self, x_min, x_max, y_min, y_max):
        self.prog.queue(
            function    = self.__cut_rectangle__,
            arguments   = [x_min, x_max, y_min, y_max],
            message     = "Performing rectangular cut",
        )
    def __cut_rectangle__(self, x_min, x_max, y_min, y_max):
        x_min = round(x_min / self.step_size)
        x_max = round(x_max / self.step_size)
        y_min = round(y_min / self.step_size)
        y_max = round(y_max / self.step_size)
        coordinates_list = pixel_maths.get_coordinates_within_rectangle(x_min, x_max, y_min, y_max)
        self.pixel_grid = pixel_maths.remove_pixels(self.pixel_grid, coordinates_list)

    # Creates a custom cut by reading from a file (and looking for black pixels)
    def cut_mask(self, png_file):
        self.prog.queue(
            function    = self.__cut_mask__,
            arguments   = [png_file],
            message     = "Performing cut using a mask",
        )
    def __cut_mask__(self, png_file):
        coordinates_list = imager.get_dead_pixels(f"{INPUT_DIR}/{png_file}")
        self.pixel_grid = pixel_maths.remove_pixels(self.pixel_grid, coordinates_list)

    # Creates an image of the sample
    def visualise(self, png_file = "sample"):
        self.prog.queue(
            function    = self.__visualise__,
            arguments   = [png_file],
            message     = "Visualising the sample",
        )
    def __visualise__(self, png_file):
        imager.generate_image(self.pixel_grid, f"{self.output_path}/{png_file}_{self.img_count}")
        self.img_count += 1

    # Generates a mesh
    def mesh(self, psculpt_path, thickness):
        self.prog.queue(
            function    = self.__mesh__,
            arguments   = [psculpt_path, thickness],
            message     = "Meshing the sample",
        )
    def __mesh__(self, psculpt_path, thickness):
        thickness = round(thickness / self.step_size)
        mesher.coarse_mesh(psculpt_path, self.output_path, self.pixel_grid, thickness)

    # Exports statistics
    def export(self, statistics, file = "stats.csv", include_header=True):
        self.prog.queue(
            function    = self.__export__,
            arguments   = [statistics, file, include_header],
            message     = "Exporting grain statistics",
        )
    def __export__(self, statistics, file, include_header):
        exporter.export_statistics(self.pixel_grid, self.grain_map, statistics, f"{self.output_path}/{file}", include_header)

    # Destructor
    def start(self):
        self.prog.start()

# For safely making a directory
def safe_mkdir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)