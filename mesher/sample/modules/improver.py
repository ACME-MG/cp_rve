"""
 Title:         Improver
 Description:   Improves the quality of the grid
 Author:        Janzen Choi

"""

# Libraries
import modules.maths.pixel_maths as pixel_maths
from random import randint

# Cleans the pixel grid by replacing stray void / live pixels
def clean_pixel_grid(pixel_grid):

    # Dimensions of the pixel grid
    x_size = len(pixel_grid[0])
    y_size = len(pixel_grid)
    
    # Iterate through each pixel
    for row in range(y_size):
        for col in range(x_size):

            # Evaluate neighbouring pixels
            neighbours = pixel_maths.get_neighbours(col, row, x_size, y_size)
            void_neighbours = [n for n in neighbours if pixel_grid[n[1]][n[0]] == pixel_maths.VOID_PIXEL_ID]
            num_void = len(void_neighbours)
            
            # If half (or less) of the neighbours are void, then fill a void pixel
            if pixel_grid[row][col] == pixel_maths.VOID_PIXEL_ID and num_void <= len(neighbours) / 2:
                copy = neighbours[randint(0, len(neighbours) - 1)]
                pixel_grid[row][col] = pixel_grid[copy[1]][copy[0]]

            # If more than half of the neighbours are void, then remove a live pixel
            if pixel_grid[row][col] != pixel_maths.VOID_PIXEL_ID and num_void > len(neighbours) / 2:
                pixel_grid[row][col] = pixel_maths.VOID_PIXEL_ID

    # Return cleaned pixel grid
    return pixel_grid

# Smoothen the pixel grid by merging pixels
def smoothen_edges(pixel_grid):

    # Dimensions of the pixel grid
    x_size = len(pixel_grid[0])
    y_size = len(pixel_grid)
    
    # Iterate through each pixel
    for row in range(y_size):
        for col in range(x_size):
        
            # Evaluate neighbouring pixels
            neighbours = pixel_maths.get_neighbours(col, row, x_size, y_size)
            foreign_neighbours = [n for n in neighbours if pixel_grid[n[1]][n[0]] != pixel_grid[row][col]]

            # If there are more than 1 foreign neighbours, get absorbed
            if len(foreign_neighbours) > 2:
                foreign = foreign_neighbours[randint(0, len(foreign_neighbours) - 1)]
                pixel_grid[row][col] = pixel_grid[foreign[1]][foreign[0]]

    # Return cleaned pixel grid
    return pixel_grid

# Pads the pixel grid by replicating live pixels
def pad_edges(pixel_grid):
    
    # Dimensions of the pixel grid
    x_size = len(pixel_grid[0])
    y_size = len(pixel_grid)
    
    # Replicate it
    padded_pixel_grid = pixel_maths.get_void_pixel_grid(x_size, y_size)

    # Iterate through each pixel
    for row in range(y_size):
        for col in range(x_size):

            # If live, copy and skip
            if pixel_grid[row][col] != pixel_maths.VOID_PIXEL_ID:
                padded_pixel_grid[row][col] = pixel_grid[row][col]
                continue

            # Get live neighbouring pixels
            neighbours = pixel_maths.get_neighbours(col, row, x_size, y_size)
            live_neighbours = [n for n in neighbours if pixel_grid[n[1]][n[0]] != pixel_maths.VOID_PIXEL_ID]

            # If there is a live neighbour, then fill this void pixel
            if len(live_neighbours) > 0:
                copy = live_neighbours[randint(0, len(live_neighbours) - 1)]
                padded_pixel_grid[row][col] = pixel_grid[copy[1]][copy[0]]
    
    # Return padded pixel grid
    return padded_pixel_grid