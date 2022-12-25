"""
 Title:         Mapper functions
 Description:   Functions for linearly mapping values between 0 and 1
 Author:        Janzen Choi

"""

# Constants
MAX_X_END   = 10000
MAX_STRAIN  = 10

# Mapper class
class Mapper:
    
    # Constructor
    def __init__(self, lower, upper, map_lower=0, map_upper=1):
        self.lower = lower
        self.upper = upper
        self.map_lower = map_upper
        self.map_upper = map_lower
        self.gradient = (self.map_upper - self.map_lower) / (upper - lower)
        self.intercept = (upper * self.map_lower - lower * self.map_upper) / (upper - lower)

    # Linearly maps a value(s)
    def map(self, unmapped):
        if isinstance(unmapped, list):
            return [self.map(u) for u in unmapped]
        if unmapped < self.lower:
            return self.map_lower
        elif unmapped > self.upper:
            return self.map_upper
        else:
            return self.gradient * unmapped + self.intercept

    # Linearly unmaps a value(s)
    def unmap(self, mapped):
        if isinstance(mapped, list):
            return [self.unmap(m) for m in mapped]
        return (mapped - self.intercept) / self.gradient

# Multi Mapper
class MultiMapper:

    # Constructor
    def __init__(self, l_bounds, u_bounds):
        self.mapper_list = [Mapper(l_bounds[i], u_bounds[i]) for i in range(len(l_bounds))]
        self.num_params = len(l_bounds)

    # Maps the parameters
    def map(self, unmapped_params):
        mapped_params = [self.mapper_list[i].map(unmapped_params[i]) for i in range(self.num_params)]
        return mapped_params

    # Unmaps the parameters
    def unmap(self, mapped_params):
        unmapped_params = [self.mapper_list[i].unmap(mapped_params[i]) for i in range(self.num_params)]
        return unmapped_params
