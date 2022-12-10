"""
 Title:         Multi-Objective Genetic Algorithm
 Description:   For parameter optimisation
 Author:        Janzen Choi

"""

# Libraries
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation, get_termination
from pymoo.optimize import minimize

# The Multi-Objective Genetic Algorithm (MOGA) class
class MOGA:
    
    # Constructor
    def __init__(self, problem, num_gens, init_pop, offspring, crossover, mutation):
        
        # Initialise
        self.problem    = problem
        self.num_gens   = num_gens
        self.init_pop   = init_pop
        self.offspring  = offspring
        self.crossover  = crossover
        self.mutation   = mutation

        # Define algorithm
        self.term = get_termination("n_gen", num_gens)
        self.algo = NSGA2(
            pop_size     = init_pop,
            n_offsprings = offspring,
            sampling     = get_sampling("real_lhs"), # latin hypercube sampling
            crossover    = get_crossover("real_sbx", prob = crossover, eta=10), # simulated binary
            mutation     = get_mutation("real_pm", prob = mutation, eta=15), # polynomial mutation
            eliminate_duplicates = True
        )

    # Runs the genetic optimisation
    def optimise(self):
        params_list = minimize(self.problem, self.algo, self.term, verbose=False, seed=None).X
        return params_list