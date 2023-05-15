"""
 Title:         Voce Slip Hardening Asaro Inelasticity Model
 Description:   For creating the VSHAI material file
 Author:        Janzen Choi

"""

# Voce Slip Hardening Asaro Inelasticity Class
class VSHAI:

    # Constructor
    def __init__(self) -> None:
        super().__init__("vshai")
    
    # Creates the file content
    def get_content(self) -> str:
        raise NotImplementedError