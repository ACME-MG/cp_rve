"""
 Title:         Orientation
 Description:   For exporting orientation information
 Author:        Janzen Choi

"""

# Libraries
import pyvista as pv
import numpy as np
import math

# Renumbers the SPN file
def renumber_grain_ids(spn_path):
    
    # Read the SPN file
    with open(spn_path, "r") as spn_file:
        voxel_string = " ".join(spn_file.readlines())
        voxel_list = [int(voxel) for voxel in voxel_string.split(" ") if voxel != ""]

    # Get unique and sorted ids
    id_list = list(set(voxel_list))
    id_list.sort()

    # Map new ids to old voxel list
    id_map = {}
    for i in range(len(id_list)):
        id_map[id_list[i]] = i+1
    new_voxel_list = [str(id_map[voxel]) for voxel in voxel_list]
    new_voxel_string = " ".join(new_voxel_list) + "\n"

    # Write new SPN file
    with open(spn_path, "w+") as spn_file:
        spn_file.write(new_voxel_string)

# Gets the orientations based on the voxel coordinates and voxel cluster centroids
def get_orientations(csv_path, csv_size, spn_path, spn_size, exo_path):
    
    # Get mappings
    spn_to_csv = get_spn_to_csv(csv_path, csv_size, spn_path, spn_size)
    spn_to_exo = get_spn_to_exo(exo_path, spn_path, spn_size)
    
    # Gets the number of grains
    with open(csv_path, "r") as file:
        num_csv_grains = len(file.readlines())
    num_spn_grains = len(spn_to_csv)
    num_exo_grains = len(spn_to_exo)

    # Print out mapping information
    error_list = [spn_to_csv[spn_id]["error"] for spn_id in spn_to_csv.keys()]
    confidence_list = [spn_to_exo[spn_id]["confidence"] for spn_id in spn_to_exo.keys()]
    print(f"CSV (number of grains):     {num_csv_grains}")
    print(f"SPN (number of grains):     {num_spn_grains}")
    print(f"EXO (number of grains):     {num_exo_grains}")
    print(f"SPN > CSV (AVG dist.):      {round(np.average(error_list), 2)}")
    print(f"SPN > EXO (AVG conf.):      {round(np.average(confidence_list), 2)}%")

    # Calculate orientations
    void_orientation = [0, 0, 0]
    orientation_list = []
    for spn_id in range(1, num_spn_grains+1):
        orientation = spn_to_csv[spn_id]["orientation"] if spn_id in spn_to_exo.keys() else void_orientation
        orientation_list.append(orientation)
    return orientation_list

# Gets the grain IDs of exodus grains from the SPN file
def get_spn_to_exo(exo_path, spn_path, spn_size):

    # Reads the contents of the exodus file
    exo_grains = pv.read(exo_path)[0]
    bounds = exo_grains.bounds
    exo_bounds = [{"min": bounds[2*i], "max": bounds[2*i+1], "range": bounds[2*i+1] - bounds[2*i]} for i in range(3)]

    # Read the contents of the SPN file
    with open(spn_path, "r") as spn_file:
        voxel_string = " ".join(spn_file.readlines())
        voxel_list = [int(voxel) for voxel in voxel_string.split(" ") if voxel != ""]

    # Iterate through the exodus grains
    spn_to_exo = {}
    for i in range(exo_grains.n_blocks):
        
        # Get grain elements
        exo_grain = exo_grains[i]
        elements = exo_grain.cell_centers().points
        elements = [list(element) for element in elements]

        # Get the grain ids based on element coordinates
        id_list = []
        for element in elements:
            pos = [math.floor((element[j] - exo_bounds[j]["min"]) / exo_bounds[j]["range"] * spn_size[j]) for j in range(3)]
            grain_id_index = pos[0] * spn_size[1] * spn_size[2] + pos[1] * spn_size[2] + pos[2]
            grain_id = voxel_list[grain_id_index]
            id_list.append(grain_id)
        
        # Add exodus grain id
        mode = max(set(id_list), key=id_list.count)
        freq = id_list.count(mode)
        total = len(id_list)
        spn_to_exo[mode] = {"exo_id": i+1, "confidence": round(freq / total * 100, 2)}

    # Return
    return spn_to_exo

# Maps the SPN grains to the CSV orientations
def get_spn_to_csv(csv_path, csv_size, spn_path, spn_size):
    
    # Read the grain statistics from the CSV file
    stats_file = open(csv_path, "r") # x, y, z, phi_1, Phi, phi_2
    csv_grains = []
    for row in stats_file.readlines():
        row_list = row.replace("\n", "").split(",")
        row_list = [float(val) for val in row_list]
        csv_grains.append({
            "x":        round(row_list[0], 2),
            "y":        round(row_list[1], 2),
            "z":        round(row_list[2], 2),
            "phi_1":    row_list[3],
            "Phi":      row_list[4],
            "phi_2":    row_list[5],
        })
    stats_file.close()

    # Read the SPN file
    with open(spn_path, "r") as spn_file:
        voxel_string = " ".join(spn_file.readlines())
        voxel_list = [int(voxel) for voxel in voxel_string.split(" ") if voxel != ""]

    # Group up the voxels based on grain id
    grain_map = {}
    for i in range(len(voxel_list)):

        # Initialise
        voxel = voxel_list[i]
        coordinates = convert_1d_to_3d(i, spn_size[0], spn_size[1], spn_size[2])
        centroid = [coordinates[i] * csv_size[i] / spn_size[i] for i in range(len(coordinates))]

        # If already grouped
        if voxel in grain_map.keys():
            old_size = grain_map[voxel]["size"]
            grain_map[voxel]["x"] = (grain_map[voxel]["x"]*old_size+centroid[0]) / (old_size+1)
            grain_map[voxel]["y"] = (grain_map[voxel]["y"]*old_size+centroid[1]) / (old_size+1)
            grain_map[voxel]["z"] = (grain_map[voxel]["z"]*old_size+centroid[2]) / (old_size+1)
            grain_map[voxel]["size"] = old_size + 1

        # If not grouped yet
        else:
            grain_map[voxel] = {
                "x": centroid[0],
                "y": centroid[1],
                "z": centroid[2],
                "size": 1,
                "grain": {},
                "error": 10000000,
            }
    
    # Allocate mesh grains to CSV grains
    for grain_id in grain_map.keys():
        mesh_grain = grain_map[grain_id]
        for csv_grain in csv_grains:
            error = sum([(mesh_grain[i] - csv_grain[i])**2 for i in ["x", "y", "z"]])**(1/2)
            if error < mesh_grain["error"]:
                mesh_grain["error"] = error
                mesh_grain["grain"] = csv_grain
    
    # Get spn to csv map
    spn_to_csv = {}
    for id in range(1, len(grain_map)+1):
        csv_grain       = grain_map[id]["grain"]
        orientation     = [csv_grain[i] for i in ["phi_1", "Phi", "phi_2"]]
        spn_to_csv[id]  = {"orientation": orientation, "error": grain_map[id]["error"]}
    return spn_to_csv

# Converts an index into 3D coordinates
def convert_1d_to_3d(index, x_length, y_length, _):
    x = index % x_length
    y = (index / x_length) % y_length
    z = index // (x_length * y_length)
    return [x, y, z]