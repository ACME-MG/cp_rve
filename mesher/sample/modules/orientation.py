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

# The Exodus Reader Class
class Exodus:

    # Constructor
    def __init__(self, exodus_path, spn_path, spn_size):
        
        # Initialise
        self.spn_size = spn_size # (x_length, y_length, z_length)

        # Reads the contents of the exodus file
        self.all_grains = pv.read(exodus_path)[0]
        bounds = self.all_grains.bounds
        self.exo_bounds = [{"min": bounds[2*i], "max": bounds[2*i+1], "range": bounds[2*i+1] - bounds[2*i]} for i in range(3)]

        # Reads the contents of the SPN file (0->x: 0->y: 0->z)
        with open(spn_path, "r") as spn_file:
            voxel_string = " ".join(spn_file.readlines())
            self.voxel_list = [int(voxel) for voxel in voxel_string.split(" ") if voxel != ""]
            self.id_list = list(set(self.voxel_list))

    # Retrieves the voxel value (assume coords within bounds)
    def get_grain_id(self, coordinates):
        pos = [math.floor((coordinates[i] - self.exo_bounds[i]["min"]) / self.exo_bounds[i]["range"] * self.spn_size[i]) for i in range(3)]
        grain_id_index = pos[0] * self.spn_size[1] * self.spn_size[2] + pos[1] * self.spn_size[2] + pos[2]
        return self.voxel_list[grain_id_index]

    # Gets the grain statistics of a grain
    def get_grain_stats(self, grain):
        elements = grain.cell_centers().points
        grain_id_list = [self.get_grain_id(list(element)) for element in elements]
        mode = max(set(grain_id_list), key=grain_id_list.count)
        freq = grain_id_list.count(mode)
        total = len(grain_id_list)
        return mode, freq, total

    # Determine the grain id of each grain
    def allocate_grains(self):

        # Initialise
        grain_id_list = []
        confidence_list = []

        # Iterate through grains
        for i in range(self.all_grains.n_blocks):
            grain = self.all_grains[i]
            
            # Get grain statistics
            mode, freq, total = self.get_grain_stats(grain)
            grain_id_list.append(mode)

            # Print progress and confidence
            confidence = round(freq / total * 100, 2)
            confidence_list.append(confidence)
            print(f"{i+1})\t id={mode}\t ({confidence}%)")

        # Print conclusion
        num_ids = len(grain_id_list)
        num_unique = len(list(set(grain_id_list)))
        avg_confidence = round(np.average(confidence_list), 2)
        print("------------------------------")
        print(f"Unique Allocations = {num_unique}/{num_ids}")
        print(f"Average Confidence = {avg_confidence}%")

        # Returns the mapping
        return grain_id_list
    
# Rewrites an orientation file based on grain id mappings
def reorient_grains(exodus_path, spn_path, spn_size, grain_map):

    # Get grain mapping
    exodus = Exodus(exodus_path, spn_path, spn_size)
    grain_id_list = exodus.allocate_grains()

    # Remap the grains and return
    new_grain_map = {}
    for i in range(len(grain_id_list)):
        old_id = grain_id_list[i]
        new_grain_map[i+1] = grain_map[old_id]
    return new_grain_map

# Converts a quaternion into a set of euler-bunge angles (rads)
def quat_to_euler(x, y, z, w):
    phi_1 = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    Phi   = math.asin(max([min([2 * (w * y - z * x), 1]), -1]))
    phi_2 = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
    return [phi_1, Phi, phi_2]

# Converts radians to degrees
def rad_to_deg(radians):
    if isinstance(radians, list):
        return [rad_to_deg(r) for r in radians]
    return radians * 180 / math.pi

# Returns a list of crystal orientations as quaternions
def get_quaternions(grain_map):
    
    # Get grain ids
    id_list = list(grain_map.keys())
    if VOID_PIXEL_ID in id_list:
        id_list.remove(VOID_PIXEL_ID)
    id_list.sort()

    # Extract statistics for existing IDs
    orientations = []
    for id in id_list:
        orientation = [grain_map[id][statistic] for statistic in ["q1", "q2", "q3", "q4"]]
        orientations.append(orientation)

    # Return
    return orientations
