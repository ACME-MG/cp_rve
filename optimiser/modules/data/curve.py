"""
 Title:         Curve
 Description:   Structures information about a curve
 Author:        Janzen Choi

"""



# Returns a curve dictionary
def get_curve(x_list = [], y_list = [], x_label = "", y_label = "", type = "", stress = 0, temp = 0, test = ""):
    return {
        "x":        x_list,
        "y":        y_list,
        "x_label":  x_label,
        "y_label":  y_label,
        "type":     type,
        "stress":   stress,
        "temp":     temp,
        "test":     test,
    }