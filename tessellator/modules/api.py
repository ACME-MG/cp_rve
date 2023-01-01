"""
 Title:         Tessellator API
 Description:   API for tessellation program
 Author:        Janzen Choi

"""

# Libraries
import time, subprocess, random, sys
import modules.lognormal as lognormal
import modules.extractor as extractor
import modules.orientation as orientation

# Helper libraries
sys.path.append("../__common__")
from progressor import Progressor
from general import safe_mkdir, write_to_csv, transpose

# I/O Directories
INPUT_DIR   = "./input"
RESULTS_DIR = "./results"

# API Class
class API:

    # Constructor
    def __init__(self, fancy=False, title="", verbose=False):
        
        # Initialise
        title = title.replace(" ", "")
        suffix = f"_{title}" if title != "" else title
        self.prog = Progressor(fancy, title, verbose)

        # Prepares environment
        self.output_dir     = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        self.output_path    = f"{RESULTS_DIR}/{self.output_dir}{suffix}"
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_path)

        # Define output
        self.rve_path   = "{}/{}".format(self.output_path, "rve")
        self.stats_path = "{}/{}".format(self.output_path, "stats")
        self.image_path = "{}/{}".format(self.output_path, "img")
        
    # Defines the domain
    def define_domain(self, length, dimensions):
        self.prog.add("Defining the domain of the tessellation")
        dimension_args = ",".join([str(length)] * dimensions)
        domain = f"\"square({dimension_args})\"" if dimensions == 2 else f"\"cube({dimension_args})\""
        self.shape = f"-dim {dimensions} -domain {domain}"

    # Defines the equivalent radius of the parent grains
    def define_radius(self, mu, sigma, min, max):
        self.prog.add("Defining the equivalent radius of the grains")
        mean, std = lognormal.get_mean_std(mu, sigma)
        self.eq_diameter = {"mean": 2*mean, "std": 2*std, "min": 2*min, "max": 2*max}
    
    # Defines the sphericity of the parent grains
    def define_sphericity(self, mu, sigma, min, max):
        self.prog.add("Defining the sphericity of the grains")
        mean, std = lognormal.get_mean_std(mu, sigma)
        self.sphericity = {"mean": mean, "std": std, "min": min, "max": max}

    # Generates the tessellation of the parent grains
    def tessellate(self, seed=None):
        self.prog.add("Generating the tessellation")
        morpho_diameq = f"diameq:lognormal({self.eq_diameter['mean']},{self.eq_diameter['std']},from={self.eq_diameter['min']},to={self.eq_diameter['max']})"
        morpho_sphericity = f"1-sphericity:lognormal({self.sphericity['mean']},{self.sphericity['std']},from={self.sphericity['min']},to={self.sphericity['max']})"
        seed = random.randint(0, 1000) if seed == None else seed
        run(f"neper -T -n from_morpho -morpho \"{morpho_diameq},{morpho_sphericity}\" {self.shape} -oridescriptor euler-bunge -id {seed} -o {self.rve_path}.tess")

    # Loads a tessellation from the input directory
    def load_tessellation(self, tessellation_file):
        self.prog.add(f"Loading in tessellation '{tessellation_file}'")
        tessellation_path   = f"{INPUT_DIR}/{tessellation_file}"
        dimensions          = int(extractor.extract_data("general", tessellation_path)[1])
        shape_length        = float(extractor.extract_data("domain", tessellation_path, "*edge")[13])
        self.define_domain(shape_length, dimensions)
        run(f"neper -T -loadtess {tessellation_path} -o {self.rve_path}.tess")

    # Visualises the tessellation
    def visualise(self):
        self.prog.add("Visualising the tessellation")
        tess_options = "-datacellcol ori -datacellcolscheme 'ipf(y)' -cameraangle 14.5 -imagesize 800:800"
        target_path = "{}.tess".format(self.rve_path)
        run("neper -V {} {} -print {}".format(target_path, tess_options, self.image_path))
    
    # Generates (random) crystallographic orientations to the grains
    def orient_random(self):
        self.prog.add("Generating random orientations")
        num_grains = len(self.__get_stat__("diameq"))
        orientation_list = [orientation.rad_to_deg(orientation.random_euler()) for _ in range(num_grains)]
        orientation_list = transpose(orientation_list)
        self.orientation_dict = {"phi_1": orientation_list[0], "Phi": orientation_list[1], "phi_2": orientation_list[2]}

    # Exports statistics from the generated tessellation
    def export(self, statistic_list):
        self.prog.add("Exporting statistics from tessellation")
        data_list = []
        for statistic in statistic_list:
            if statistic in ["phi_1", "Phi", "phi_2"]:
                data_list.append(self.orientation_dict[statistic])
            else:
                data_list.append(self.__get_stat__(statistic))
        data = transpose(data_list)
        write_to_csv(f"{self.stats_path}.csv", data)

    # Extracts a statistic of the grains
    def __get_stat__(self, requested_stats):
        run(f"neper -T -loadtess {self.rve_path}.tess -statcell {requested_stats} -o {self.rve_path}.tess")
        with open(f"{self.rve_path}.stcell", "r") as file:
            data = [float(line.replace("\n", "")) for line in file.readlines()]
        return data

# Runs a command using a single thread
def run(command, shell=True, check=True):
    subprocess.run([f"OMP_NUM_THREADS=1 {command}"], shell=shell, check=check)