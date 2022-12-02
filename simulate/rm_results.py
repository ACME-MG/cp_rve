"""
 Title:         Results Remover
 Description:   For removing the contents of the simulation results
 Author:        Janzen Choi

"""

# Libraries
import os

# Constants
RESULTS_PATH = "./results/"

# Get all directories
files = [os.path.join(RESULTS_PATH, file) for file in os.listdir(RESULTS_PATH)]
directories = [file for file in files if os.path.isdir(file)]

# Remove the contents of each directory
for directory in directories:
    directory_files = [os.path.join(directory, file) for file in os.listdir(directory)]
    for directory_file in directory_files:
        os.remove(directory_file)
    os.rmdir(directory)