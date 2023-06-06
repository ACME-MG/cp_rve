"""
 Title:         Material
 Description:   For creating material files
 Author:        Janzen Choi

"""

# Libraries
import importlib, os

# Constants
PATH_TO_MATERIALS = "modules/materials"
EXCLUSION_LIST = ["__material__", "__pycache__"]

# Material Class
class MaterialTemplate:

    # Sets values of internal variables
    def set_vals(self, name:str, output_path:str) -> None:
        self.name = name
        self.output_path = output_path

    # Gets the name
    def get_name(self) -> str:
        return self.name
    
    # Creates the file content (placeholder)
    def get_content(self) -> str:
        raise NotImplementedError
    
    # Creates the material file
    def create_file(self, params:list) -> None:
        content = self.get_content(*params)
        with open(self.output_path, "w+") as file:
            file.write(content)

# Creates a material file
def create_material(material_name:str, params:list, material_path:str) -> None:

    # Get available materials in current folder
    files = os.listdir(PATH_TO_MATERIALS)
    files = [file.replace(".py", "") for file in files]
    files = [file for file in files if not file in EXCLUSION_LIST]
    
    # Raise error if material name not in available materials
    if not material_name in files:
        raise NotImplementedError(f"The material '{material_name}' has not been implemented")

    # Import and prepare material
    module = f"{PATH_TO_MATERIALS}/{material_name}".replace("/", ".")
    material_file = importlib.import_module(module)
    material = material_file.Material()
    material.set_vals(material_name, material_path)
    material.create_file(params)