"""
 File:          Compressor
 Description:   Compresses large EBSD CSV files
 Author:        Janzen Choi

"""

# Libraries
import time

# Constants
BIG_FILE = "ebsdExportColumnsTable.csv"
NEW_FILE = "617_ebsd.csv"
NEW_STEP = 6.5 # 3.25
PROGRESS_STEPS = 10000
EPSILON = 0.001

# Open both files
big_file = open(BIG_FILE, "r")
new_file = open(NEW_FILE, "w+")

# Extract header information
header = big_file.readline()
header_list = header.replace("\n", "").split(",")
x_index = header_list.index("x")
y_index = header_list.index("y")
phase_id_index = header_list.index("phaseId")
graid_id_index = header_list.index("grainId")
phi_1_index = header_list.index("Euler_phi1")
Phi_index = header_list.index("Euler_Phi")
phi_2_index = header_list.index("Euler_phi2")

# Transfer header
new_file.write("x,y,phaseId,grainId,Euler_phi1,Euler_Phi,Euler_phi2\n")

# Initialise before transfer
progress_count = 1
first_iteration = True
x_min, y_min = 0, 0
start_time = time.time()

# Transfer the contents of the files with lower resolution
print("Transfer starting soon ...")
for line in big_file.readlines():
    
    # If coordinates have NaN, then continue
    row_list = line.replace("\n", "").split(",")
    if "NaN" in row_list:
        continue

    # Get coordinates
    x = round(float(row_list[x_index]), 2) - x_min
    y = round(float(row_list[y_index]), 2) - y_min
    if first_iteration:
        x_min = x
        y_min = y
        first_iteration = False
    
    # If coordinates do not fit new step, then continue
    if round(x % NEW_STEP, 2) % NEW_STEP > 0 or round(y % NEW_STEP, 2) % NEW_STEP > 0:
        continue
    
    # Extract valid data
    phase_id    = row_list[phase_id_index]
    graid_id    = row_list[graid_id_index]
    phi_1       = row_list[phi_1_index]
    Phi         = row_list[Phi_index]
    phi_2       = row_list[phi_2_index]

    # Add extracted data to new file
    new_file.write(f"{x},{y},{phase_id},{graid_id},{phi_1},{Phi},{phi_2}\n")

    # Provide progress update every X transfered
    elapsed = round(time.time() - start_time)
    if progress_count % PROGRESS_STEPS == 0:
        print(f"{progress_count // PROGRESS_STEPS})\t{PROGRESS_STEPS} pixels transfered ({elapsed}s)")
    progress_count += 1

# Close both files
big_file.close()
new_file.close()