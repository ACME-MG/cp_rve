"""
 Title:         Optimiser API
 Description:   API for calibrating creep models
 Author:        Janzen Choi

"""

# Libraries
import time
from modules.data.reader import get_exp_data
from modules.errors._error_factory import get_error_list
from modules.errors._error import get_bfd
from modules.models.__model_factory__ import get_model
from modules.moga.objective import Objective
from modules.moga.problem import Problem
from modules.moga.moga import MOGA
from modules.recorder import Recorder

# Helper Libraries
import sys; sys.path.append("../../__common__")
from progressor import Progressor
from plotter import Plotter
from general import safe_mkdir

# Input / Output
INPUT_DIR   = "./"
INPUT_FILE  = "alloy_617"
RESULTS_DIR = "./results"
CSV_FILE    = "moga"

# Constants
DEFAULT_INTERVAL    = 10
DEFAULT_POPULATION  = 10
DEFAULT_NUM_GENS    = 10000
DEFAULT_INIT_POP    = 400
DEFAULT_OFFSPRING   = 400
DEFAULT_CROSSOVER   = 0.65
DEFAULT_MUTATION    = 0.35

# API Class
class API:

    # Constructor
    def __init__(self, fancy=False, title="", verbose=False):
        
        # Initialise progress visualiser
        self.prog = Progressor(fancy, title, verbose)

        # Initialise paths
        self.output_dir  = time.strftime("%y%m%d%H%M%S", time.localtime(time.time()))
        self.output_dir  = self.output_dir if title == "" else f"{self.output_dir} ({title})"
        self.output_path = "{}/{}".format(RESULTS_DIR, self.output_dir)
        self.csv_path    = "{}/{}".format(self.output_path, CSV_FILE)

        # Set up environment
        safe_mkdir(RESULTS_DIR)
        safe_mkdir(self.output_path)

    # Reads in experimental data
    def read_data(self, test_names):
        self.prog.add("Reading in experimental data")
        self.test_names = test_names
        self.exp_curves = get_exp_data(test_names)

    # Removes data past the minimum rate value
    def remove_damage(self):
        self.prog.add("Removing creep damage")
        for i in range(len(self.test_names)):
            exp_y_fd = get_bfd(self.exp_curves[i]["x"], self.exp_curves[i]["y"])
            min_index = exp_y_fd.index(min(exp_y_fd))
            self.exp_curves[i]["x"] = [self.exp_curves[i]["x"][j] for j in range(min_index)]
            self.exp_curves[i]["y"] = [self.exp_curves[i]["y"][j] for j in range(min_index)]

    # Initialising the model
    def define_model(self, model_name):
        self.prog.add("Defining the model")
        self.model = get_model(model_name, self.exp_curves)
    
    # Defining the errors
    def define_errors(self, error_names):
        self.prog.add("Defining the errors to minimise")
        self.error_list = get_error_list(error_names, self.exp_curves)

    # Prepares the optimisation objective
    def prepare_objective(self):
        self.prog.add("Preparing the optimisation objective")
        self.objective = Objective(self.model, self.error_list)

    # Prepares the recorder
    def prepare_recorder(self, interval = DEFAULT_INTERVAL, population = DEFAULT_POPULATION):
        self.prog.add("Preparing the results recorder")
        self.recorder = Recorder(self.objective, self.exp_curves, self.csv_path, interval, population)

    # Conducts the optimisation
    def optimise(self, num_gens = DEFAULT_NUM_GENS, init_pop = DEFAULT_INIT_POP, offspring = DEFAULT_OFFSPRING, crossover = DEFAULT_CROSSOVER, mutation = DEFAULT_MUTATION):
        self.prog.add("Optimising the parameters of the model")
        self.recorder.define_hyperparameters(num_gens, init_pop, offspring, crossover, mutation)
        problem = Problem(self.objective, self.recorder)
        moga = MOGA(problem, num_gens, init_pop, offspring, crossover, mutation)
        print("\n=============================== Optimising ===============================\n")
        moga.optimise()

    # Plots the results
    def plot_results(self, params):
        self.prog.add("Plotting the results")
        plotter = Plotter(self.output_path)
        plotter.scat_plot(self.exp_curves)
        prd_curves = self.model.get_prd_curves(*params)
        plotter.line_plot(prd_curves)
        plotter.save_plot()

    # Returns the error values of the objective functions
    def get_errors(self, params):
        self.prog.add("Obtaining error values")
        prd_curves  = self.model.get_prd_curves(*params)
        objective   = Objective(self.model, self.error_list)
        error_names = objective.get_error_names()
        error_values = objective.get_error_values(prd_curves)
        with open(f"{self.output_path}/errors.csv", "w+") as file:
            for i in range(len(error_names)):
                file.write(f"{error_names[i]},{error_values[i]}\n")
            file.write(f"err_sqr_sum,{sum([err**2 for err in error_values])}")
