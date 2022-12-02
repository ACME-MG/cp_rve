"""
 Title:         Exporter
 Description:   Exports stuff
 Author:        Janzen Choi

"""

# Libraries
import csv
from modules.maths.pixel_maths import DEAD_PIXEL_ID

# Exports grain statistics
def export_statistics(pixel_grid, grain_map, statistic_list, path, include_header):
    
    # Get existing IDs
    id_list = [pixel for pixel_list in pixel_grid for pixel in pixel_list]
    id_list = list(dict.fromkeys(id_list))
    id_list.remove(DEAD_PIXEL_ID)

    # Redefine statistic list
    available_statistics = ["grain_id", "phase_id", "q1", "q2", "q3", "q4", "num_pixels"]
    statistic_list = [statistic for statistic in statistic_list if statistic in available_statistics]
    
    # Add grain IDs to grain map
    for grain_id in grain_map.keys():
        grain_map[grain_id]["grain_id"] = grain_id

    # Extract statistics for existing IDs
    rows = []
    for id in id_list:
        row = [grain_map[id][statistic] for statistic in statistic_list]
        rows.append(row)
    
    # Writes to the CSV file
    rows = [[statistic] for statistic in statistic_list] + rows if include_header else rows
    write_to_csv(path, rows)

# For writing to CSV files
def write_to_csv(path, rows):
    with open(path, "w+") as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)