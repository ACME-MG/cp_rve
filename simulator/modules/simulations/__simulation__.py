"""
 Title:         Simulation
 Description:   For creating simulation input files
 Author:        Janzen Choi

"""

# Libraries
import importlib, os

# Constants
PATH_TO_SIMULATIONS = "modules/simulations"
EXCLUSION_LIST = ["__simulation__", "__pycache__"]

# Simulation Template Class
class SimulationTemplate:

    # Sets values of internal variables
    def set_vals(self, name:str, num_grains:int, mesh_path:str, orientation_path:str, material_name:str, material_file:str, output_path:str) -> None:
        self.name             = name
        self.num_grains       = num_grains
        self.mesh_path        = mesh_path
        self.orientation_path = orientation_path
        self.material_name    = material_name
        self.material_file    = material_file
        self.output_path      = output_path

    # Gets the name
    def get_name(self) -> str:
        return self.name
    
    # Creates the file content (placeholder)
    def get_content(self) -> str:
        raise NotImplementedError
    
    # Creates the simulation file
    def create_file(self, params:list) -> None:
        content = self.get_content(*params)
        with open(self.output_path, "w+") as file:
            file.write(content)

# Creates a simulation file
def create_simulation(simulation_name:str, params:list, num_grains:int, mesh_path:str, orientation_path:str, material_name:str, material_file:str, output_path:str) -> None:

    # Get available simulations in current folder
    files = os.listdir(PATH_TO_SIMULATIONS)
    files = [file.replace(".py", "") for file in files]
    files = [file for file in files if not file in EXCLUSION_LIST]
    
    # Raise error if simulation name not in available simulations
    if not simulation_name in files:
        raise NotImplementedError(f"The simulation '{simulation_name}' has not been implemented")

    # Import and prepare simulation
    module = f"{PATH_TO_SIMULATIONS}/{simulation_name}".replace("/", ".")
    simulation_file = importlib.import_module(module)
    simulation = simulation_file.Simulation()
    simulation.set_vals(simulation_name, num_grains, mesh_path, orientation_path, material_name, material_file, output_path)
    simulation.create_file(params)