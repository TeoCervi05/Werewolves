from core.cmd import Command
from core.ctx import Context
from core.phase_manager import PhaseManager
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
    printf("Welcome:", "body")
    printf("for a list of commands and applications, type \"help\" in the command line;_to have information about a specific command, type \"help {query}\".", "bull")
    printf("Have a nice game!", "body")
    
    #initializing objects
    setup_database()
    ctx = Context()
    pmanager = PhaseManager(ctx)
    cmd = Command()

    pmanager.start(ctx.status.phase)

    log_this("system", "game started succesfully")

    q = 0

    while 1 > 0:
        q = cmd.line(ctx, pmanager)
        if q:
            #GTFO protocol
            printf("Goodbye!")
            break


if __name__ == "__main__":
    main()