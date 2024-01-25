"""
A custom logger implementing command-line interface colour specifications
"""

class cmd_color:
	BLACK       = "\033[30m"
	RED         = "\033[31m"
	GREEN       = "\033[32m"
	YELLOW      = "\033[33m"
	MAGENTA     = "\033[35m"
	CYAN        = "\033[36m"
	WHITE       = "\033[97m"

def ERROR_STR(data):
    return cmd_color.RED + data + cmd_color.WHITE

def ERROR(data):
    print(ERROR_STR(data))

def WARNING_STR(data):
     return cmd_color.YELLOW + data + cmd_color.WHITE
    
def WARNING(data):
    print(WARNING_STR(data))

def SUCCESS_STR(data):
     return cmd_color.GREEN + data + cmd_color.WHITE
    
def SUCCESS(data):
    print(SUCCESS_STR(data))

def MESSAGE_STR(data):
     return cmd_color.CYAN + data + cmd_color.WHITE
    
def MESSAGE(data):
    print(MESSAGE_STR(data))

def TRACE_STR(data):
    return cmd_color.MAGENTA + data + cmd_color.WHITE
    
def TRACE(data):
    print(TRACE_STR(data))