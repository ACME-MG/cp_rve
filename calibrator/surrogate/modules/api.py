"""
 Title:         API for Surrogate Modelling
 Description:   For developing surrogate models
 Author:        Janzen Choi
 
"""

# Libraries
import time, random
import numpy as np
from modules.models.__model_factory__ import get_model
from modules.sampler import Sampler
from modules.surrogate import Surrogate
from modules.simplifier import Simplifier
from modules.mapper import MultiMapper

# Helper libraries
import sys; sys.path.append("../../__common__")
from progressor import Progressor
from plotter import Plotter
from general import safe_mkdir

# I/O directories
INPUT_DIR   = "./input"
RESULTS_DIR = "./results"

# API Class
class API:

    # Constructor
    def __init__(self, fancy=False, title="", verbose=False):
        
        # Initialise
        self.prog = Progressor(fancy, title, verbose)
        self.simplifier = Simplifier(10, 100, 9)
        self.plotter = Plotter()
        self.plot_count = 1

        # Set up environment
        title = "" if title == "" else f" ({title})"
        self.output_dir  = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        self.output_path = f"{RESULTS_DIR}/{self.output_dir}{title}"
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_path)

    # Defines the model, surrogate model, and mappers
    def define_sm(self, model_name=""):
        self.prog.add(f"Defining the surrogate model for {model_name}")

        # Define model
        self.model = get_model(model_name)
        self.l_bounds = self.model.get_param_lower_bounds()
        self.u_bounds = self.model.get_param_upper_bounds()
        
        # Define surrogate model and mapper
        self.surrogate = Surrogate(len(self.l_bounds), len(self.simplifier.l_bounds))
        self.param_mapper = MultiMapper(self.l_bounds, self.u_bounds)
        self.curve_mapper = MultiMapper(self.simplifier.l_bounds, self.simplifier.u_bounds)

    # Samples the parameter space using the CCD strategy
    def sample_CCD(self, axial=0.5):
        self.prog.add(f"Sampling the parameter space with CCD")
        smp = Sampler(self.l_bounds, self.u_bounds)
        params_list = smp.sample_CCD(axial)
        self.__prepare_sample__(params_list)

    # Samples the parameter space randomly
    def sample_random(self, size=10):
        self.prog.add(f"Sampling the parameter space randomly")
        params_list = [[random.uniform(self.l_bounds[i], self.u_bounds[i]) for i in range(len(self.l_bounds))] for _ in range(size)]
        self.__prepare_sample__(params_list)

    # Trains the surrogate model
    def train(self, epochs=100, batch_size=32):
        self.prog.add(f"Training the surrogate model")
        self.surrogate.fit(self.sm_inputs, self.sm_outputs, epochs, batch_size)
    
    # Predicts a curve using the trained surrogate model
    def assess(self, trials=1):
        self.prog.add(f"Assessing the surrogate model {trials} time(s)")

        # Iterate through trials
        for i in range(trials):

            # Uniformly generate random parameters
            random_params = [random.uniform(self.l_bounds[i], self.u_bounds[i]) for i in range(len(self.l_bounds))]
            mapped_params = self.param_mapper.map(random_params)

            # Gets the actual curve
            actual_curve = self.model.get_curve(*random_params)
            actual_curve = {"x": actual_curve["x"][-1], "y": actual_curve["y"][-1]}
            
            # Request the surrogate model to predict the curve
            mapped_simplified_curve = self.surrogate.predict(mapped_params)
            simplified_curve = self.curve_mapper.unmap(mapped_simplified_curve[0])
            predicted_curve = self.simplifier.restore_curve(simplified_curve)

            # Plot the results
            plt = Plotter(self.output_path, f"plot_{self.plot_count}")
            self.plot_count += 1
            plt.scat_plot([predicted_curve], "r")
            plt.scat_plot([actual_curve])
            plt.define_legend(["Predicted", "Actual"])
            plt.save_plot()
            plt.clear()

            # Print out progress
            print(f"  {i+1}\tTested - {random_params}")

    # Prepare sampled parameters for the surrogate model
    def __prepare_sample__(self, params_list):
        
        # Initialise
        self.sm_inputs = []
        self.sm_outputs = []

        # Get curve for each parameter
        for i in range(len(params_list)):
            curve = self.model.get_curve(*params_list[i])

            # Check curve and print progress
            if curve["x"] == [] or curve["y"] == [] or np.nan in curve["y"]:
                print(f"  {i+1})\tFAILURE - {params_list[i]}")
                continue
            print(f"  {i+1})\tSUCCESS - {params_list[i]}")

            # Map and append parameters
            mapped_params = self.param_mapper.map(params_list[i])
            self.sm_inputs.append(mapped_params)

            # Simplify, map, and append curve
            simplified_curve = self.simplifier.simplify_curve(curve)
            mapped_curve = self.curve_mapper.map(simplified_curve)
            self.sm_outputs.append(mapped_curve)
