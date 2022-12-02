"""
 Title:         Hex Mesher
 Description:   For creating hexahedral meshes from a collection of STL files
 Author:        Janzen Choi

"""

# Libraries
import os, subprocess, time
import modules.sculpt_diatom as sculpt_diatom
import modules.sculpt_input as sculpt_input
import modules.helper.progressor as progressor
from modules.helper.general import *

# Paths
RESULTS_DIR     = "results"
INPUT_DIR       = "input"

# The Mesher Class
class Mesher:

    # Constructor
    def __init__(self, psculpt_path, epu_path, num_processors, num_cells, volume_length, verbose):

        # Initialise progressor
        self.prog = progressor.Progressor(verbose)

        # Initialise input / output directories
        self.output_dir     = "{}_{}_{}".format(time.strftime("%y%m%d%H%M%S", time.localtime(time.time())), volume_length, num_cells)
        self.input_path     = INPUT_DIR
        self.output_path    = "{}/{}".format(RESULTS_DIR, self.output_dir)
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_path)

        # Initialise variables
        self.psculpt_path   = psculpt_path
        self.epu_path       = epu_path
        self.num_processors = num_processors
        self.num_cells      = num_cells
        self.volume_length  = volume_length

    # Writes diatom file
    def write_diatom_file(self):
        self.prog.queue(
            function    = sculpt_diatom.write_diatom_file,
            arguments   = [self.input_path, self.output_path],
            message     = "Writing sculpt diatom file",
        )

    # Writes the input file
    def write_input_file(self):
        self.prog.queue(
            function    = sculpt_input.write_input_file,
            arguments   = [self.num_cells, self.volume_length, self.output_path],
            message     = "Writing sculpt input file",
        )

    # Commence the sculpt process
    def sculpt_hex_mesh(self):
        self.prog.queue(
            function    = self.__sculpt_hex_mesh__,
            message     = "Sculpting the hexahedral mesh",
        )

    # Commences the sculpting process
    def __sculpt_hex_mesh__(self):

        # Change to workspace directory
        os.chdir("{}/{}".format(os.getcwd(), self.output_path))

        # Calls the psculpt executable to sculpt everything
        command = "mpiexec -n {num_processors} {psculpt_path} -j {num_processors} -i {input_path}".format(
            psculpt_path    = self.psculpt_path,
            num_processors  = self.num_processors,
            input_path      = sculpt_input.INPUT_FILE,
        )
        subprocess.run([command], shell = True, check = True)

        # If there are multiple processors, then combine
        if self.num_processors > 1:
            command = "mpiexec -n 1 {epu_path} -p {num_processors} {exodus_file}".format(
                epu_path        = self.epu_path,
                num_processors  = self.num_processors,
                exodus_file     = sculpt_input.EXODUS_FILE
            )
            subprocess.run([command], shell = True, check = True)
        
        # If there is one processor, then just rename
        else:
            os.rename(sculpt_input.EXODUS_FILE + ".e.1.0", sculpt_input.EXODUS_FILE + ".e")

    # Start the mesh
    def commence_mesh(self):
        self.prog.start(self.output_dir)