"""
 Title:         CTF File Reader
 Description:   Reads CTF Files
 Author:        Janzen Choi

"""

# Libraries
import modules.maths.pixel_maths as pixel_maths
import modules.maths.grain_maths as grain_maths
from random import randint

# Constants
STEP_DECIMAL_PLACE = 3

# Gets the range and step size from a list of values
def get_info(value_list):
    num_values = len(set(value_list))
    min_value = min(value_list)
    return num_values, min_value

# Converts a CSV file into a grid of pixels
def read_pixels(path, step_size):

    # Open file and read header
    file = open(path, "r")
    header = file.readline().replace("\n", "").split(",")
    rows = file.readlines()
    
    # Get column indexes
    x_index = header.index("x")
    y_index = header.index("y")
    phase_id_index = header.index("phaseId")
    graid_id_index = header.index("grainId")
    quat_1_index = header.index("orientations_a")
    quat_2_index = header.index("orientations_b")
    quat_3_index = header.index("orientations_c")
    quat_4_index = header.index("orientations_d")

    # Get dimensions
    x_cells, x_min = get_info([float(row.split(",")[x_index]) for row in rows])
    y_cells, y_min = get_info([float(row.split(",")[y_index]) for row in rows])

    # Initialise pixel grid and grain map
    pixel_grid = pixel_maths.get_dead_pixel_grid(x_cells, y_cells)
    grain_map = {}

    # Read CSV and fill grid
    prev_row = [0,0,0,0,0,0,0,0]
    for row in rows:

        # Process data
        row_list = row.replace("\n", "").split(",")
        row_list = prev_row if "NaN" in row_list else row_list # if NaN, use previous pixel data
        row_list = [float(val) for val in row_list]
        prev_row = row_list
        grain_id = round(row_list[graid_id_index])

        # Add to pixel grid
        x = round(float(row_list[x_index] - x_min) / step_size)
        y = round(float(row_list[y_index] - y_min) / step_size)
        pixel_grid[y][x] = grain_id + 1

        # Add to grain map if not yet added
        if not grain_id in grain_map:
            grain_dict = grain_maths.get_grain_dict(
                phase_id = row_list[phase_id_index],
                q1 = row_list[quat_1_index],
                q2 = row_list[quat_2_index],
                q3 = row_list[quat_3_index],
                q4 = row_list[quat_4_index],
                num_pixels = 1,
            )
            grain_map[grain_id] = grain_dict
        
        # Update grain map if already added
        else:
            old_grain_dict = grain_map[grain_id]
            new_grain_dict = grain_maths.update_grain_dict(
                grain_dict = old_grain_dict,
                q1 = row_list[quat_1_index],
                q2 = row_list[quat_2_index],
                q3 = row_list[quat_3_index],
                q4 = row_list[quat_4_index],
            )
            grain_map[grain_id] = new_grain_dict
    
    # Close file and return grid and map
    file.close()
    return pixel_grid, grain_map

# Cleans the pixel grid by replacing stray dead pixels
def clean_pixel_grid(pixel_grid):

    # Dimensions of the pixel grid
    x_size = len(pixel_grid[0])
    y_size = len(pixel_grid)
    
    # Iterate through each pixel
    for row in range(y_size):
        for col in range(x_size):
        
            # Evaluate neighbouring pixels
            neighbours = pixel_maths.get_neighbours(col, row, x_size, y_size)
            alive = [n for n in neighbours if pixel_grid[n[1]][n[0]] != pixel_maths.DEAD_PIXEL_ID]
            num_dead = len(neighbours) - len(alive)
            
            # If half (or less) of the neighbours are dead, then revive a dead pixel
            if pixel_grid[row][col] == pixel_maths.DEAD_PIXEL_ID and num_dead <= len(neighbours) / 2:
                copy = neighbours[randint(0, len(neighbours) - 1)]
                pixel_grid[row][col] = pixel_grid[copy[1]][copy[0]]

            # If more than half of the neighbours are dead, then kill a live pixel
            if pixel_grid[row][col] != pixel_maths.DEAD_PIXEL_ID and num_dead > len(neighbours) / 2:
                pixel_grid[row][col] = pixel_maths.DEAD_PIXEL_ID

    # Return new pixel grid
    return pixel_grid