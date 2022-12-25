"""
 Title:         Surrogate
 Description:   Contains the DNN for the Surrogate Model 
 Author:        Janzen Choi

"""

# Libraries
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" # disable warnings
import tensorflow.keras as kr
import numpy as np

# Surrogate Class
class Surrogate:

    # Constructor
    def __init__(self, input_size, output_size):

        # Define and compile neural network
        self.model = kr.Sequential()
        self.model.add(kr.layers.Dense(units=200, input_dim=input_size))
        self.model.add(kr.layers.Activation("relu"))
        self.model.add(kr.layers.Dense(units=50))
        self.model.add(kr.layers.Activation("relu"))
        self.model.add(kr.layers.Dense(units=50))
        self.model.add(kr.layers.Activation("relu"))
        self.model.add(kr.layers.Dense(units=output_size))
        self.model.compile(optimizer="sgd", loss="mse")

    # Fits the model
    def fit(self, x_train, y_train, epochs=100, batch_size=32):
        x_train = np.array(x_train)
        y_train = np.array(y_train)
        self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)

    # Makes a single prediction
    def predict(self, x_test):
        x_test = np.array([x_test])
        y_pred = self.model.predict(x_test, batch_size=10)
        return y_pred
