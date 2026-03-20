from data import data
from data.db import setup_database
from core.context import GameContext
from core.command import Command
from core.players import pull as load_players
from core.players import show_all as show_players
from core.phase_manager import PhaseManager
from core.status import Status
from core.role_manager import RoleManager
from utils.log import delete_log, log_this
from utils.format import prints

"""
 -- WAREWOLVES (ver 1.0.137)
 Support utility for the game master
 Author: TeoCervi05
 Language: Python 3.1.37
"""

def main():
    # title
    prints("werewolves - game master tool", "title")

    # setup database
    setup_database()
    delete_log()

    # initializing objects
    status = Status()
    players = load_players()
    game = GameContext(status, players)
    role_manager = RoleManager(game)
    phase_manager = PhaseManager(game, role_manager)
    phase_manager.start()
    cmd = Command(game, phase_manager)

    log_this("system", "The game has been initialized.", game.status.day)

    while True:
        # listen for commands
        cmd.ins()

        # exit game
        if cmd.query == "exit":
            prints("Exiting the game...", "body")
            break

if __name__ == "__main__":
    main()