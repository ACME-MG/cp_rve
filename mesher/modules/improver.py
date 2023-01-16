"""
 Title:         Improver
 Description:   For improving the quality of the grain grid
 Author:        Janzen Choi

"""

# Gets the coordinates of neighbouring cells
def get_neighbours(x, y, z, length):
    neighbours = [(x-1,y,z), (x+1,y,z), (x,y-1,z), (x,y+1,z), (x,y,z-1), (x,y,z+1)]
    neighbours = [
        neighbour for neighbour in neighbours
        if neighbour[0] >= 0 and neighbour[0] < length
        and neighbour[1] >= 0 and neighbour[1] < length
        and neighbour[2] >= 0 and neighbour[2] < length
    ]
    return neighbours

# Smooths the corners of grains
def smooth_corners(grain_grid):

    # Initialise
    replaced = 0
    length = len(grain_grid)
    
    # Iterate through the grain grid
    for z in range(length):
        for y in range(length):
            for x in range(length):

                # Get neighbours
                neighbour_coords = get_neighbours(x, y, z, length)
                neighbour_ids = [grain_grid[c[2]][c[1]][c[0]] for c in neighbour_coords]

                # Ignore surrounded voxels (> 1 neighbouring common voxel)
                if neighbour_ids.count(grain_grid[z][y][x]) > 1:
                    continue

                # Replace unsurrounded voxels (<= 1) with most common neighbour
                mode_neighbour = max(set(neighbour_ids), key=neighbour_ids.count)
                if neighbour_ids.count(mode_neighbour) > 1:
                    grain_grid[z][y][x] = mode_neighbour
                    replaced += 1
    
    # Return new grain grid
    print(f"Replaced {replaced} voxel(s)")
    return grain_grid
