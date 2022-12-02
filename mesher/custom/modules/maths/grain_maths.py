"""
 Title:         Grain
 Description:   Contains grain-related functions
 Author:        Janzen Choi

"""

# Returns a grain dictionary
def get_grain_dict(phase_id, q1, q2, q3, q4, num_pixels):
    return {
        "phase_id": phase_id,
        "q1":       q1,
        "q2":       q2,
        "q3":       q3,
        "q4":       q4,
        "num_pixels": num_pixels,
    }

# Updates an existing grain dictionary
def update_grain_dict(grain_dict, q1, q2, q3, q4):
    num_pixels = grain_dict["num_pixels"]
    grain_dict["q1"] = (num_pixels * grain_dict["q1"] + q1) / (num_pixels + 1)
    grain_dict["q2"] = (num_pixels * grain_dict["q2"] + q2) / (num_pixels + 1)
    grain_dict["q3"] = (num_pixels * grain_dict["q3"] + q3) / (num_pixels + 1)
    grain_dict["q4"] = (num_pixels * grain_dict["q4"] + q4) / (num_pixels + 1)
    grain_dict["num_pixels"] += 1
    return grain_dict