"""
 Title:         Simulator
 Description:   For simulating creep behaviour
 Author:        Janzen Choi

"""

# Libraries
import time, subprocess
import modules.material as material
import modules.simulation as simulation
import modules.helper.progressor as progressor
from modules.helper.general import *

# Directories
INPUT_DIR   = "input"
RESULTS_DIR = "results"

# File Paths
MATERIAL_FILE       = "material.xml"
SIMULATION_FILE     = "simulation.i"

# Default Parameters
DEFAULT_MATERIAL_PARAMS     = [12, 66.67, 40, 9.55e-8, 12]
DEFAULT_SIMULATION_PARAMS   = [4e-5, 5.9e-2, 0.9]

# MPI Constants
TASKS_PER_NODE = 8

# Simulator Class
class Simulator:

    # Constructor
    def __init__(self, deer_path, num_processors, mesh_file, orientation_file, verbose):

        # Initialise
        self.prog           = progressor.Progressor(verbose)
        self.deer_path      = deer_path
        self.num_processors = num_processors
        self.mesh_file      = mesh_file

        # Define directories
        start_time          = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        self.output_dir     = f"{start_time}_{num_processors}"
        self.input_path     = INPUT_DIR
        self.output_path    = "{}/{}".format(RESULTS_DIR, self.output_dir)

        # Define file paths
        self.mesh_file_path     = "{}/{}".format(self.input_path, mesh_file)
        self.orientation_path   = "{}/{}".format(self.input_path, orientation_file)
        self.material_path      = "{}/{}".format(self.output_path, MATERIAL_FILE)
        self.simulation_path    = "{}/{}".format(self.output_path, SIMULATION_FILE)

        # Set up environment
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_path)

    # Creates the material file
    def define_material(self, params = DEFAULT_MATERIAL_PARAMS):
        self.prog.queue(
            function    = material.define_material,
            arguments   = [*params, self.material_path],
            message     = "Defining the material XML file",
        )

    # Creates the simulation file
    def define_simulation(self, params = DEFAULT_SIMULATION_PARAMS):

        # Determine number of cells
        file = open(self.orientation_path, newline = "")
        all_rows = [row for row in csv.reader(file, delimiter = " ")]
        num_cells = len(all_rows)
        file.close()

        # Define relative paths
        relative_mesh_path = "../../" + self.mesh_file_path
        relative_orientation_path = "../../" + self.orientation_path

        # Queue defining simulation
        self.prog.queue(
            function    = simulation.define_simulation,
            arguments   = [*params, num_cells, relative_mesh_path, relative_orientation_path, MATERIAL_FILE, self.simulation_path],
            message     = "Defining the simulation input file",
        )
    
    # Commences the simulation
    def commence(self):
        self.prog.queue(
            function    = self.__commence__,
            message     = "Commencing the simulation",
        )
        self.prog.start(self.output_dir)

    # Commences the simulation
    def __commence__(self):
        
        # Change to workspace directory
        os.chdir("{}/{}".format(os.getcwd(), self.output_path))

        # Calls the psculpt executable to sculpt everything
        # command = "mpiexec -np {num_processors} {deer_path} -i {input_path} --distributed-mesh".format(
        command = "mpiexec -np {num_processors} {deer_path} -i {input_path}".format(
            deer_path       = self.deer_path,
            num_processors  = self.num_processors,
            tasks_per_node  = TASKS_PER_NODE,
            input_path      = SIMULATION_FILE,
        )
        subprocess.run([command], shell = True, check = True)