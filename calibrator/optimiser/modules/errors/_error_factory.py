"""
 Title:         The Error Factory
 Description:   For creating and returning error objects
 Author:        Janzen Choi

"""

# Errors
from modules.errors.dy_area import DyArea
from modules.errors.x_area import XArea
from modules.errors.y_area import YArea
from modules.errors.x_end import XEnd
from modules.errors.y_end import YEnd

# Returns a list of errors
def get_error_list(error_names, exp_curves):
    error_list = (
        DyArea(exp_curves),
        XArea(exp_curves),
        YArea(exp_curves),
        XEnd(exp_curves),
        YEnd(exp_curves),
    )
    error_list = [error for error in error_list if error.get_name() in error_names]
    return error_list