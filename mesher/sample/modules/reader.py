"""
 Title:         CTF File Reader
 Description:   Reads CTF Files
 Author:        Janzen Choi

"""

# Libraries
import modules.maths.pixel_maths as pixel_maths
import modules.maths.grain_maths as grain_maths

# Constants
STEP_DECIMAL_PLACE = 3

# Gets the range and step size from a list of values
def get_info(value_list, step_size):
    max_value = max(value_list)
    min_value = min(value_list)
    num_values = round((max_value - min_value) / step_size) + 1
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
    phi_1_index = header.index("euler_phi1")
    Phi_index   = header.index("euler_Phi")
    phi_2_index = header.index("euler_phi2")

    # Get dimensions
    x_cells, x_min = get_info([float(row.split(",")[x_index]) for row in rows], step_size)
    y_cells, y_min = get_info([float(row.split(",")[y_index]) for row in rows], step_size)
    
    # Initialise pixel grid and grain map
    pixel_grid = pixel_maths.get_void_pixel_grid(x_cells, y_cells)
    grain_map = {}

    # Read CSV and fill grid
    for row in rows:

        # Process data
        row_list = row.replace("\n", "").split(",")
        if "NaN" in row_list or "nan" in row_list:
            continue
        row_list = [float(val) for val in row_list]
        grain_id = round(row_list[graid_id_index]) + 1 # 1 dedicated to void pixels

        # Add to pixel grid
        x = round(float(row_list[x_index] - x_min) / step_size)
        y = round(float(row_list[y_index] - y_min) / step_size)
        pixel_grid[y][x] = grain_id

        # Add to grain map if not yet added
        if not grain_id in grain_map:
            grain_dict = grain_maths.get_grain_dict(
                phase_id    = row_list[phase_id_index],
                phi_1       = row_list[phi_1_index],
                Phi         = row_list[Phi_index],
                phi_2       = row_list[phi_2_index],
                size        = 1,
            )
            grain_map[grain_id] = grain_dict
        
        # Update grain map if already added
        else:
            old_grain_dict = grain_map[grain_id]
            new_grain_dict = grain_maths.update_grain_dict(
                grain_dict  = old_grain_dict,
                phi_1       = row_list[phi_1_index],
                Phi         = row_list[Phi_index],
                phi_2       = row_list[phi_2_index],
            )
            grain_map[grain_id] = new_grain_dict
    
    # Close file and return grid and map
    file.close()
    return pixel_grid, grain_map

# Renumbers the grain IDs
def renumber_grains(pixel_grid, grain_map):
    
    # Get list of old IDs
    flattened = [pixel for pixel_list in pixel_grid for pixel in pixel_list]
    old_ids = list(set(flattened))
    if pixel_maths.VOID_PIXEL_ID in old_ids:
        old_ids.remove(pixel_maths.VOID_PIXEL_ID)
    old_ids.sort()

    # Map old IDs to new IDs
    id_map = {}
    for i in range(len(old_ids)):
        id_map[old_ids[i]] = i + 1
    
    # Create new pixel grid
    new_pixel_grid = pixel_maths.get_void_pixel_grid(len(pixel_grid[0]), len(pixel_grid))
    for row in range(len(pixel_grid)):
        for col in range(len(pixel_grid[0])):
            if pixel_grid[row][col] == pixel_maths.VOID_PIXEL_ID:
                continue
            new_id = id_map[pixel_grid[row][col]]
            new_pixel_grid[row][col] = new_id
    
    # Create new grain map
    new_grain_map = {}
    for old_id in old_ids:
        new_id = id_map[old_id]
        new_grain_map[new_id] = grain_map[old_id]
    
    # Return new pixel grid and grain map
    return new_pixel_grid, new_grain_map