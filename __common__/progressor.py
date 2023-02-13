"""
 Title:         Progressor
 Description:   For visualising the steps of a process
 Author:        Janzen Choi

"""

# Libraries
import time, os, sys, atexit
import printer

# Constants
START_INDEX  = 1
MIN_PADDING  = 5
INIT_LENGTH  = 30
END_PAD_CHAR = "."

# Display settings
DISPLAY_FANCY = 2
DISPLAY_PLAIN = 1
DISPLAY_OFF   = 0

# Statuses
COMPLETE = "Complete"
ONGOING  = "Ongoing"
FAILED   = "Failed"

# For visualising the progress of a process
class Progressor:

    # Constructor
    def __init__(self, title="", display=DISPLAY_FANCY):

        # Initialise inputs
        self.title = title
        self.display = display
        
        # Initialise auxiliary
        self.message_list = []
        self.start_time = time.time()
        self.start_time_string = time.strftime("%y/%m/%d, %H:%M:%S", time.localtime(self.start_time))
        atexit.register(self.__finish__)

    # Print caller depending on fanciness
    def __print__(self, message="", options=[], newline=True):
        if self.display == DISPLAY_FANCY:
            printer.print(message, options, newline)
        elif self.display == DISPLAY_PLAIN:
            end = "\n" if newline else ""
            print(message, end=end)

    # Displays all the messages
    def __display__(self):
        
        # Only clear if not verbose
        if self.display != DISPLAY_OFF:
            os.system('cls' if os.name == 'nt' else 'clear')

        # Get auxiliary values
        max_length = max([len(message["message"]) for message in self.message_list])
        max_length = max(INIT_LENGTH, max_length)
        max_index_length = len(str(len(self.message_list)))

        # Print the title
        self.__print__(f"\n  Progress Report ({self.start_time_string}):\n", ["orange"])

        # Print the components
        for i in range(len(self.message_list)):

            # Extract message and duration
            message     = self.message_list[i]["message"]
            duration    = self.message_list[i]["duration"]
            status      = self.message_list[i]["status"]

            # Print index and message
            padding_start = (2 + max_index_length - len(str(i+1))) * " "
            padding_end = (MIN_PADDING + max_length - len(message)) * END_PAD_CHAR
            self.__print__(f"{padding_start} {i+1}) ", ["orange"], False)
            self.__print__(f"{message} {padding_end} ", [], False)
            
            # Print progress status
            if status == COMPLETE:
                self.__print__("[Complete]", ["l_green"], False)
                self.__print__(f" ({duration}s)")
            elif status == ONGOING:
                self.__print__("[Ongoing]", ["yellow"])
                self.__print__("")
            elif status == FAILED:
                self.__print__("[Failed]", ["l_red"], False)
                self.__print__(f" ({duration}s)")
    
    # When closing, display end message
    def __finish__(self):

        # If an error was raised, then sys.last_value exists, and leave
        try:
            sys.last_value
            return
        except AttributeError:
            pass

        # Update progress
        self.message_list[-1]["duration"] = round(time.time() - self.curr_time, 2)
        if self.message_list[-1]["status"] == ONGOING:
            self.message_list[-1]["status"] = COMPLETE

        # Display final message
        self.__display__()
        total_duration = round(time.time() - self.start_time, 2)
        final_message = f" ({self.title})" if self.title != "" else ""
        self.__print__(f"\n  Finished in {total_duration}s{final_message}!\n", ["orange"])

    # Adds a component to the process
    def add(self, message):

        # Update duration if not first
        if len(self.message_list) > 0:
            self.message_list[-1]["duration"] = round(time.time() - self.curr_time, 2)
            if self.message_list[-1]["status"] == ONGOING:
                self.message_list[-1]["status"] = COMPLETE
        self.curr_time = time.time()

        # Add message and display
        self.message_list.append({
            "message": message,
            "duration": 0,
            "status": ONGOING,
        })
        self.__display__()
    
    # Fails the current process but move on
    def fail(self):
        if len(self.message_list) > 0:
            self.message_list[-1]["duration"] = round(time.time() - self.curr_time, 2)
            self.message_list[-1]["status"] = FAILED
            self.__display__()
            print()