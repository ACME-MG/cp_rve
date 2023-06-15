"""
 Title:         Statifyer
 Description:   Extracts statistics from microstructure data
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
from copy import deepcopy

# Returns a list of areas
def get_areas(pixel_grid:list, scale:float=1) -> list:

    # Get list and set of grain IDs
    flattened = [pixel for pixel_list in pixel_grid for pixel in pixel_list]
    grain_id_list = list(set(flattened))

    # Initialise list of areas
    num_grains = len(grain_id_list)
    area_list = [0 for _ in range(len(grain_id_list))]

    # Calculate areas for each grain, from lowest to highest ID
    for i in range(num_grains):
        area = flattened.count(grain_id_list[i])
        area_list[i].append(area)
    
    # Apply scale and return
    scale_2 = scale ** 2
    area_list = [area * scale_2 for area in area_list]
    return area_list

# Takes a list of values and creates a dictionary noting down their first instances
def get_first_pos(value_list:list) -> dict:
    
    # Initialise dictionary
    unique_value_list = list(set(value_list))
    value_dict = {}
    for unique_value in unique_value_list:
        value_dict[unique_value] = None # has to be overwritten

    # Add values to dictionary
    for pos in range(len(value_list)):
        value = value_list[pos]
        if value_dict[value] == None:
            value_dict[value] = pos
        
    # Return dictionary
    return value_dict

# Transposes a 2D list of lists
def transpose(list_of_lists):
    transposed = np.array(list_of_lists).T.tolist()
    return transposed

# Returns a list of perimeters
def get_perimeters(pixel_grid:list, scale:float=1) -> list:

    # Get list and set of grain IDs
    flattened = [pixel for pixel_list in pixel_grid for pixel in pixel_list]
    grain_id_list = list(set(flattened))

    # Initialise a dict containing outer pixels
    outer_pixel_dict = {}
    for grain_id in grain_id_list:
        outer_pixel_dict[grain_id] = []

    # Initialise grid dimensions
    x_size = len(pixel_grid[0])
    y_size = len(pixel_grid)

    # Iterate through rows
    for y in y_size:

        # Get first and last positions
        first_pos_dict = get_first_pos(pixel_grid[y])
        new_pixel_list = deepcopy(pixel_grid[y])
        new_pixel_list.reverse()
        last_pos_dict = get_first_pos(new_pixel_list)

        # Add positions to dictionary
        for grain_id in first_pos_dict.keys():
            coordinates = (first_pos_dict[grain_id], y)
            outer_pixel_dict[grain_id].append(coordinates)
        
        # Get last position
        for grain_id in last_pos_dict.keys():
            coordinates = (last_pos_dict[grain_id], y)
            outer_pixel_dict[grain_id].append(coordinates)