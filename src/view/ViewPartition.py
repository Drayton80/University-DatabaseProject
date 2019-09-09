import sys
import os

class ViewPartition:
    _border_divisory = '#----------------------------------------------------------------------------#'
    _input_divisory  = '---------------------------------------------------------'
    
    def border_logo(self):
        self.clear_console()
        self.border_divisory()
        print("\t\t\t\tPOST-AGE")
        self.border_divisory()
    
    def border_divisory(self):
        print("")
        print(self._border_divisory)
        print("")

    def input_divisory(self):
        print("")
        print(self._input_divisory)
        print("")

    def clear_console(self):
        if sys.platform == "linux" or sys.platform == "linux2":
            clear = lambda: os.system('clear')
            clear()
        elif sys.platform == "win32" or sys.platform == "win64":
            clear = lambda: os.system('cls')
            clear()

    