"""
 Title:         Tessellator
 Description:   For generating a tessellation using Neper
 Author:        Janzen Choi

"""

# Libraries
import os, time, random
import modules.exporter as exporter
import modules.lognormal as lognormal
import modules.generator as generator
from modules.helper.general import *

# Directories
OUTPUT_DIR      = "results"
AUXILIARY_DIR   = "auxiliary"

# Other Constants
ROUNDING_PLACE  = 5
MAX_SEED_VALUE  = 1000

# The Tessellator Class
class Tessellator:
    
    # Defines the domain to be a square
    def define_domain(self, shape_length, dimensions):

        # Define domain
        self.shape_length = shape_length
        self.dimensions = dimensions
        dimension_args = ",".join([str(shape_length)] * self.dimensions)
        domain = f"\"square({dimension_args})\"" if dimensions == 2 else f"\"cube({dimension_args})\""
        self.shape = f"-dim {self.dimensions} -domain {domain}"
        
        # Define directory name
        curr_time = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        shape = "{}d{}".format(self.dimensions, int(self.shape_length))
        self.output_dir_name = "{}_{}".format(curr_time, shape)

        # Define output files
        self.output_dir     = "{}/{}".format(OUTPUT_DIR, self.output_dir_name)
        self.rve_path       = "{}/{}".format(self.output_dir, "rve")
        self.stats_path     = "{}/{}".format(self.output_dir, "stats")
        self.image_path     = "{}/{}".format(self.output_dir, "img")
        self.image_index    = 1

        # Define auxiliary files
        self.auxiliary_dir      = "{}/{}".format(self.output_dir, AUXILIARY_DIR)
        self.parent_path        = "{}/{}".format(self.auxiliary_dir, "parent")
        self.twin_width_path    = "{}/{}".format(self.auxiliary_dir, "twin_width")
        self.crystal_ori_path   = "{}/{}".format(self.auxiliary_dir, "crystal_ori")

        # Prepares the environment
        safe_mkdir(OUTPUT_DIR)
        safe_mkdir(self.output_dir)
        safe_mkdir(self.auxiliary_dir)

    # Generates the tessellation of the parent grains
    def add_parents(self, eq_radius, sphericity):

        # Redefine statistics
        eq_radius[0], eq_radius[1] = lognormal.get_mean_std(eq_radius[0], eq_radius[1])
        eq_diameter = [2 * radius for radius in eq_radius]
        sphericity[0], sphericity[1] = lognormal.get_mean_std(sphericity[0], sphericity[1])

        # Create and run command
        morpho_diameq = f"diameq:lognormal({eq_diameter[0]},{eq_diameter[1]},from={eq_diameter[2]},to={eq_diameter[3]})"
        morpho_sphericity = f"1-sphericity:lognormal({sphericity[0]},{sphericity[1]},from={sphericity[2]},to={sphericity[3]})"
        seed = random.randint(0, MAX_SEED_VALUE)

        # Tessellate and make a copy
        run(f"neper -T -n from_morpho -morpho \"{morpho_diameq},{morpho_sphericity}\" {self.shape} -oridescriptor euler-bunge -id {seed} -o {self.parent_path}")
        run(f"cp {self.parent_path}.tess {self.rve_path}.tess")

    # Loads in the tessellation of the grains
    def load_parents(self, path):

        # Extract and define shape of tessellation
        general_data = exporter.extract_data("general", path)
        dimensions = int(general_data[1])
        domain_data = exporter.extract_data("domain", path, "*edge")
        shape_length = float(domain_data[13])
        self.define_domain(shape_length, dimensions)

        # Retessellate and make a copy
        run(f"neper -T -loadtess {path} -o {self.parent_path}")
        run(f"cp {self.parent_path}.tess {self.rve_path}.tess")

    # Adds the twins
    def add_twins(self, twin_width):
        diameter_list = self.__extract_stats__(["diameq"])[0]
        distribution = lognormal.Lognormal(twin_width[0], twin_width[1], twin_width[2], twin_width[3])
        width_str = generator.generate_lamellae_widths(diameter_list, distribution, self.shape_length)
        quick_write(self.twin_width_path, width_str)
        morpho  = f"-morpho \"voronoi::lamellar(w=file({self.twin_width_path}),v=crysdir(1,0,0))\""
        optiini = f"-morphooptiini \"file({self.parent_path}.tess)\""
        run(f"neper -T -n {len(diameter_list)}::from_morpho {morpho} {self.shape} {optiini} -oridescriptor euler-bunge -o {self.rve_path}")

    # Generates random crystallographic orientations
    def orient_random(self, has_twins):
        diameter_list = self.__extract_stats__(["diameq"])[0]
        orientations = generator.generate_random_orientations(len(diameter_list), has_twins)
        if has_twins:
            self.__orient_twins__(len(diameter_list), orientations)
        else:
            quick_write(self.crystal_ori_path, "\n".join(orientations))
            run(f"neper -T -loadtess {self.parent_path}.tess -transform \"ori({self.crystal_ori_path},des=euler-bunge)\" -oridescriptor euler-bunge -o {self.rve_path}")

    # Generates crystallographic orientations based on CSL (coincidence cite lattice)
    def orient_csl(self, csl_sigma):
        diameter_list = self.__extract_stats__(["diameq"])[0]
        orientations = generator.generate_csl_orientations(len(diameter_list), csl_sigma)
        self.__orient_twins__(len(diameter_list), orientations)

    # Converts the tessellation into another file
    def export_file(self, conversion_format):
        loadtess = "-loadtess {}.tess".format(self.rve_path)
        format = "-format {}".format(conversion_format)
        run("neper -T {} {} -o {}".format(loadtess, format, self.rve_path))

    # Visualises the tessellation
    def visualise(self):
        tess_options = "-datacellcol ori -datacellcolscheme 'ipf(y)' -cameraangle 14.5 -imagesize 800:800"
        target_path = "{}.tess".format(self.rve_path)
        img_name = "{}_{}".format(self.image_path, self.image_index)
        run("neper -V {} {} -print {}".format(target_path, tess_options, img_name))
        self.image_index += 1

    # Extracts statistics from the generated tessellation
    def get_stats(self, stat_names, include_header = True):
        
        # Extract statistics
        header_list, stat_list = [], []
        for stat_name in stat_names:
            headers, stat = self.__get_stat__(stat_name)
            header_list += headers
            stat_list += stat

        # Process statistics and write as csv
        data = transpose(stat_list)
        data = [header_list] + data if include_header else data
        write_to_csv(f"{self.stats_path}.csv", data)

    # Removes all auxiliary files
    def remove_auxiliary_files(self):
        auxiliary_files = [os.path.join(self.auxiliary_dir, file) for file in os.listdir(self.auxiliary_dir)]
        for file in auxiliary_files:
            os.remove(file)
        os.rmdir(self.auxiliary_dir)

    # Creates a tessellation with twins and orientations defined
    # TODO still broken
    def __orient_twins__(self, num_grains, orientations):
        
        # Write the orientations into individual files, and write an index to those files
        index_str = ""
        for i in range(num_grains):
            ori_path = f"{self.crystal_ori_path}_{i + 1}"
            quick_write(ori_path, orientations[i])
            index_str += f"{i + 1} file({ori_path},des=euler-bunge)\n"
        quick_write(self.crystal_ori_path, index_str)

        # Run the command
        morpho      = f"-morpho \"voronoi::lamellar(w=file({self.twin_width_path}),v=crysdir(1,0,0))\"".format(self.twin_width_path)
        optiini     = f"-morphooptiini \"file({self.parent_path}.tess)\""
        ori         = f"-ori \"random::file({self.crystal_ori_path},des=euler-bunge)\" -oridescriptor euler-bunge"
        run(f"neper -T -n {num_grains}::from_morpho {morpho} {self.shape} {optiini} {ori} -o {self.rve_path}")

    # Extracts the statistics of the grains
    def __extract_stats__(self, requested_stats):

        # Generate stats (assume input is valid)
        stats_str = ",".join(requested_stats)
        run(f"neper -T -loadtess {self.parent_path}.tess -statcell {stats_str} -o {self.parent_path}")
        
        # Read stats
        with open(self.parent_path + ".stcell", "r") as file:
            lines = file.readlines()
            values = [line.replace("\n", "").split(" ") for line in lines]

        # Extract and return float casted stats
        data_list = []
        for i in range(len(requested_stats)):
            data = [float(value[i]) for value in values]
            data_list.append(data)
        return data_list
    
    # Extracts the orientations of the grains
    def __extract_orientations__(self):
        run(f"neper -T -loadtess {self.parent_path}.tess -statcell euler-bunge -o {self.parent_path}")
        with open(self.parent_path + ".stcell", "r") as file:
            lines = file.readlines()
            values = [line.replace("\n", "").split(" ") for line in lines]
        orientations = [[float(value[i]) for value in values] for i in range(3)]
        return orientations
    
    # Maps and returns the requested stats
    # TODO make it work with twins 
    def __get_stat__(self, stat_name):

        # For id
        if stat_name == "id":
            stat = self.__extract_stats__(["diameq"])
            return ["id"], [range(1,len(stat[0]) + 1)]

        # For orientation
        if stat_name == "orientation":
            orientations = self.__extract_orientations__()
            return ["phi_1", "Phi", "phi_2"], orientations
        
        # For Neper supported stats
        mapped_name = stat_name
        if mapped_name in ["area", "vol", "diameq", "radeq", "sphericity", "convexity", "npolynb_samedomain"]:
            stat = self.__extract_stats__([mapped_name])
            return [mapped_name], stat
