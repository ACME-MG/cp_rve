"""
 Title:         API
 Description:   Provides the user with an interface to interact with the code
 Author:        Janzen Choi

"""

# Libraries
import inspect
import modules.tessellator as tessellator
import modules.exporter as exporter
import modules.helper.progressor as progressor
from modules.orientation.csl import CSL_DICT
from modules.helper.general import *

# API class
class API:

    # Constructor
    def __init__(self):
        
        # Initialise tessellator and progress visualiser
        self.tess = tessellator.Tessellator()
        self.prog = progressor.Progressor()

        # Define available functions
        self.available_functions = [function for function in dir(API) if not function.startswith('__')]
        self.function_calls = {}
        for function in self.available_functions:
            self.function_calls[function] = False
        
        # Defines state of RVE
        self.has_twins  = False
        self.has_ori    = False

    # Safely calls define_domain
    def define_domain(self, shape_length = None, dimensions = None):
        self.__check_dependency__({"load_parents": False})

        # Checks input
        if not is_number(shape_length) or shape_length <= 0:
            self.__raise_error__("Input 'shape_length' must be a positive number")
        if not dimensions in [2, 3]:
            self.__raise_error__("Input 'dimensions' must be either 2 or 3")

        # Calls the function
        self.__call__(
            function    = self.tess.define_domain,
            arguments   = [shape_length, dimensions],
            message     = "Defining the domain of the RVE")

    # Safely calls tessellate_parents
    def add_parents(self, equivalent_radius = None, sphericity = None):
        self.__check_dependency__({"define_domain": True})

        # Checks inputs
        value_type = ["mu", "sigma", "min", "max"]
        if not is_number(equivalent_radius[0]):
            self.__raise_error__(f"Input 'equivalent_radius[{0}]' ({value_type[0]}) must be a number")
        if not is_number(sphericity[0]):
            self.__raise_error__(f"Input 'sphericity[{0}]' ({value_type[0]}) must be a number")
        for i in range(1,4):
            if not is_number(equivalent_radius[i]) or equivalent_radius[i] <= 0:
                self.__raise_error__(f"Input 'equivalent_radius[{i}]' ({value_type[i]}) must be a positive number")
            if not is_number(sphericity[i]) or sphericity[i] <= 0 or sphericity[i] > 1:
                self.__raise_error__(f"Input 'sphericity[{i}]' ({value_type[i]}) must be a number between 0 and 1")

        # Calls the function
        self.__call__(
            function    = self.tess.add_parents,
            arguments   = [equivalent_radius, sphericity],
            message     = "Generating tessellation of grains")

    # Safely calls load_parents
    def load_parents(self, path = None):
        self.__check_dependency__({"add_parents": False})
        self.__check_dependency__({"define_domain": False})

        # Checks input
        if not isinstance(path, str):
            self.__raise_error__("Input 'path' must be a string")
        if not os.path.exists(path):
            self.__raise_error__("Input 'path' must be a real path")
        if not path.endswith(".tess"):
            self.__raise_error__("Input 'path' must direct to a '.tess' file")
        if exporter.extract_data("scale", path, "*cellid") != []:
            self.__raise_error__("The '.tess' file must not have twins")

        # Calls the function
        self.__call__(
            function    = self.tess.load_parents,
            arguments   = [path],
            message     = "Loading in tessellation of grains")

    # Safely calls generate_twins
    def add_twins(self, twin_width):
        self.__check_dependency__({"add_parents": True, "load_parents": True})

        # Checks inputs
        value_type = ["mu", "sigma", "min", "max"]
        if not is_number(twin_width[0]):
            self.__raise_error__(f"Input 'twin_width[{0}]' ({value_type[0]}) must be a number")
        for i in range(1,4):
            if not is_number(twin_width[i]) or twin_width[i] <= 0:
                self.__raise_error__(f"Input 'twin_width[{i}]' ({value_type[i]})  must be a positive number")

        # Calls the function
        self.__call__(
            function    = self.tess.add_twins,
            arguments   = [twin_width],
            message     = "Generating twin structures")
        self.has_twins = True

    # Safely calls orient_random
    def orient_random(self):
        self.__check_dependency__({"add_parents": True, "load_parents": True})
        self.__check_dependency__({"orient_csl": False})

        # Calls the function
        self.__call__(
            function    = self.tess.orient_random,
            arguments   = [self.has_twins],
            message     = "Generating crystal orientations (random)")
        self.has_ori = True

    # Safely calls generate_orientations_csl
    def orient_csl(self, csl_sigma = None):
        self.__check_dependency__({"add_twins": True})
        self.__check_dependency__({"orient_random": False})

        # Checks inputs
        csl_domain = list(CSL_DICT.keys())
        if not isinstance(csl_sigma, str):
            self.__raise_error__("Input 'csl_sigma' must be a string")
        if not csl_sigma in csl_domain:
            csl_domain = ["'{}'".format(csl) for csl in csl_domain]
            self.__raise_error__("Input 'csl_sigma' must be either {}".format(conjunct(csl_domain, "or")))

        # Calls the function
        self.__call__(
            function    = self.tess.orient_csl,
            arguments   = [csl_sigma],
            message     = "Generating crystal orientations (CSL)")
        self.has_ori = True

    # Safely calls export_file
    def export_file(self, format = None):
        self.__check_dependency__({"add_parents": True, "load_parents": True})

        available_formats = ["tess", "tesr", "sim", "geo", "ply", "stl", "stl:bycell", "obj", "3dec", "vtk", "ori"]
        if not isinstance(format, str):
            self.__raise_error__("Input 'format' must be a string")
        if format not in available_formats:
            available_formats = ["'{}'".format(format) for format in available_formats]
            self.__raise_error__("Input 'format' must be either {}".format(conjunct(available_formats, "or")))

        # Calls the function
        self.__call__(
            function    = self.tess.export_file,
            arguments   = [format],
            message     = "Outputing tessellation as a '.{}' file".format(format))

    # Safely calls get_stats
    # TODO input checking
    def get_stats(self, stats_list = None, include_header = True):
        self.__check_dependency__({"add_parents": True, "load_parents": True})

        # Calls the function
        self.__call__(
            function    = self.tess.get_stats,
            arguments   = [stats_list, include_header],
            message     = "Extracting statistics from tessellation")

    # Safely calls visualise
    def visualise(self):
        self.__check_dependency__({"add_parents": True, "load_parents": True})

        # Calls the function
        self.__call__(
            function    = self.tess.visualise,
            message     = "Visualising the tessellation")

    # Commences all the queued up functions
    def commence(self, remove_auxiliary = True):

        # Check queued up functions
        called_functions = [call for call in self.function_calls.items() if call[1]]
        if len(called_functions) == 0:
            return
        
        # Remove auxiliary files if desired
        if remove_auxiliary:
            self.__call__(
                function    = self.tess.remove_auxiliary_files,
                message     = "Removing all auxiliary files"),
        
        # Start queued up functions
        self.prog.start()

    # Checks whether a function can be called
    def __check_dependency__(self, requirements):
        
        # If there is only one requirement
        if len(requirements.keys()) == 1:
            key = list(requirements.keys())[0]
            if requirements[key] != self.function_calls[key]:
                if requirements[key]:
                    error = "Requires the '{}' function to be called first".format(key)
                else:
                    error = "Cannot be called together with the '{}' function".format(key)
                self.__raise_error__(error, inspect.stack()[1][3])
        
        # If there are multiple, make sure at least one of the requirements are met
        for key in requirements.keys():
            if self.function_calls[key] == requirements[key]:
                return
        requiredFunctions = conjunct(["'{}'".format(key) for key in requirements.keys()], "or")
        error = "Requires either the {} function to be called first".format(requiredFunctions)
        self.__raise_error__(error, inspect.stack()[1][3])

    # Indicates than an input error has been made
    def __raise_error__(self, message, caller = ""):
        caller = inspect.stack()[1][3] if caller == "" else caller
        silent_raise(message, caller)

    # Indicates that a function has been called
    def __call__(self, function, arguments = [], message = ""):
        self.prog.queue(function, arguments, message)
        self.function_calls[inspect.stack()[1][3]] = True