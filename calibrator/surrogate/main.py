"""
 Title:         Main file
 Description:   For developing surrogate models
 Author:        Janzen Choi
 
"""

# Libraries
from modules.api import API

# Fails causes [] hard to CCD need to use log mapping

# Code
api = API(True)
api.define_model("evpwd_s")
# api.sample_random(1000)
api.sample_CCD()
api.train()
api.assess_random(10)