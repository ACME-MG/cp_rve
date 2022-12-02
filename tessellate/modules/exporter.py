"""
 Title:         Exporter
 Description:   Exports data
 Author:        Janzen Choi

"""

# Libraries
import csv
from modules.helper.general import *

# Export parent statistics
def export_parent_statistics(grain_list, stats_path, has_twins, has_ori):

    # Export base statistics
    parent_header = ["id", "eq_radius", "sphericity"]
    parent_data = [[
        grain["id"],
        grain["diameter"] / 2,
        grain["sphericity"]
    ] for grain in grain_list]

    # If twins were added
    if has_twins:
        parent_header += ["num_twins"]
        for i in range(len(grain_list)):
            parent_data[i] += [grain_list[i]["num_twins"]]

    # If crystal orientations were defined
    if has_ori:
        parent_header += ["phi_1", "Phi", "phi_2"]
        for i in range(len(grain_list)):
            parent_data[i] += grain_list[i]["parent_ori"]

    # Write to CSV
    write_to_csv(stats_path + "_grain.csv", parent_header, parent_data)

# Export twin statistics
def export_twin_statistics(grain_list, stats_path, has_ori):

    # Prepare header
    twin_header = ["twin_id", "parent_id", "width", "gap"]
    twin_header += ["phi_1", "Phi", "phi_2"] if has_ori else []
    
    # Organise data
    twin_data = []
    for grain in grain_list:
        for i in range(grain["num_twins"]):
            twin = [
                len(twin_data) + 1,
                grain["id"],
                grain["twin_widths"][i],
                grain["twin_gaps"][i]
            ]
            twin += grain["twin_ori"] if has_ori else []
            twin_data.append(twin)
    
    # Write to CSV
    write_to_csv(stats_path + "_twin.csv", twin_header, twin_data)

# Converts a TESS to CSV
def export_cell_statistics(tess_path, csv_path):
    tess_path += ".tess"
    csv_path += "_cell.csv"
    
    # Get orientation (euler-bunge)
    ori_data = extract_data("ori", tess_path)
    ori_data = [float(o) for o in ori_data[2:]]

    # Writes data of each cell to CSV
    with open(csv_path, "w+") as file:
        writer = csv.writer(file)

        # Write headers
        headers = ["cell_id", "phi_1", "Phi", "phi_2"]
        writer.writerow(headers)

        # Iterate through each cell
        for i in range(len(ori_data) // 3):

            # Prepares the data
            row = [
                i + 1,
                round(ori_data[3 * i], 3),
                round(ori_data[3 * i + 1], 3),
                round(ori_data[3 * i + 2], 3),
            ]

            # Writes the data
            writer.writerow(row)

# Converts a TESR to CSV
def export_voxel_statistics(tesr_path, csv_path):
    tesr_path += ".tesr"
    csv_path += "_voxel.csv"

    # Get volume shape information
    vol_data = extract_data("general", tesr_path)
    volume_length = int(vol_data[2])

    # Get orientation (euler-bunge)
    ori_data = extract_data("ori", tesr_path)
    ori_data = [float(o) for o in ori_data[2:]]

    # Get positions and derive coordinates
    pos_data = extract_data("data", tesr_path)
    pos_data = [int(p) for p in pos_data[2:]]

    # Write data of each voxel to CSV (directly, to avoid RAM issues)
    with open(csv_path, "w+") as file:
        writer = csv.writer(file)

        # Write headers
        headers = ["voxel_id", "cell_id", "x", "y", "z", "phi_1", "Phi", "phi_2"]
        writer.writerow(headers)

        # Iterate through each voxel
        for i in range(len(pos_data)):

            # Provides progress updates
            if i % (len(pos_data) / 20) == 0:
                print("  Update ({}%)".format(1 + round(20 * i / len(pos_data))))

            # Prepares the data
            voxel_ori = ori_data[3 * (pos_data[i] - 1): 3 * pos_data[i]]
            row = [
                i,
                pos_data[i],
                i % volume_length,
                i // volume_length % volume_length,
                i // volume_length // volume_length,
                round(voxel_ori[0], 3),
                round(voxel_ori[1], 3),
                round(voxel_ori[2], 3),
            ]

            # Writes the data
            writer.writerow(row)
    
    # Finish message
    print("Finished everything!")

# Searches for a keyword in a text file and extracts the contained data
def extract_data(keyword, filename, end_char = "*"):
    
    # Read the file
    file = open(filename, "r")
    data = file.read()
    file.close()

    # Searches for the data encased by the keyword
    start   = data.find(keyword)
    data    = data[start:]
    end     = data.find(end_char)
    data    = data[:end]

    # Process the extracted data and return
    data = data.replace("\n", " ")
    data = data.split(" ")
    data = [d for d in data if d != ""]
    return data