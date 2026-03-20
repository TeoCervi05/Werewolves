import data
from db import setup_database
from log import delete_log, log_this
from cmd import Command
from players import pull as check_players
from players import show_all as show_players
from status import Status
from characters import *
from format import prints

# -- WAREWOLVES (ver 1.0.137)
# Support utility for the game master
# Author: TeoCervi05
# Language: Python 3.1.37

def main():
    #setup
    setup_database()
    delete_log()
    game.status = Status()
    game.players = check_players()
    cmd = Command()
    
    #start
    log_this("system", "The game has been initialized.")
    prints("werewolves - game master tool", "title")

    # -- UPDATING CURRENT STATUS

    if game.status.phase == "setup" or game.status.phase == "day":
        game.status.show()
        show_players()
    
    elif game.status.phase == "day":
        prints(f"down of day {game.status.day}.", "stitle")
        game.status.show()
        show_players()
    
    elif game.status.phase == "night":
        prints(f"night {game.status.day} has begun, eye closed!", "stitle")

        if game.status.turn == "priest":
            priest()
   
    while True:
        #listen for commands
        cmd.ins()
             
        #exit game
        if cmd.query == "exit":
            prints("Exiting the game...", "body")
            break
    
if __name__ == "__main__":
    main()
    
#from db import setup_database
#from models import get_day, list_players, change_day, change_name, change_role, change_active, change_alive, change_romeo, add_death_list
#from game_actions import kill_player, remove_player, add_player
#from events import night_zero, vote
#from roles import madman_turn
#from log import print_log, purge_log

#TO IMPROVE:
#minor:
# - if the vote results is a single player, bypass the ballot;
# - use class;
# - create def wolf 3;
# - better log system;
# - add flags to the commands;
# - modify listing system (list only alive / only dead);
# - error prevention;
# - more chances for wolves and vampire in case of dead selection;
# - for characters like the healer or the major, their turn doesn't start if they are on the death list / in ballot;
# - general refactoring (again).
#major:
# - create a GUI;
# - add language pack;
# - add winning system;
# - add schizophrenic mode.

#def main():
#    setup_database()

#    print("\n=== WEREWOLVES GAME master ===")
#    while True:
#        day = get_day()
#        print(f"\nday {day} — Current status:")
#        list_players(show_all=True)

#        cmd = input("> ").strip().lower()

#        if cmd == "exit":
#            print(" Exiting game.")
#            break

#        elif cmd == "log":
#            print_log()

#        elif cmd == "logpurge":
#            purge_log()

        #player managment
#        elif cmd == "add":
#            name = input(" Name > ")
#            add_player(name, day)

#        elif cmd == "remove":
#            pid = int(input(" Player ID? > "))
#            remove_player(pid, day)

        #change game variables
#        elif cmd == "chday":
#            new_day = int(input(" New day? > "))
#            change_day(day, new_day)

#        elif cmd == "chname":
#            pid = int(input(" Player ID? > "))
#            name = input(" New name? > ")
#            change_name(pid, name, day)
        
#        elif cmd == "chrole":
#            pid = int(input(" Player ID? > "))
#            change_role(pid, day)

#        elif cmd == "chactive":
#            pid = int(input(" Player ID? > "))
#            change_active(pid, day)

#        elif cmd == "chalive":
#            pid = int(input(" Player ID? > "))
#            change_alive(pid, day)

#        elif cmd == "chromeo":
#            pid = int(input(" Player ID? > "))
#            change_romeo(pid, day)
            
        #madman
        
#        elif cmd == "madman":
#            madman_turn(day)
            
#        elif cmd == "madmankill":
#            if find_player_by_role("Madman"):
#                add_death_list(day, find_player_by_role("Madman"), "by himself")

        #start next event

#        elif cmd == "go":
#            night_zero() if day == 0 else vote(day)
                
#        else:
#            print("\n---Commands---\n add (add a new player to the game);\n chactive (set player active/not active);\n chalive (set player dead/alive);\n chday (change current day);\n chname (change the name of a player);\n chromeo (set player Romeo/not Romeo)\n chrole (change the role of a player);\n exit (exit the program);\n go (Start the next event);\n kill (Cause a player's dead for breaking the rules;\n log (print the current game log);\n logpurge (delete the log);\n madman (the madman has chosen his mystic);\n madmankill (kill the madman for bad playing);\n remove (remove a player from the game).")

#if __name__ == "__main__":
#    main()

