"""
 Title:         The Model Factory
 Description:   For creating and returning model objects
 Author:        Janzen Choi

"""

# Models
from modules.models.cubic import Cubic
from modules.models.evp import EVP
from modules.models.evpwd import EVPWD
from modules.models.evpwd_s import EVPWD_S
from modules.models.thkr import THKR

# Creates and return a model
def get_model(model_name):
    model_list = (
        Cubic(),
        EVP(),
        EVPWD(),
        EVPWD_S(),
        THKR(),
    )
    model_list = [model for model in model_list if model.get_name() == model_name]
    return model_list[0]