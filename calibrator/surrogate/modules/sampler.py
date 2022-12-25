"""
 Title:         Sampler
 Description:   For sampling the parameter space
 Author:        Janzen Choi
"""

# Libraries
import numpy as np

# The Sampler class
class Sampler:

    # Constructor
    def __init__(self, l_bounds, u_bounds):
        self.l_bounds = l_bounds
        self.u_bounds = u_bounds

    # Returns points based on the N-level factorial design (N^K)
    def sample_LFD(self, factorial_N=2):

        # Define the domain
        domain = [np.linspace(self.l_bounds[i], self.u_bounds[i], factorial_N) for i in range(len(self.l_bounds))]
        num_points = factorial_N**len(self.l_bounds)
        
        # Obtain all points and return
        point_list = [[domain[j][i // factorial_N**j % factorial_N] for j in range(len(self.l_bounds))] for i in range(num_points)]
        return point_list

    # Returns axial points (2*K) given alpha (between 0 and 1)
    def sample_axial(self, alpha=0.5):

        # Define the domain
        domain = []
        for i in range(len(self.l_bounds)):
            mid_point       = (self.l_bounds[i] + self.u_bounds[i]) / 2
            alpha_magnitude = (self.u_bounds[i] - self.l_bounds[i]) * alpha
            axial_points    = [mid_point - alpha_magnitude, mid_point, mid_point + alpha_magnitude]
            domain.append(axial_points)
        
        # Obtain all points and return
        absolute_centre = [d[1] for d in domain]
        point_list = []
        for i in range(len(self.l_bounds)):
            
            # Add negative axial point
            negative_axial = absolute_centre.copy()
            negative_axial[i] = domain[i][0]
            point_list.append(negative_axial)

            # Add positive axial point
            positive_axial = absolute_centre.copy()
            positive_axial[i] = domain[i][2]
            point_list.append(positive_axial)
        return point_list

    # Returns centre point (1)
    def sample_centre(self):
        absolute_centre = [(self.l_bounds[i] + self.u_bounds[i]) / 2 for i in range(len(self.l_bounds))]
        return [absolute_centre]

    # Returns points based on centre composite design (2^K + 2*K + 1)
    def sample_CCD(self, axial=0.5):
        point_list = self.sample_LFD(2)
        point_list += self.sample_axial(axial)
        point_list += self.sample_centre()
        return point_list