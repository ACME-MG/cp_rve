"""
 Title:         Simulator API
 Description:   For simulating creep behaviour
 Author:        Janzen Choi

"""

# Libraries
import  subprocess, os, csv, sys
import modules.material as material
import modules.simulation as simulation
import modules.visualiser as visualiser

# Helper libraries
sys.path.append("../__common__")
from api_template import APITemplate

# Default params
MATERIAL_PARAMS = [12, 66.67, 40, 9.55e-8, 12]
SIMULATION_PARAMS = [4e-5, 5.9e-2, 0.9]

# API Class
class API(APITemplate):

    # Constructor
    def __init__(self, title="", display=2):
        super().__init__(title, display)
        self.material_file   = "material.xml"
        self.simulation_file = "simulation.i"
        self.material_path   = self.get_output(self.material_file)
        self.simulation_path = self.get_output(self.simulation_file)

    # Defines the mesh
    def define_mesh(self, mesh_file, orientation_file):
        self.add("Defining the mesh")
        self.mesh_path = self.get_input(mesh_file)
        self.orientation_path = self.get_input(orientation_file)
        with open(self.orientation_path, newline = "") as file:
            self.num_cells = len([row for row in csv.reader(file, delimiter=" ")])

    # Defines the parameters
    def define_params(self, mat_params=MATERIAL_PARAMS, sim_params=SIMULATION_PARAMS):
        self.add("Defining the material / simulation parameters")
        material.define_material(*mat_params, self.material_path)
        simulation.define_simulation(*sim_params, self.num_cells, f"../../{self.mesh_path}", f"../../{self.orientation_path}", self.material_file, self.simulation_path)

    # Change to workspace directory, and summons DEER to simulate
    def simulate(self, deer_path, num_processors):
        self.add("Commencing the simulation")
        os.chdir("{}/{}".format(os.getcwd(), self.output_path))
        command = f"mpiexec -np {num_processors} {deer_path} -i {self.simulation_file}"
        subprocess.run([command], shell = True, check = True)
    
    # Visualises the reuslts
    def visualise(self, input_files=[]):
        self.add("Visualising the results")
        output_path = self.get_output("results.png")
        visualiser.visualise(self.input_path, input_files, output_path)