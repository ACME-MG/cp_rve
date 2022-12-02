"""
 Title:         Pixel Maths
 Description:   Contains pixel-related functions
 Author:        Janzen Choi

"""

# Libraries
import numpy as np

# Constants
DEAD_PIXEL_ID = 1

# Returns a dead pixel (to be removed)
def get_dead_pixel():
    return DEAD_PIXEL_ID

# Returns a grid of dead pixels
def get_dead_pixel_grid(x_cells, y_cells):
    pixel_grid = []
    for _ in range(y_cells):
        pixel_list = []
        for _ in range(x_cells):
            dead_pixel = get_dead_pixel()
            pixel_list.append(dead_pixel)
        pixel_grid.append(pixel_list)
    return pixel_grid

# Replaces a grid of pixels with dead pixels based on coordinates
def remove_pixels(pixel_grid, coordinates_list):
    for coordinates in coordinates_list:
        try:
            pixel_grid[coordinates[1]][coordinates[0]] = get_dead_pixel()
        except IndexError:
            pass
    return pixel_grid

# Rounds a number to the nearest multiple of another number
def mult_round(to_round, mult_number, decimal_place = 5):
    result =  mult_number*(round(to_round / mult_number))
    return round(result, decimal_place)

# Returns a list of coordinates within a defined circle
def get_coordinates_within_circle(x_centre, y_centre, radius):

    # Define bounds
    x_min = max(x_centre - radius, 0)
    x_max = x_centre + radius
    y_min = max(y_centre - radius, 0)
    y_max = y_centre + radius

    # Get list of coordinates within bounds
    coordinates_list = []
    for x in np.arange(x_min, x_max, 1):
        for y in np.arange(y_min, y_max, 1):
            if (x-x_centre)**2 + (y-y_centre)**2 < radius ** 2:
                coordinates_list.append((round(x), round(y)))
    
    # Return list of pixels
    return coordinates_list

# Returns a list of coordinates within a defined rectangle
def get_coordinates_within_rectangle(x_min, x_max, y_min, y_max):
    coordinates_list = []
    for x in np.arange(x_min, x_max, 1):
        for y in np.arange(y_min, y_max, 1):
            if x >= x_min and x <= x_max and y >= y_min and y <= y_max:
                coordinates_list.append((round(x), round(y)))
    return coordinates_list

# Gets the neighbouring indices of a pixel
def get_neighbours(x, y, x_size, y_size):
    neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    neighbours = [
        neighbour for neighbour in neighbours
        if neighbour[0] >= 0 and neighbour[0] < x_size
        and neighbour[1] >= 0 and neighbour[1] < y_size
    ]
    return neighbours