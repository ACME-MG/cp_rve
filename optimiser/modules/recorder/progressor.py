"""
 Title:         Progress Visualiser
 Description:   For visualising the steps of a process
 Author:        Janzen Choi

"""

# Libraries
import time, os
import modules.recorder.printer as printer

# Constants
START_INDEX     = 1
MIN_PADDING     = 5
PADDING_CHAR    = "."

# For visualising the progress of a process
class Progressor:

    # Constructor
    def __init__(self, fancy = False):
        self.function_list = []
        self.printed_text = ""
        self.fancy = fancy

    # Queues up a (non-returning) function
    def queue(self, function, arguments = [], message = ""):
        self.function_list.append({
            "function": function,
            "arguments": arguments,
            "message": message
        })

    # Runs all the queued up functions
    def start(self, message = ""):

        # Determine formatting
        max_index_padding_length = len(str(len(self.function_list))) + 1
        max_message_length = max([len(function["message"]) for function in self.function_list])
        self.header_padding = " " * max_index_padding_length
        self.start_time = time.time()
        self.start_time_string = time.strftime("%y/%m/%d, %H:%M:%S", time.localtime(self.start_time))
        
        # Iterate through functions
        for i in range(len(self.function_list)):

            # Print before running
            function = self.function_list[i]
            index_padding = " " * (max_index_padding_length - len(str(i + 1)))
            message_padding = PADDING_CHAR * (max_message_length - len(function["message"]) + MIN_PADDING)
            self.__update__("  {}{}) {} {} ".format(index_padding, i + 1, function["message"], message_padding))
            self.__print__("")

            # Run the function
            modules_start_time = time.time()
            function["function"](*function["arguments"])

            # Print after running
            time_string = str(round((time.time() - modules_start_time) * 1000)) + "ms"
            self.__update__("Done!", ["bold", "l_green"])
            self.__update__(" ({})\n".format(time_string), ["l_cyan"])

        # Finish running everything
        message = " ({})".format(message) if message != "" else ""
        time_diff = round(time.time() - self.start_time, 2)
        self.__print__("{}Finished in {} seconds{}\n".format(self.header_padding, time_diff, message), ["bold", "orange"])
    
    # Prints and stores message
    def __update__(self, message, settings = []):

        # If fancy, adding formatting
        if self.fancy:
            message = printer.get_text(message, settings)

        # Clear and print
        os.system("cls" if os.name == "nt" else "clear")
        self.printed_text += message
        self.__print__("\n{}Progress Report ({}):\n".format(self.header_padding, self.start_time_string), ["bold", "orange"])
        self.__print__(self.printed_text)
    
    # Prints
    def __print__(self, message, settings = []):
        if self.fancy:
            printer.print(message, settings)
        else:
            print(message)