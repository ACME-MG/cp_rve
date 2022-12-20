"""
 Title:         Helper
 Description:   General helper functions
 Author:        Janzen Choi

"""

# Libraries
import subprocess, os, csv, inspect
import numpy as np
import pandas as pd
import printer as printer

# For safely making a directory
def safe_mkdir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

# For quickly writing to a file
def quick_write(file_name, content):
    with open(file_name, "w+") as file:
        file.write(content)
        
# Converts a list of dictionaries to a CSV format
def dict_list_to_csv(dictionary_list):
    headers = list(dictionary_list[0].keys())
    data = [[d[1] for d in dictionary.items()] for dictionary in dictionary_list]
    return headers, data

# For writing to CSV files
def write_to_csv(path, data):
    with open(path, "w+") as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

# Runs a command using a single thread
def run(command, shell = True, check = True):
    subprocess.run(["OMP_NUM_THREADS=1 " + command], shell = shell, check = check)

# Performs a 3x3 matrix multiplication
def get_matrix_product(matrix_1, matrix_2):
    result = [[0,0,0], [0,0,0], [0,0,0]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += matrix_1[i][k] * matrix_2[k][j]
    return result

# Inverts a matrix
def get_inverted(matrix):
    matrix = np.array(matrix)
    inverted = [list(i) for i in np.linalg.inv(matrix)]
    return inverted

# Inserts a commas and a conjunction into a list of strings
def conjunct(str_list, conjunction):
    if len(str_list) == 1:
        return str_list[0]
    elif len(str_list) == 2:
        return "{} {} {}".format(str_list[0], conjunction, str_list[1])
    conjuncted = ", ".join(str_list[:-1])
    conjuncted += ", {} {}".format(conjunction, str_list[-1])
    return conjuncted

# Silently raises an exception
def silent_raise(exception, caller = ""):
    caller = inspect.stack()[1][3] if caller == "" else caller
    print("\n  Error in '{}':\n".format(caller))
    print("  {}\n".format(exception))
    exit()

# Checks whether a variable is a number
def is_number(variable):
    return isinstance(variable, float) or isinstance(variable, int)

# Transposes a 2D list of lists
def transpose(list_of_lists):
    transposed = pd.DataFrame(list_of_lists).T.values.tolist()
    return transposed