"""
 Title:         Progress Visualiser
 Description:   For visualising the steps of a process
 Author:        Janzen Choi

"""

# Libraries
import time, os
import modules.helper.printer as printer

# Constants
START_INDEX     = 1
MIN_PADDING     = 5
PADDING_CHAR    = "."

# For visualising the progress of a process
class Progressor:

    # Constructor
    def __init__(self, verbose = False):
        self.function_list = []
        self.printed_text = ""
        self.verbose = verbose

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
            printer.print("")

            # Run the function
            modules_start_time = time.time()
            function["function"](*function["arguments"])

            # Print after running
            time_string = str(round((time.time() - modules_start_time) * 1000)) + "ms"
            self.__update__(printer.get_text("Done!", ["bold", "l_green"]))
            self.__update__(printer.get_text(" ({})\n".format(time_string), ["l_cyan"]))

        # Finish running everything
        message = " ({})".format(message) if message != "" else ""
        time_diff = round(time.time() - self.start_time, 2)
        printer.print("{}Finished in {} seconds{}\n".format(self.header_padding, time_diff, message), ["bold", "orange"])
    
    # Prints and stores message if the verbose option is turned off
    def __update__(self, message):
        if not self.verbose:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.printed_text += message
            printer.print("\n{}Progress Report ({}):\n".format(self.header_padding, self.start_time_string), ["bold", "orange"])
            printer.print(self.printed_text)