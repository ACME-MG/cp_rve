"""
 Title:         Excel I/O
 Description:   For reading and writing to .xlsx files
 Author:        Janzen Choi

"""

# Libraries
import pandas as pd

# Constants
DEFAULT_PATH    = "./"
DEFAULT_FILE    = "excel"
DEFAULT_SHEET   = "info"

# Class for reading data
class Excel:

    # Constructor
    def __init__(self, path = DEFAULT_PATH, file = DEFAULT_FILE, sheet = DEFAULT_SHEET):
        self.path   = path
        self.file   = file
        self.sheet  = sheet

    # Sets the default values if empty
    def set_default(self, path, file, sheet):
        path = self.path if path == "" else path        
        file = self.file if file == "" else file
        sheet = self.sheet if sheet == "" else sheet
        return path, file, sheet

    # Reads a column of data and returns it in the form of a list
    def read_column(self, column, path="", file="", sheet=""):
        path, file, sheet = self.set_default(path, file, sheet)
        data = pd.read_excel(io=f"{path}/{file}.xlsx", sheet_name=sheet, usecols=[column])
        data = data.dropna()
        data = data.values.tolist()
        data = [d[0] for d in data]
        return data

    # Reads multuple columns of data
    def read_columns(self, columns, path="", file="", sheet=""):
        path, file, sheet = self.set_default(path, file, sheet)
        data = [self.read_column(column = column) for column in columns]
        data = [[column[i] for column in data] for i in range(0, len(data[0]))]
        return data

    # Gets a list of data only for the included tests
    def read_included(self, column, test_names):
        info_list = self.read_column(column=column, sheet="info")
        test_list = self.read_column(column="test", sheet="info")
        info_list = [info_list[test_list.index(test_name)] for test_name in test_names]
        return info_list