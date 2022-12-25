"""
 Title:         Main file
 Description:   For developing surrogate models
 Author:        Janzen Choi
 
"""

# Libraries
from modules.api import API

# Code
api = API(True)
api.define_sm("thkr")
# api.sample_CCD()
api.sample_random(9000)
api.train()
api.assess(10)