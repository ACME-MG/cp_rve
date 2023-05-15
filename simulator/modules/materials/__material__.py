"""
 Title:         Material
 Description:   For creating material files
 Author:        Janzen Choi

"""

# Material Class
class Material:

    # Constructor
    def __init__(self, name:str) -> None:
        self.name = name

    # Gets the name
    def get_name(self) -> str:
        return self.name
    
    # Creates the file content (placeholder)
    def get_content(self) -> str:
        raise NotImplementedError
    
    # Creates the material file
    def create_file(self, params:list[str], num_grains:int, mesh_file:str, orientation_path:str, material_file:str, output_path:str) -> None:
        content = self.get_content(params, num_grains, mesh_file, orientation_path, material_file)
        with open(output_path, "w+") as file:
            file.write(content)