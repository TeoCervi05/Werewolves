from utils.format import *
from utils.help import system_help

class Command:
    def __init__(self):
        self.query = ""
        self.params = []
    
    def line(self, game, pmanager):
        parts = printq().split(" ")
        self.query = parts[0]
        self.params = parts[1:]

        if self.query == "help":
            if len(self.params) == 0:
                printf("list of avaible commands:", "stitle")
                printf("system queries:", "head")
                printf("help - get general or specifical help;_quit - proceed with the GTFO protocol.", "bull")
                printf(f"{game.status.phase} queries:", "head")
                printf(pmanager.help,"bull")
                return 0
            if len(self.params) == 1:
                system_help(self.params[0])
                return 0
            printf(f"\"help\" requires 0 to 1 parameters, {len(self.params)} was given", "err")

        if self.query == "player":
            printf("Player coming soon!")
            return 0

        if self.query == "quit":
            return 1

        if self.query == "status":
            game.status.show()
            return 0

        printf(f"unknown command \'{self.query}\'", "err")
        return 0