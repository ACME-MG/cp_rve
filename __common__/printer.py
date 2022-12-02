"""
 Title:         Printer
 Description:   For printing text to the terminal
 Author:        Janzen Choi

"""

# Libraries
import subprocess

# Constants
OPTIONS = {
    "black":        "\\033[30m",
    "red":          "\\033[31m",
    "green":        "\\033[32m",
    "orange":       "\\033[33m",
    "blue":         "\\033[34m",
    "purple":       "\\033[35m",
    "cyan":         "\\033[36m",
    "l_grey":       "\\033[37m",
    "darkgrey":     "\\033[90m",
    "l_red":        "\\033[91m",
    "l_green":      "\\033[92m",
    "yellow":       "\\033[93m",
    "l_blue":       "\\033[94m",
    "pink":         "\\033[95m",
    "l_cyan":       "\\033[96m",
    "bold":         "\\033[1m",
    "underline":    "\\033[4m",
    "strike":       "\\033[9m",
    "bg_black":     "\\033[40m",
    "bg_red":       "\\033[41m",
    "bg_green":     "\\033[42m",
    "bg_orange":    "\\033[43m",
    "bg_blue":      "\\033[44m",
    "bg_purple":    "\\033[45m",
    "bg_cyan":      "\\033[46m",
    "bg_l_grey":    "\\033[47m",
}
PRINT_RESET = "\\033[0m"

# Prints with boldening
def print(text, options = [], newline = True):
    formats = [OPTIONS[option] for option in options]
    pretext = "".join(formats)
    newline = "" if newline else "-n"
    subprocess.run(["echo {} \"{}{}{}\"".format(newline, pretext, text, PRINT_RESET)], shell = True)

# Gets the text with formatting
def get_text(text, options = []):
    formats = [OPTIONS[option] for option in options]
    pretext = "".join(formats)
    return pretext + text + PRINT_RESET