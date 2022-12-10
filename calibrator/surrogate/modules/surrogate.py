"""
 Title:         Surrogate Model
 Description:   For creating the surrogate model
 Author:        Janzen Choi
 
"""

# Libraries
import numpy as np
import pickle
from smt.surrogate_models import KPLS

# Surrogate Model Wrapper Class
class Surrogate:

    # Constructor
    def __init__(self):
        self.sm = KPLS(theta0=[1e-2]) # kriging model using partial least squares (PLS)

    # Trains the surrogate model
    def train_sm(self, input_list, output_list):
        self.sm.set_training_values(np.array(input_list), np.array(output_list))
        self.sm.train()

    # Assesses the surrogate model
    def predict(self, input_list):
        prd_output_list = self.sm.predict_values(np.array(input_list))
        return prd_output_list

    # Saves the trained model (via pickling)
    def save_sm(self, model_path):
        with open(f"{model_path}.pkl", "wb") as f:
            pickle.dump(self.sm, f)

    # Loads the trained model (via pickling)
    def load_sm(self, model_path):
        with open(f"{model_path}.pkl", "rb") as f:
            self.sm = pickle.load(f)