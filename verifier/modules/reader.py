"""
 Title:         Reader
 Description:   Reads data of different formats
 Author:        Janzen Choi

"""

# Constants
VOID_PIXEL_ID = 100000 # large number

# Tries to float cast a value
def try_float_cast(value:str) -> float:
    try:
        return float(value)
    except:
        return value

# Converts a header file into a dict of lists
def read_csv(csv_path:str, delimeter:str=",") -> dict:

    # Read all data from CSV (assume that file is not too big)
    csv_fh = open(csv_path, "r")
    csv_lines = csv_fh.readlines()
    csv_fh.close()

    # Initialisation for conversion
    csv_dict = {}
    headers = csv_lines[0].replace("\n", "").split(delimeter)
    csv_lines = csv_lines[1:]
    for header in headers:
        csv_dict[header] = []

    # Start conversion to dict
    for csv_line in csv_lines:
        csv_line_list = csv_line.replace("\n", "").split(delimeter)
        for i in range(len(headers)):
            value = try_float_cast(csv_line_list[i])
            csv_dict[headers[i]].append(value)
    
    # Return the dict
    return csv_dict

# Returns a grid of void pixels
def get_void_pixel_grid(x_size, y_size, void_id=VOID_PIXEL_ID):
    pixel_grid = []
    for _ in range(y_size):
        pixel_list = []
        for _ in range(x_size):
            void_pixel = void_id
            pixel_list.append(void_pixel)
        pixel_grid.append(pixel_list)
    return pixel_grid

# Interprets a string of grain IDs as 2D pixel data
def get_pixel_grid(grain_id_str:str, x_size:int, y_size:int) -> list:

    # Initialise list of grain ids
    grain_id_list = [int(grain_id) for grain_id in grain_id_str.split(" ")]
    if len(grain_id_list) != x_size * y_size:
        raise ValueError("X and Y dimensions passed in do not match number of grain IDs!")

    # Populate pixel grid
    pixel_grid = get_void_pixel_grid(x_size, y_size)
    for y in range(y_size):
        for x in range(x_size):
            grain_id = grain_id_list[y*x_size+x]
            pixel_grid[x][y] = grain_id
    
    # Return pixel grid
    return pixel_grid