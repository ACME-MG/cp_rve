"""
 Title:         Simulator API
 Description:   For simulating creep behaviour
 Author:        Janzen Choi

"""

# Libraries
import  subprocess, os, csv, sys
import modules.material as material
import modules.simulations.__simulation__ as simulation

# Helper libraries
sys.path.append("../__common__")
from api_template import APITemplate

# Default params
MATERIAL_PARAMS = [12, 66.67, 40, 9.55e-8, 12]
SIMULATION_PARAMS = [4e-5, 5.9e-2, 0.9]

# API Class
class API(APITemplate):

    # Constructor
    def __init__(self, title:str="", display:int=2):
        super().__init__(title, display)
        self.material_name   = "material"
        self.material_file   = "material.xml"
        self.simulation_file = "simulation.i"
        self.material_path   = self.get_output(self.material_file)
        self.simulation_path = self.get_output(self.simulation_file)

    # Defines the mesh
    def define_mesh(self, mesh_file:str, orientation_file:str):
        self.add("Defining the mesh")
        self.mesh_path = self.get_input(mesh_file)
        self.orientation_path = self.get_input(orientation_file)
        with open(self.orientation_path, newline = "") as file:
            self.num_grains = len([row for row in csv.reader(file, delimiter=" ")])

    # Defines the parameters
    def define_params(self, material_params:list[float]=MATERIAL_PARAMS, simulation_params:list[float]=SIMULATION_PARAMS):
        self.add("Defining the parameters")
        self.material_params = material_params
        self.simulation_params = simulation_params

    # Defines the material
    def define_material(self, material_name:str):
        self.add(f"Defining the material ({material_name})")
        material.define_material(*self.material_params, self.material_path)
    
    # Defines the simulation
    def define_simulation(self, simulation_name:str):
        self.add(f"Defining the simulation ({simulation_name})")
        simulation.create_simulation(simulation_name, self.simulation_params, self.num_grains,
                                     f"../../{self.mesh_path}", f"../../{self.orientation_path}",
                                     self.material_name, self.material_file, self.simulation_path)

    # Change to workspace directory, and summons DEER to simulate
    def simulate(self, deer_path:str, num_processors:int):
        self.add("Commencing the simulation")
        os.chdir("{}/{}".format(os.getcwd(), self.output_path))
        command = f"mpiexec -np {num_processors} {deer_path} -i {self.simulation_file}"
        subprocess.run([command], shell = True, check = True)
