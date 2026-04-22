from core.cmd import Command
from core.ctx import Context
from data.db import setup_database
from utils.log import log_this
from utils.format import printf

"""
 -- WAREWOLVES (ver. 1.0.4) --
 Support utility for the game master
 AUTHOR: TeoCervi05
 LANGUAGE: Python 3.13.7
 Tested on Linux (I don't know if it works on other systems)
"""

def main():
    #title
    printf("werewolves - game master tool", "title")
    printf("Welcome: for a list of commands and applications, type \"help\" in the command line. Have a nice game!")
    
    #initializing objects
    setup_database()
    ctx = Context()
    cmd = Command()

    log_this("system", "game started succesfully")

    q = 0

    while 1 > 0:
        q = cmd.line(ctx)
        if q:
            break


if __name__ == "__main__":
    main()