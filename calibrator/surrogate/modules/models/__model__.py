"""
 Title:         Model
 Description:   Contains the basic structure for a model class
 Author:        Janzen Choi
 
"""

# The Model Class
class Model:

    # Constructor
    def __init__(self, name, param_info):
        self.name = name
        self.param_info = param_info

    # Returns the name of the model
    def get_name(self):
        return self.name

    # Returns the parameter names
    def get_param_names(self):
        return [param["name"] for param in self.param_info]

    # Returns the parameter lower bounds
    def get_param_lower_bounds(self):
        return [param["min"] for param in self.param_info]

    # Returns the parameter upper bounds
    def get_param_upper_bounds(self):
        return [param["max"] for param in self.param_info]
    
    # Returns the experimental curves
    def get_curve(self):
        return []