from utils.format import *

class Command:
    def __init__(self):
        self.query = ""
        self.params = []
    
    def line(self):
        parts = printq().split(" ")
        self.query = parts[0]
        self.params = parts[1:]

        if self.query == "quit":
            return 1

        if self.query == "help":
            prints("Help coming soon!")
        
        return 0