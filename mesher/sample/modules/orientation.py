"""
 Title:         Exporter
 Description:   Exports stuff
 Author:        Janzen Choi

"""

# Libraries
import math
import pyvista as pv
import numpy as np
from modules.maths.pixel_maths import VOID_PIXEL_ID

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
            if math.nan in element:
                continue
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
    
# Rewrites an orientation file based on grain id mappings
def get_orientations(exodus_path, spn_path, spn_size, grain_map):
    
    # Get grain ids
    spn_id_list = list(grain_map.keys())
    if VOID_PIXEL_ID in spn_id_list:
        spn_id_list.remove(VOID_PIXEL_ID)
    spn_id_list.sort()

    # Get spn to exo mapping and print
    spn_to_exo = get_spn_to_exo(exodus_path, spn_path, spn_size)
    avg_confidence = round(np.average([spn_to_exo[spn_id]["confidence"] for spn_id in spn_to_exo.keys()]), 2)
    print(f"SPN (Num. of Grains):       {len(spn_id_list)}")
    print(f"EXO (Num. of Grains):       {len(spn_to_exo)}")
    print(f"SPN > EXO (Confidence):     {avg_confidence}%")
    
    # Get orientations and return
    void_orientation = [0, 0, 0]
    orientation_list = []
    for spn_id in spn_id_list:
        orientation = [grain_map[spn_id][i] for i in ["phi_1", "Phi", "phi_2"]] if spn_id in spn_to_exo.keys() else void_orientation
        orientation_list.append(orientation)
    return orientation_list
