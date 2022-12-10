"""
 Title:         Recorder
 Description:   For recording results periodically
 Author:        Janzen Choi

"""

# Libraries
import time, math
import pandas as pd
from modules.moga.objective import BIG_VALUE

# Constants
CURVE_DENSITY = 100

# The Recorder class
class Recorder:

    # Constructor
    def __init__(self, objective, exp_curves, path, interval, population):

        # Initialise
        self.model          = objective.get_model()
        self.error_names    = objective.get_error_names()
        self.exp_curves     = exp_curves
        self.path           = path
        self.interval       = interval
        self.population     = population

        # Prepare experimental data
        exp_x_data = [get_thinned_list(exp_curve["x"]) for exp_curve in self.exp_curves]
        exp_y_data = [get_thinned_list(exp_curve["y"]) for exp_curve in self.exp_curves]
        self.exp_x_flat = [exp_x for exp_x_list in exp_x_data for exp_x in exp_x_list] # flatten
        self.exp_y_flat = [exp_y for exp_y_list in exp_y_data for exp_y in exp_y_list] # flatten

        # Track optimisation progress
        self.start_time = time.time()
        self.update_time = self.start_time
        self.start_time_str = time.strftime("%A, %D, %H:%M:%S", time.localtime())
        self.num_evals_completed, self.num_gens_completed = 0, 0
        self.opt_params, self.opt_errors = [], []
    
    # Define MOGA hyperparameters
    def define_hyperparameters(self, num_gens, init_pop, offspring, crossover, mutation):
        self.num_gens   = num_gens
        self.init_pop   = init_pop
        self.offspring  = offspring
        self.crossover  = crossover
        self.mutation   = mutation

    # Updates the results after X iterations
    def update_results(self, params, errors):

        # Update optimisation progress
        self.num_evals_completed += 1
        self.num_gens_completed = (self.num_evals_completed - self.init_pop) / self.offspring + 1
        
        # If parameters are valid, update the population
        if not BIG_VALUE in errors:
            self.update_population(params, errors)

        # Record results after X generations
        if self.num_gens_completed > 0 and self.num_gens_completed % self.interval == 0:

            # Get time since previous update in seconds
            current_time = time.time()
            update_duration = round(current_time - self.update_time)
            self.update_time = current_time

            # Prepare CSV output
            num_gens_completed_padded = str(round(self.num_gens_completed)).zfill(len(str(self.num_gens)))
            file_path = f"{self.path}_{num_gens_completed_padded} ({update_duration}s).xlsx"

            # Write to CSV
            writer = pd.ExcelWriter(file_path, engine = "xlsxwriter")
            self.record_settings(writer)
            self.record_results(writer)
            self.record_plot(writer)
            writer.save()

            # Display progress in console
            progress = f"{num_gens_completed_padded}/{self.num_gens}"
            print(f"  Recorded results ({progress} in {update_duration}s)")
    
    # Updates the population
    def update_population(self, params, errors):
        params, errors = list(params), list(errors)
        err_sqr_sum = sum([error**2 for error in errors])

        # If the stored parameters exceed the limit, remove the worst
        if len(self.opt_params) == self.population:
            if self.opt_errors[-1][-1] < err_sqr_sum:
                return
            self.opt_params.pop()
            self.opt_errors.pop()
        
        # Adds new params in order
        inserted = False
        for i in range(0, len(self.opt_params)):
            if err_sqr_sum < self.opt_errors[i][-1]:
                self.opt_params.insert(i, params)
                self.opt_errors.insert(i, errors + [err_sqr_sum])
                inserted = True
                break

        # If new params is worst between existing params
        if not inserted:
            self.opt_params.append(params)
            self.opt_errors.append(errors + [err_sqr_sum])

    # Records the settings
    def record_settings(self, writer):

        # Settings Data
        settings = {
            "Status":       ["Complete" if self.num_gens_completed == self.num_gens else "Incomplete"],
            "Progress":     [f"{round(self.num_gens_completed)}/{self.num_gens}"],
            "Start Time":   [self.start_time_str],
            "End Time":     [time.strftime("%A, %D, %H:%M:%S", time.localtime())],
            "Time Elapsed": [f"{round(time.time() - self.start_time)}s"],
            "Model":        [self.model.get_name()],
            "Params":       self.model.get_param_names(),
            "Lower Bound":  self.model.get_param_lower_bounds(),
            "Upper Bound":  self.model.get_param_upper_bounds(),
            "Errors":       self.error_names,
            "Tests":        [exp_curve["test"] for exp_curve in self.exp_curves],
            "Stresses":     [exp_curve["stress"] for exp_curve in self.exp_curves],
            "Temperatures": [exp_curve["temp"] for exp_curve in self.exp_curves],
            "num_gens":     [self.num_gens],
            "init_pop":     [self.init_pop],
            "offspring":    [self.offspring],
            "crossover":    [self.crossover],
            "mutation":     [self.mutation],
        }

        # Change format of data
        columns = list(settings.keys())
        data = zip_longest([settings[column] for column in columns])
        data = list(map(list, zip(*data)))
        settings_dataframe = pd.DataFrame(data, columns = columns)

        # Write settings
        settings_dataframe.style.apply(centre_align, axis = 0).to_excel(writer, "settings", index = False)
        sheet = writer.sheets["settings"]
        for column in settings_dataframe:
            column_length = max(settings_dataframe[column].astype(str).map(len).max(), len(column)) + 1
            column_index = settings_dataframe.columns.get_loc(column)
            sheet.set_column(column_index, column_index, column_length)
    
    # Records the results
    def record_results(self, writer):
        columns = [param["name"] for param in self.model.param_info] + self.error_names + ["err_sqr_sum"]
        data = [self.opt_params[i] + self.opt_errors[i] for i in range(0,len(self.opt_params))]
        results = pd.DataFrame(data, columns = columns)
        results.to_excel(writer, "results", index = False)

    # Records the plot
    def record_plot(self, writer):

        # Prepare predicted curves
        prd_curves = self.model.get_prd_curves(*self.opt_params[0])
        prd_x_flat = [prd_x for prd_curve in prd_curves for prd_x in get_thinned_list(prd_curve["x"])] # flatten
        prd_y_flat = [prd_y for prd_curve in prd_curves for prd_y in get_thinned_list(prd_curve["y"])] # flatten
        
        # Prepare chart
        data = zip_longest([self.exp_x_flat, self.exp_y_flat, prd_x_flat, prd_y_flat])
        data = list(map(list, zip(*data)))
        pd.DataFrame(data).to_excel(writer, "plot", index = False)
        workbook = writer.book
        worksheet = writer.sheets["plot"]
        chart = workbook.add_chart({"type": "scatter"})

        # Add curves to chart
        marker = {"type": "circle", "size": 3}
        chart.add_series({"categories": ["plot", 1, 0, len(prd_x_flat), 0], "values": ["plot", 1, 1, len(prd_x_flat), 1], "marker": marker})
        chart.add_series({"categories": ["plot", 1, 2, len(prd_x_flat), 2], "values": ["plot", 1, 3, len(prd_x_flat), 3], "marker": marker})

        # Insert chart into worksheet
        chart.set_x_axis({"name": "Time", "major_gridlines": {"visible": True}})
        chart.set_y_axis({"name": "Strain", "major_gridlines": {"visible": True}})
        worksheet.insert_chart("A1", chart)

# For centre-aligning the cellss
def centre_align(x):
    return ["text-align: center" for _ in x]

# Returns a thinned list
def get_thinned_list(unthinned_list):
    src_data_size = len(unthinned_list)
    step_size = src_data_size / CURVE_DENSITY
    thin_indexes = [math.floor(step_size*i) for i in range(1, CURVE_DENSITY - 1)]
    thin_indexes = [0] + thin_indexes + [src_data_size - 1]
    return [unthinned_list[i] for i in thin_indexes]

# Imitates zip longest but for a list of lists
def zip_longest(list_list):
    max_values = max([len(list) for list in list_list])
    new_list_list = []
    for list in list_list:
        new_list = list + [None] * (max_values - len(list))
        new_list_list.append(new_list)
    return new_list_list