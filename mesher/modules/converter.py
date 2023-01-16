"""
 Title:         Converter
 Description:   For converting volume information
 Author:        Janzen Choi

"""

# Libraries
import subprocess

# Creates an empty grid
def initialise_grid(length, value=0):
    grid = [[[value for _ in range(length)] for _ in range(length)] for _ in range(length)]
    return grid      

# Converts a tessellation (.tess) into a raster tessellation (.tesr)
def tess_2_tesr(tess_path, tesr_path, length):
    loadtess = f"-loadtess {tess_path}"
    tesr_format = f"-format tesr -tesrsize {length} -tesrformat ascii"
    command = f"neper -T {loadtess} {tesr_format} -o {tesr_path}"
    subprocess.run([command], shell = True, check = True)

# Converts the raster tessellation file into a 3D grid of grain IDs
def tesr_2_grid(tesr_path):

    # Open file (.tesr) for reading and initialise
    file = open(tesr_path, "r")
    start_word = "ascii"
    end_word = "***end"
    started = False

    # Iterate the lines and store grain IDs
    grain_list = []
    for line in file:
        line_list = line.replace("\n", "").split(" ")
        if start_word in line_list:
            started = True
            continue
        if end_word in line_list:
            break
        if started:
            grain_list += [int(id) for id in line_list]
    file.close()

    # Initialise, populate, and return 3D grid
    length = round(len(grain_list)**(1/3))
    grain_grid = initialise_grid(length)
    for i in range(length):
        for j in range(length):
            for k in range(length):
                index = i*length**2 + j*length + k
                grain_grid[i][j][k] = grain_list[index]
    return grain_grid

# Converts the grid into a spn file
def grid_2_spn(grain_grid, spn_path):
    file = open(spn_path, "w+")
    for grain_plane in grain_grid:
        for grain_line in grain_plane:
            for grain in grain_line:
                file.write(f"{grain} ")
    file.close()