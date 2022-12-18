"""
 File:          Compressor
 Description:   Compresses large EBSD CSV files
 Author:        Janzen Choi

"""

# Libraries
import time

# Constants
BIG_FILE = "617_ebsd_big.csv"
NEW_FILE = "617_ebsd.csv"
BIG_STEP = 0.65
NEW_STEP = BIG_STEP * 8 # 5.2
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
quat_1_index = header_list.index("orientations_a")
quat_2_index = header_list.index("orientations_b")
quat_3_index = header_list.index("orientations_c")
quat_4_index = header_list.index("orientations_d")

# Transfer header
new_file.write("x,y,phaseId,grainId,orientations_a,orientations_b,orientations_c,orientations_d\n")

# Initialise before transfer
progress_count = 1
start_time = time.time()

# Transfer the contents of the files with lower resolution
print("Transfer starting soon ...")
for line in big_file.readlines():
    
    # If coordinates have NaN, then continue
    row_list = line.replace("\n", "").split(",")
    if "NaN" in row_list:
        continue

    # Get coordinates
    x = round(float(row_list[x_index]), 2)
    y = round(float(row_list[y_index]), 2)
    
    # If coordinates do not fit new step, then continue
    if ((x % NEW_STEP >= EPSILON
    and abs(NEW_STEP - (x % NEW_STEP)) >= EPSILON)
    or (y % NEW_STEP >= EPSILON
    and abs(NEW_STEP - (y % NEW_STEP)) >= EPSILON)):
        continue
    
    # Extract valid data
    phase_id    = row_list[phase_id_index]
    graid_id    = row_list[graid_id_index]
    quat_1      = row_list[quat_1_index]
    quat_2      = row_list[quat_2_index]
    quat_3      = row_list[quat_3_index]
    quat_4      = row_list[quat_4_index]

    # Add extracted data to new file
    new_file.write(f"{x},{y},{phase_id},{graid_id},{quat_1},{quat_2},{quat_3},{quat_4}\n")

    # Provide progress update every X transfered
    elapsed = round(time.time() - start_time)
    if progress_count % PROGRESS_STEPS == 0:
        print(f"{progress_count // PROGRESS_STEPS})\t{PROGRESS_STEPS} pixels transfered ({elapsed}s)")
    progress_count += 1

# Close both files
big_file.close()
new_file.close()