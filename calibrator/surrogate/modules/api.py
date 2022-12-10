"""
 Title:         API for Surrogate Modelling
 Description:   For developing surrogate models
 Author:        Janzen Choi
 
"""

# Libraries
import time, random
from modules.models.__model_factory__ import get_model
from modules.sampler import Sampler
from modules.surrogate import Surrogate
from modules.polyfier import Polyfier

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
        self.poly = Polyfier()

        # Set up environment
        title = "" if title == "" else f" ({title})"
        self.output_dir  = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        self.output_path = f"{RESULTS_DIR}/{self.output_dir}{title}"
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_path)

    # Defines the model
    def define_model(self, model_name=""):
        self.prog.add(f"Defining the {model_name} model")
        self.model = get_model(model_name)
        self.l_bounds = self.model.get_param_lower_bounds()
        self.u_bounds = self.model.get_param_upper_bounds()

    # Samples the parameter space using the CCD strategy
    def sample_CCD(self):
        self.prog.add(f"Sampling the parameter space with CCD")
        smp = Sampler(self.l_bounds, self.u_bounds)
        self.param_list = smp.sample_CCD()

    # Commence training the surrogate model
    def train(self):
        self.prog.add("Training the surrogate model")
        
        # Initialise
        self.sm = Surrogate()
        curve_list = []

        # Gather curves
        for i in range(len(self.param_list)):
            print(f"    Training ({i+1}/{len(self.param_list)})")
            curve = self.model.get_curve(*self.param_list[i])
            curve = self.poly.compress_curve(curve)
            curve_list.append(curve["y"])
        
        # Start training
        self.sm.train_sm(self.param_list, curve_list)

    # Assess the surrogate model
    def assess_random(self, trials=1):
        self.prog.add(f"Assessing the surrogate model {trials} times")

        # Uniformly generate a bunch of random parameters
        actual_list, predicted_list = [], []
        for i in range(trials):
            print(f"    Testing ({i+1}/{trials})")

            # Get random parameters and actual curve
            random_params = [random.uniform(self.l_bounds[i], self.u_bounds[i]) for i in range(len(self.l_bounds))]
            actual = self.model.get_curve(*random_params)
            actual = self.poly.compress_curve(actual)

            # Get predicted curve
            predicted = {
                "x": self.poly.get_x_list(),
                "y": self.sm.predict([random_params])
            }

            # Append to list of curves
            actual_list.append(actual)
            predicted_list.append(predicted)
        
        # Plot results
        plt = Plotter(self.output_path, "plot")
        plt.prd_plot(actual_list)
        plt.exp_plot(predicted_list)
        plt.save_plot()
    
    # Saves the trained model (via pickling)
    def save_sm(self, model_path):
        self.save_sm(model_path)

    # Loads the trained model (via pickling)
    def load_sm(self, model_path):
        self.sm = Surrogate()
        self.sm = self.sm.load_sm(model_path)
