"""
 Title:         Error
 Description:   Contains the basic structure for an error class
 Author:        Janzen Choi

"""

# Libraries
import math

# The Error Class
class Error:

    # Constructor
    def __init__(self, name, exp_curves):
        self.name = name
        self.exp_curves = exp_curves

    # Returns the name of the error
    def get_name(self):
        return self.name

    # Returns the experimental curve
    def get_exp_curves(self):
        return self.exp_curves
    
    # Returns an error (to be overriden)
    def get_value(self):
        pass

# Returns a list of indexes corresponding to thinned data
def get_thin_indexes(src_data_size, dst_data_size):
    step_size = src_data_size/dst_data_size
    thin_indexes = [math.floor(step_size*i) for i in range(1,dst_data_size-1)]
    thin_indexes = [0] + thin_indexes + [src_data_size-1]
    return thin_indexes

# Returns the derivative via backward finite difference
def get_bfd(x_list, y_list):
    dy_list = []
    for i in range(1,len(x_list)):
        dy = (y_list[i]-y_list[i-1])/(x_list[i]-x_list[i-1]) if (x_list[i] > x_list[i-1] and y_list[i] > y_list[i-1]) else 100
        dy_list.append(dy)
    return dy_list