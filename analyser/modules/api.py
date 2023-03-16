"""
 Title:         Analyser API
 Description:   For analysing the results of simulations
 Author:        Janzen Choi

"""

# Libraries
import sys
import modules.analyser as analyser

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
        self.input_tests = []

    # Adds an input file
    def add_input(self, input_file):
        self.add(f"Adding {input_file} to the input")
        self.input_tests.append({"file": input_file})
    
    # Summarises the results
    def plot_curves(self, output_file="results", directions=["x", "y", "z"]):
        self.add(f"Plotting curves for {len(self.input_tests)} simulation{'s' if len(self.input_tests) > 1 else ''}")
        output_path = self.get_output(f"{output_file}.png")
        analyser.plot_curves(self.input_path, output_path, self.input_tests, directions)