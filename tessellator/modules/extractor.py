"""
 Title:         Extracter
 Description:   Extracts data
 Author:        Janzen Choi

"""

# Searches for a keyword in a text file and extracts the contained data
def extract_data(keyword, filename, end_char = "*"):
    
    # Read the file
    file = open(filename, "r")
    data = file.read()
    file.close()

    # Searches for the data encased by the keyword
    start   = data.find(keyword)
    data    = data[start:]
    end     = data.find(end_char)
    data    = data[:end]

    # Process the extracted data and return
    data = data.replace("\n", " ")
    data = data.split(" ")
    data = [d for d in data if d != ""]
    return data