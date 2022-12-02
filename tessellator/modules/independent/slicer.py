"""
 Title:         Slicer
 Description:   Slices a 3D raster tessellation into 2D maps
 Author:        Janzen Choi

"""

# Libraries
import os, math
import modules.lognormal as lognormal
import modules.helper.progressor as progressor
from modules.helper.general import *

# Constants
RESOLUTION      = 1
NUM_SLICES      = 3
RESULTS_DIR     = "./results/"
TARGET          = "output_3d500"

# Main function
def main():
    prog = progressor.Progressor()
    slicer = Slicer("{}/{}/".format(RESULTS_DIR, TARGET))
    prog.queue(slicer.read_pos_data,            message = "Reading positional data of voxels")
    prog.queue(slicer.slice_volume,             message = "Slicing RVE into 2D sheets of grains")
    prog.queue(slicer.reassign_grain_ids,       message = "Reassigning the ids of all the grains")
    # prog.queue(slicer.slice_to_tesr,            message = "Converting slices into 2D raster tessellations")
    # prog.queue(slicer.visualise_slices,         message = "Visualise 2D raster tessellations")
    prog.queue(slicer.order_voxels_in_grains,   message = "Ordering voxels based on grain ids")
    prog.queue(slicer.remove_boundary_grains,   message = "Removing grains on boundaries")
    prog.queue(slicer.export_equivalent_radii,  message = "Exporting the equivalent radii")
    prog.commence(TARGET)

# The Slicer Class
class Slicer:

    # Constructor
    def __init__(self, target_dir):
        
        # Define directories
        self.input_dir  = target_dir
        self.output_dir = self.input_dir + "sliced/"
        
        # Define file paths
        self.input_tesr  = self.input_dir + "parent"
        self.output_csv  = self.output_dir + "stats"
        self.output_plot = self.output_dir + "plot"
        self.output_tesr = self.output_dir + "slice"
        self.output_img  = self.output_dir + "img"
        
        # Create a directory for output
        safe_mkdir(self.output_dir)
        output_files = os.listdir(self.output_dir)
        for file in output_files:
            os.remove(self.output_dir + file)

    # Returns a list of voxels
    def read_pos_data(self):

        # Get volume shape information
        vol_data = extract_data("general", self.input_tesr + ".tesr")
        self.volume_length = int(vol_data[2])

        # Get positions and derive coordinates
        self.pos_data = extract_data("data", self.input_tesr + ".tesr")
        self.pos_data = [int(p) for p in self.pos_data[2:]]

    # Order the voxel positions into slices
    def slice_volume(self):

        # Positions for the slices
        slice_gap = self.volume_length // NUM_SLICES
        slice_x_list = [i * slice_gap for i in range(NUM_SLICES)] 

        # Iterate through each voxel's positional data
        self.slice_list = [[] for _ in range(NUM_SLICES)]
        for i in range(len(self.pos_data)):

            # Ignore non slices
            x = i % self.volume_length
            if not x in slice_x_list:
                continue

            # Add voxel to slice list
            slice_id = slice_x_list.index(x)
            self.slice_list[slice_id].append({
                "voxel_id": i,
                "slice_id": slice_id,
                "grain_id": self.pos_data[i],
                "x": x,
                "y": i // self.volume_length % self.volume_length,
                "z": i // self.volume_length // self.volume_length,
            })

        # Release positional data from memory
        del self.pos_data
    
    # Reassigns the grain ids of the voxels
    def reassign_grain_ids(self):
        for slice in self.slice_list:
            grain_id_list = []
            for voxel in slice:
                try:
                    grain_index = grain_id_list.index(voxel["grain_id"])
                    voxel["grain_id"] = grain_index + 1
                except:
                    old_grain_id = voxel["grain_id"]
                    grain_id_list.append(old_grain_id)
                    voxel["grain_id"] = len(grain_id_list)

    # Converts the slices into raster tessellation files
    def slice_to_tesr(self):
        for i in range(len(self.slice_list)):

            # Convert slice to list of ids
            id_list = [str(voxel["grain_id"]) for voxel in self.slice_list[i]]
            id_str = " ".join(id_list)
            num_grains = len(set(id_list))

            # Generate string
            length_string       = "{} {} ".format(self.volume_length, self.volume_length)
            resolution_string   = "{} {} ".format(RESOLUTION, RESOLUTION)
            data_string         = "***tesr\n **format\n   2.1\n **general\n   2\n   {}\n   {}\n ".format(length_string, resolution_string)
            data_string        += "**cell\n   {}\n **data\n   ascii\n{}\n***end".format(num_grains, id_str)

            # Write to file
            with open(self.output_tesr + "_" + str(i + 1) + ".tesr", "w+") as file:
                file.write(data_string)
    
    # Visualises the slices
    def visualise_slices(self):
        for i in range(len(self.slice_list)):
            suffix = "_" + str(i + 1)
            options = "-datacellcol id -cameraangle 14.5 -imagesize 800:800"
            run("neper -V {}.tesr {} -print {}".format(self.output_tesr + suffix, options, self.output_img + suffix))

    # Orders the voxels in grains
    def order_voxels_in_grains(self):
        grain_list_list = []
        
        # Iterate through each slice
        for slice in self.slice_list:
            num_grains = len(set([voxel["grain_id"] for voxel in slice]))
            grain_list = [[] for _ in range(num_grains)]
            for voxel in slice:
                grain_list[voxel["grain_id"] - 1].append(voxel)
            grain_list_list.append(grain_list)

        # Release old slice list from memory
        del self.slice_list
        self.slice_list = grain_list_list

    # Checks whether a grain is on a boundary
    def check_on_boundary(self, grain):
        for voxel in grain:
            if voxel["y"] in [0, self.volume_length - RESOLUTION] or voxel["z"] in [0, self.volume_length - RESOLUTION]:
                return True
        return False

    # Removes boundary grains
    def remove_boundary_grains(self):
        new_slice_list = [[grain for grain in slice if not self.check_on_boundary(grain)] for slice in self.slice_list]
        del self.slice_list
        self.slice_list = new_slice_list

    # Exports the equivalent radius of each grain
    def export_equivalent_radii(self):

        # Get radii
        statistics_list, all_eq_radius_list = [], []
        for slice in self.slice_list:
            eq_radius_list = [math.sqrt(len(grain) / math.pi) for grain in slice]
            statistics_list.append(lognormal.fit_lognormal(eq_radius_list))
            all_eq_radius_list += eq_radius_list
        statistics_list = [lognormal.fit_lognormal(all_eq_radius_list)] + statistics_list # prepend

        # Export to CSV
        headers, statistics = dict_list_to_csv(statistics_list)
        write_to_csv(self.output_csv + "_eq_radius.csv", headers, statistics)

        # Plot distribution
        lognormal.plot_lognormal(statistics_list[0])

# Searches for a keyword in a text file and extracts the contained data
def extract_data(keyword, filename):
    
    # Read the file
    with open(filename, "r") as file:
        data = file.read()

    # Searches for the data encased by the keyword
    start = data.find(keyword)
    data  = data[start:]
    end   = data.find("*")
    data  = data[:end]

    # Process the extracted data and return
    data = data.replace("\n", " ")
    data = data.split(" ")
    data = [d for d in data if d != ""]
    return data

# Main function caller
if __name__ == "__main__":
    main()