"""
 Title:         Custom Lognormal Distribution
 Description:   For defining a custom lognormal distribution
 Author:        Janzen Choi

"""

# Libraries
import numpy as np
import random

# Constants
DEFAULT_MIN = 0
DEFAULT_MAX = 100000
DEFAULT_SIZE = 10000

# Lognormal Class
class Lognormal:

    # Constructor
    def __init__(self, mu, sigma, min = DEFAULT_MIN, max = DEFAULT_MAX, amount = DEFAULT_SIZE):
        self.distribution = np.random.lognormal(mu, sigma, amount)
        self.distribution = [d for d in self.distribution if d >= min and d <= max]

    # Gets a value from the lognormal distribution
    def get_val(self):
        return round(self.distribution[random.randrange(len(self.distribution))], 10)

    # Gets values from the lognormal distribution
    def get_vals(self, size):
        return [self.get_val() for _ in range(size)]

    # Gets normalised values from the lognormal distribution
    def get_norm_vals(self, size, norm_value):
        values = self.get_vals(size)
        factor = norm_value / sum(values)
        return [value * factor for value in values]

# Determines the mean and standard deviation from mu and sigma
def get_mean_std(mu, sigma):
    mean = np.exp(mu + sigma**2 / 2)
    variance = (np.exp(sigma**2) - 1) * np.exp(2*mu + sigma**2)
    return round(mean, 5), round(variance ** 0.5, 5)

# # Fits a set of data to a lognormal distribution and returns the statistics
# def fit_lognormal(data):
#     params = paramnormal.lognormal.fit(data)
#     return {
#         "mu": params[0],
#         "sigma": params[1],
#         "mean": np.average(data),
#         "stdev": np.std(data),
#         "min": min(data),
#         "max": max(data),
#     }

# Plots a lognormal distribution given statistics
def plot_lognormal(stats):
    distribution = Lognormal(stats["mu"], stats["sigma"])
    vals = distribution.get_vals(100)
    # plt.hist(vals, 100)
    # plt.savefig("tester")