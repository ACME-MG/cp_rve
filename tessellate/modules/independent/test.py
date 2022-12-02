"""
 Title:         Main test file
 Description:   Custom code for conducting tests on algorithmic code
 Author:        Janzen Choi

"""

# Libraries
import time, random
import modules.helper.printer as printer
import modules.lognormal as lognormal
import modules.orientation.csl as csl
import modules.orientation.euler_converter as euler_converter
import modules.orientation.misorienter as misorienter
import modules.orientation.angle as angle

# Constants
DEFAULT_MAX_CHARS   = 30
DEFAULT_MAX_INDEX   = 99

# Main function
def main():
    tester = Tester()
    tester.conduct_test(test_angle, "angle conversions")
    tester.conduct_test(test_matrix, "matrix conversions")
    tester.conduct_test(test_misorientation, "misorientation generator")
    tester.conduct_test(test_csl, "CSL orienter")
    tester.conduct_test(test_lognormal, "lognormal distributor")
    tester.finish()

# Tester class
class Tester:

    # Constructor
    def __init__(self, max_chars = DEFAULT_MAX_CHARS, max_index = DEFAULT_MAX_INDEX):
        self.start_time = time.time()
        self.start_time_string = time.strftime("%H:%M:%S", time.localtime(self.start_time))
        self.index = 1
        self.num_passes = 0
        self.num_fails = 0
        self.max_chars = max_chars
        self.max_index = max_index
        self.header_padding = " " * (len(str(self.max_index)))
        printer.print("\n{}Test Report (started at {}):\n".format(self.header_padding, self.start_time_string), ["bold", "orange"])

    # Conducts a test
    def conduct_test(self, function, test_desc):
        
        # Prepare text
        index_padding = " " * (len(str(self.max_index)) - len(str(self.index)))
        result_padding = "." * (self.max_chars - len(test_desc))
        printer.print("  {}{}) Testing {} {} ".format(index_padding, self.index, test_desc, result_padding), newline = False)

        # Conduct test
        time_start = time.time()
        result = function()
        self.num_passes += result
        self.index += 1

        # Print result
        result_text = "Passed" if result else "Failed"
        result_colour = "l_green" if result else "l_red"
        printer.print(result_text, [result_colour, "bold"], newline = False)
        printer.print(" ({}ms)".format(round((time.time() - time_start) * 1000)), ["l_cyan"])

    # Prints a summary of all the tests
    def finish(self):
        time_diff = round(time.time() - self.start_time, 2)
        printer.print("\n{}Finished in {} seconds ({}/{} passed)\n".format(self.header_padding, time_diff, self.num_passes, self.index - 1), ["bold", "orange"])

# Tests angle conversions
def test_angle():
    num_trials = 10
    for _ in range(num_trials):
        euler_1 = angle.random_euler()
        quat_1 = angle.euler_to_quat(*euler_1)
        euler_2 = angle.quat_to_euler(*quat_1)
        diff = sum([abs(euler_1[i] - euler_2[i]) for i in range(len(euler_1))])
        if diff > 0.00001:
            return False
    return True

# Tests all the possible CSL values (within 1 degree)
def test_csl():
    csl_keys = csl.CSL_DICT.keys()
    for key in csl_keys:
        euler_angles = csl.get_csl_euler_angles(key)
        mori = misorienter.get_misorientation_angle(euler_angles[0], euler_angles[1], "cubic")
        mori = angle.rad_to_deg(mori)
        mori_diff = abs(mori - csl.CSL_DICT[key]["mori"])
        if mori_diff > 1: # degree
            return False
    return True

# Tests misorientation operations
def test_misorientation():
    num_trials = 10
    max_misorientation = 60 # degrees
    crystal_types = ["cubic", "hexagonal", "tetrahedral"]
    for crystal_type in crystal_types:
        for _ in range(num_trials):
            mori_1 = angle.deg_to_rad(random.uniform(0, 1) * max_misorientation)
            euler_pair = misorienter.generate_euler_pair(mori_1, crystal_type)
            mori_2 = misorienter.get_misorientation_angle(euler_pair[0], euler_pair[1], crystal_type)
            mori_diff = angle.rad_to_deg(abs(mori_1 - mori_2))
            if mori_diff > 1: # degree
                return False
    return True

# Tests matrix conversions
def test_matrix():
    num_trials = 10
    for _ in range(num_trials):
        euler_0 = angle.random_euler()
        matrix_1 = euler_converter.euler_to_matrix(euler_0)
        euler_1 = euler_converter.matrix_to_euler(matrix_1)
        matrix_2 = euler_converter.euler_to_matrix(euler_1)
        euler_2 = euler_converter.matrix_to_euler(matrix_2)
        diff = sum([abs(euler_1[i] - euler_2[i]) for i in range(len(euler_1))])
        if diff > 0.00001:
            return False
    return True

# Tests the lognormal distributor
def test_lognormal():
    num_trials = 10
    num_vals = 10
    max_val = 10
    max_norm = 100
    for _ in range(num_trials):
        mu = random.uniform(0.1, 1) * max_val // 10
        sigma = random.uniform(0.1, 1) * max_val // 10
        dist = lognormal.Lognormal(mu, sigma)
        norm_val = random.uniform(0, 1) * max_norm
        norm_vals = dist.get_norm_vals(num_vals, norm_val)
        norm_vals_diff = abs(sum(norm_vals) - norm_val)
        if norm_vals_diff > 0.00001:
            return False
    return True

# Main function caller
if __name__ == "__main__":
    main()