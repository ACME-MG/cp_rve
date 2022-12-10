"""
 Title:         The Objective class
 Description:   For storing the errors to be minimised
 Author:        Janzen Choi

"""

# Libraries
import math

# Constants
BIG_VALUE = 100

# The Objective class
class Objective():

    # Constructor
    def __init__(self, model, error_list):
        self.model      = model
        self.error_list = error_list

    # Returns the model
    def get_model(self):
        return self.model

    # Returns the objective names
    def get_error_names(self):
        return [error.get_name() for error in self.error_list]

    # Gets all the errors
    def get_error_values(self, prd_curves):
        if prd_curves == []:
            return [BIG_VALUE] * len(self.error_list)
        error_values = [error.get_value(prd_curves) for error in self.error_list]
        error_values = [BIG_VALUE if math.isnan(error_value) else error_value for error_value in error_values]
        return error_values