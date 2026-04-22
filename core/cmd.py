from utils.format import *

class Command:
    def __init__(self):
        self.query = ""
        self.params = []
    
    def line(self, ctx):
        parts = printq().split(" ")
        self.query = parts[0]
        self.params = parts[1:]

        if self.query == "help":
            """
            Take this to another script:
            it will soon get more complex due to the phase depentent list
            """
            printf("list of avaible commands:", "head")
            printf("help - Get help about a command;_quit - proceed with the GTFO protocol;_status - show current game status.", "bull")
            return 0

        if self.query == "player":
            printf("Player coming soon!")
            return 0

        if self.query == "quit":
            return 1

        if self.query == "status":
            ctx.status.show()
            return 0

        printf(f"unknown command \'{self.query}\'", "err")
        return 0