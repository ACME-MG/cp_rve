"""
 Title:         API Template
 Description:   For creating API classes
 Author:        Janzen Choi
 
"""

# Libraries
import time, re
from progressor import Progressor
from general import safe_mkdir

# I/O directories
INPUT_DIR   = "./input"
RESULTS_DIR = "./results"

# API Template Class
class APITemplate:

    # Constructor
    def __init__(self, title="", display=2):
        
        # Prepare progressor
        title = "" if title == "" else f"_{title}"
        title = re.sub(r"[^a-zA-Z0-9_]", "", title.replace(" ", "_"))
        self.prog = Progressor(title, display)
        
        # Define paths
        self.input_path  = INPUT_DIR
        self.output_dir  = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        self.output_path = f"{RESULTS_DIR}/{self.output_dir}{title}"
        
        # Create directories
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_path)

    # Adds to the progressor
    def add(self, message):
        self.prog.add(message)

    # Gets the input path
    def get_input(self, path):
        return f"{INPUT_DIR}/{path}"

    # Gets the output path
    def get_output(self, path):
        return f"{self.output_path}/{path}"