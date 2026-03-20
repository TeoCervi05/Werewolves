import data
from format import *
from db import delete_database
from players import insert, remove, check_name, check_role
from players import show_all as show_players
from characters import *
from log import *

def clear(params):
    if len(params) == 0:
        #clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        return
    
    if len(params) == 1:
        #get help
        if params[0] == "-h" or params[0] == "-help":
            printh(
                "clear",
                "use \"clear\" to erase the screen.",
                "clear",
                [None]
            )
            return
    
        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return
    
    prints(f"\"clear\" only accept 1 tag, {len(params)} were given", "err")
    
def exit(params):
    if len(params) == 0:
        #exit the game (break the main loop)
        log_this("system", "the game has been terminated.")
        return "exit"

    if len(params) == 1:
        #delete the database (use at the end of the session)
        if params[0] == "-d" or params[0] == "-delete":
            prints("Deleting database...", "body")
            delete_database()
            log_this("system", "database has been deleted.")
            log_this("system", "the game has been terminated.")
            return "exit"

        #get help
        if params[0] == "-h" or params[0] == "-help":
            printh(
                "exit",
                "\"exit\" is used to close the program. By default, all the changes are stored for the next session.",
                "exit {tag}",
                [["-d (-delete)", "If your game session is over, use the \"-d\" tag to delete the game database; It can also be removed manually by deleting the \"game.db\" file in the directory."]]
            )
            return ""
        
        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return ""
    
    prints(f"\"exit\" only accept 1 tag, {len(params)} were given", "err")
                    
def help(params):
    if len(params) == 0:
        #print all the query with a simple descripion
        prints(f"avaible queries ({game.status.phase} actions):", "head")
        if game.status.phase == "setup":
            prints(data.setup_ACTIONS, "bull")
            return
        
        prints("coming soon...", "body") #add in future
        return
    
    if len(params) == 1:
        #get help (show how to use the -h tag)
        if params[0] == "-h" or params[0] == "-help":
            printh(
                "help",
                "The \"help\" command prints a list of all the avaible queries with an essential description for each of them.",
                "help {tag}",
                [["-h (-help)", "The \"-h\" tag can be used after every query: it is used to print addictional infos about the selected command, including syntax and parameters."]]
            )
            return
        
        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return
    
    prints(f"\"help\" only accept 1 tag, {len(params)} were given", "err")

def log(params):
    #print log
    if len(params) == 0:
        prints("log:", "head")
        logt = print_log()
        prints(logt[0], logt[1])
        return

    if len(params) == 1:
        #delete log
        if params[0] == "-d" or params[0] == "-delete":
            res = delete_log()
            prints(res[0], res[1])
            return

        #get help
        if params[0] == "-h" or params[0] == "-help":
            printh(
                "log",
                "Show the content of the log.txt file white the \"log\" command. If not in the directory, the file is created at the start of the application.",
                "log {tag}",
                [["-d (-delete)", "Delete log.txt. This action is performed automatically at the start of each session."]]
            )
            return

        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return
    
    prints(f"\"log\" only accept 1 tag, {len(params)} were given", "err")

def next(params):
    if len(params) == 0:
        #next phase
        if game.status.phase == "setup":
            game.status.phase = "night"
            game.status.push()
            prints(f"night {game.status.day} has begun, eye closed!", "stitle")
            if game.status.day == 0:
                game.status.turn = "priest"
                priest()
            return
    
    if len(params) == 1:
        #get help
        if params[0] == "-h" or params[0] == "-help":
            printh(
                "next",
                "proceed to the next phase, it may be necessary to confirm this action.",
                "next",
                [None]
            )
            return
    
        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return
    
    prints(f"\"next\" only accept 1 tag, {len(params)} were given", "err")

def player(params):
    #TO ADD:
    #-c (-change): change the name or the role of a player (-n = name -r = role)
    #-s (-status): turn on/off status switches of a player (-u = active -r = romeo -a = alive)

    #print players list
    if len(params) == 0:
        show_players()
        return

    if len(params) == 1:
        #add a new player
        if params[0] == "-a" or params[0] == "-add":
            if game.status.phase == "setup":
                name = printq("What's the name of the player?")
                if check_name(name):
                    prints(f"{name} is already in the game", "err")
                    return
                for l in game.players:
                    if l.name == name.upper():
                        prints(f"{name.upper()} is already in the game", "err")
                        return
                print()
                for r in data.ROLE_LIST:
                    prints(f"[{r[0]}] {r[1]}", "bull")
                role = printq("What character he/she's gonna play?", "range", 1, 32)
                if check_role(role):
                    prints(f"{name} is already in the game", "err")
                    return
                game.players.append(insert(name, data.ROLE_LIST[role - 1][1], data.ROLE_LIST[role - 1][2], data.ROLE_LIST[role - 1][3]))
                show_players()
                return
            
            prints("new players can be added only during the setup phase", "err")
            return

        #get help
        if params[0] == "-h" or params[0] == "-help":
            printh(
                "player",
                "This query is used to operate with the list of players, whitout any tag it only prints the players list.",
                "player {tag} {infos 1} {infos 2}",
                [["-a (-add)", "Add a new player to the game: this tag can be completed with the player informations showed in the syntax section (the \"role\" parameter can be max two words long). If not given, the program will ask for the name and the role of the player, that is the only way to add one word longer names;"], ["-r (-remove)", "Remove a player from the game: this tag can be completed with the player's name; if not given, the program will ask for it."]]
            )
            return

        #remove a player
        if params[0] == "-r" or params[0] == "-remove":
            if game.status.phase == "setup":
                name = printq("Who is going to be removed?")
                remove(name)
                show_players()
                return
            
            prints("players can be removed only during the setup phase", "err")
            return

        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return

    if len(params) == 2:
        #add a new player with name
        if params[0] == "-a" or params[0] == "-add":
            if game.status.phase == "setup":
                name = params[1].upper()
                if check_name(name):
                    prints(f"{name} is already in the game", "err")
                    return
                for r in data.ROLE_LIST:
                    prints(f"[{r[0]}] {r[1]}", "bull")
                role = printq("What character he/she's gonna play?", "range", 1, 32)
                game.players.append(insert(name, data.ROLE_LIST[role - 1][1], data.ROLE_LIST[role - 1][2], data.ROLE_LIST[role - 1][3]))
                show_players()
                return
            
            prints("new players can be added only during the setup phase", "err")
            return

        #remove a player
        if params[0] == "-r" or params[0] == "-remove":
            if game.status.phase == "setup":
                remove(params[1])
                show_players()
                return
            
            prints("players can be removed only during the setup phase", "err")
            return

        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return

    if len(params) == 3:
        #add a new player with name and role
        if params[0] == "-a" or params[0] == "-add":
            if game.status.phase == "setup":
                name = params[1].upper()
                if check_name(name):
                    prints(f"{name} is already in the game", "err")
                    return
                role = params[2].upper()
                if check_role(role):
                    prints(f"{role} is already in the game", "err")
                    return
                if role in data.CHECK_ROLE_LIST():
                    name = params[1]
                    for r in data.ROLE_LIST:
                        if r[1] == role:
                            soul = r[2]
                            faction = r[3]
                            break
                    game.players.append(insert(name, role, soul, faction))
                    show_players()
                    return

                prints("the chosen role is not valid", "err")
                return
            
            prints("new players can be added only during the setup phase", "err")
            return
        
        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return

    if len(params) == 4:
        #add a new player with name and role (2 words)
        if params[0] == "-a" or params[0] == "-add":
            if game.status.phase == "setup":
                role = f"{params[2]} {params[3]}".upper()
                if check_role(role):
                    prints(f"{role} is already in the game", "err")
                    return
                if role in data.CHECK_ROLE_LIST():
                    name = params[1].upper()
                    for l in game.players:
                        if l.name == name:
                            prints(f"{name} is already in the game", "err")
                            return
                    for r in data.ROLE_LIST:
                        if r[1] == role:
                            soul = r[2]
                            faction = r[3]
                            break
                    game.players.append(insert(params[1], role, soul, faction))
                    show_players()
                    return

                prints("the chosen role is not valid", "err")
                return
            
            prints("new players can be added only during the setup phase", "err")
            return
        
        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return

    prints(f"\"player\" only accept 1 tags and 2 parameter, {len(params)} inputs were given", "err")

def status(params):
    if len(params) == 0:
        #print current status (day, phase, turn)
        game.status.show()
        return

    if len(params) == 1:
        #modify a value
        if params[0] == "-c" or params[0] == "-change":
            while True:
                ans = printq("Wich value is to be modified?", "list", opt = ["Day", "Phase", "Turn"])

                #modify day
                if ans == "Day":
                    game.status.day = printq("New day?", "int")
                    game.status.push()
                    prints(f"Day has been changed to {game.status.day}.")
                    log_this("status", f"Day has been changed to {game.status.day}.")
                    return

                #modify phase
                if ans == "Phase":
                    game.status.phase = printq("New phase?", "list", opt = game.status_TIME)
                    if game.status.phase == "setup" or game.status.phase == "day":
                        game.status.turn = "master"
                    elif game.status.phase == "vote" or game.status.phase == "village":
                        game.status.turn = "village"
                    elif game.status.phase == "night" and game.status.day == 0:
                        game.status.turn = "priest"
                    else:
                        game.status.turn = "psychic"
                    game.status.push()
                    prints(f"Phase has been changed to {game.status.phase}.")
                    log_this("status", f"Phase has been changed to {game.status.phase}.")
                    return

                #modifty turn
                if ans == "Turn":
                    if game.status.phase == "night" and game.status.day == 0:
                        game.status.turn = printq("New turn?", "list", opt = data.ACTIVES_NIGHT_ZERO)
                    elif game.status.phase == "night":
                        game.status.turn = printq("New turn?", "list", opt = data.ACTIVES_NIGHT)
                    elif game.status.phase == "vote":
                        game.status.turn = printq("New turn?", "list", opt = data.ACTIVES_VOTE)
                    elif game.status.phase == "ballot":
                        game.status.turn = printq("New turn?", "list", opt = data.ACTIVES_BALLOT)
                    else:
                        prints("turn cannot be changed, only the master can act in this phase...", "err")
                        return
                    game.status.push()
                    prints(f"Turn has been changed to {game.status.turn}.")
                    log_this("status", f"Turn has been changed to {game.status.turn}.")
                    return

        #get help
        if params[0] == "-h" or params[0] == "-help":
            printh(
                "status",
                "To show the game status, namely the common variables of the session, use the \"status\" query. Three values (one int and two strings) are printed: \"day\", intuitively, refers to the current in-game day (day 0 is the setup step); \"phase\" shows the actual phase of the game (day, vote, ballot, night); \"turn\" express wich character is supposed to act in that moment (could be a specific one, a group, all the players or even the master).",
                "status {tag 1} {tag 2} {values}",
                [["-c (-change)", "Use the \"-c\" tag to modify one of the variables, if not followed by another tag an a value, it will ask for specifications;"], ["-c -d (-change -day)", "Used to change day value. It can be completed with an int parameter;"], ["-c -p (-change -phase)", "Used to change the phase value. It can be completed with a string parameter, chosen from \"setup\", \"day\", \"vote\", \"ballot\" or \"night\";"], ["-c -t (-change -turn)", "Used to change turn value. It can be completed with a string value, may it be an active character, a group (for example, wolves) or even the Master itself;"]]
            )
            return

        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return

    if len(params) == 2:
        if params[0] == "-c" or params[0] == "-change":
            
            #change day
            if params[1] == "-d" or params[1] == "-day":
                game.status.day = printq("New day?","int")
                game.status.push()
                prints(f"day has been changed to {game.status.day}.")
                log_this("status", f"day has been changed to {game.status.day}.")
                return

            #change phase
            if params[1] == "-p" or params[1] == "-phase":
                game.status.phase = printq("New phase?", "list", opt = game.status_TIME)
                if game.status.phase == "setup" or game.status.phase == "day":
                    game.status.turn = "master"
                elif game.status.phase == "vote" or game.status.phase == "village":
                    game.status.turn = "village"
                elif game.status.phase == "night" and game.status.day == 0:
                    game.status.turn = "priest"
                else:
                    game.status.turn = "psychic"
                game.status.push()
                prints(f"phase has been changed to {game.status.phase}.")
                log_this("status", f"phase has been changed to {game.status.phase}.")
                return
            
            #change turn
            if params[1] == "-t" or params[1] == "-turn":
                if game.status.phase == "night" and game.status.day == 0:
                    game.status.turn = printq("New turn?", "list", opt = data.ACTIVES_NIGHT_ZERO)
                elif game.status.phase == "night":
                    game.status.turn = printq("New turn?", "list", opt = data.ACTIVES_NIGHT)
                elif game.status.phase == "vote":
                    game.status.turn = printq("New turn?", "list", opt = data.ACTIVES_VOTE)
                elif game.status.phase == "ballot":
                    game.status.turn = printq("New turn?", "list", opt = data.ACTIVES_BALLOT)
                else:
                    prints("turn cannot be changed, only the master can act in this phase...", "err")
                    return
                game.status.push()
                prints(f"turn has been changed to {game.status.turn}.")
                log_this("status", f"turn has been changed to {game.status.turn}.")
                return

            prints(f"\"{params[1]}\" is not a valid parameter", "err")
            return

        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return

    if len(params) == 3:
        if params[0] == "-c" or params[0] == "-change":
            
            #change day
            if params[1] == "-d" or params[1] == "-day":
                try:
                    game.status.day = int(params[2])
                    prints(f"day has been changed to {game.status.day}.")
                    log_this("status", f"day has been changed to {game.status.day}.")
                except:
                    prints("an \"int\" value was expected", "err")
                game.status.push()
                return

            #change phase
            if params[1] == "-p" or params[1] == "-phase":
                if params[2].lower() in game.status_TIME:
                    game.status.phase = params[2].lower()
                    if game.status.phase == "setup" or game.status.phase == "day":
                        game.status.turn = "master"
                    elif game.status.phase == "vote" or game.status.phase == "village":
                        game.status.turn = "village"
                    elif game.status.phase == "night" and game.status.day == 0:
                        game.status.turn = "priest"
                    else:
                        game.status.turn = "psychic"
                    game.status.push()
                    prints(f"phase has been changed to {game.status.phase}.")
                    log_this("status", f"phase has been changed to {game.status.phase}.")
                    return
                prints(f"phase {params[2]} is not a valid option", "err")
                return
            
            #change turn
            if params[1] == "-t" or params[1] == "-turn":
                if game.status.phase == "night" and game.status.day == 0:
                    if params[2].lower() in data.ACTIVES_NIGHT_ZERO:
                        pass
                    else:
                        prints(f"turn \"{params[2]}\" is not a valid option", "err")
                        return
                elif game.status.phase == "night":
                    if params[2].lower() in data.ACTIVES_NIGHT:
                        pass
                    else:
                        prints(f"turn \"{params[2]}\" is not a valid option", "err")
                        return
                elif game.status.phase == "vote":
                    if params[2].lower() in data.ACTIVES_VOTE:
                        pass
                    else:
                        prints(f"turn \"{params[2]}\" is not a valid option", "err")
                        return
                elif game.status.phase == "ballot":
                    if params[2].lower() in data.ACTIVES_BALLOT:
                        pass
                    else:
                        prints(f"turn \"{params[2]}\" is not a valid option", "err")
                        return
                else:
                    prints("turn cannot be changed, only the master can act in this phase...", "err")
                    return

                game.status.turn = params[2].lower()
                game.status.push()
                prints(f"turn has been changed to {game.status.turn}.")
                log_this("status", f"turn has been changed to {game.status.turn}.")
                return

            prints(f"\"{params[1]}\" is not a valid parameter", "err")
            return

        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return

    prints(f"\"status\" only accept 2 tags and 1 parameter, {len(params)} inputs were given", "err")

def blanck_command():
    if game.status.phase == "setup" or game.status.phase == "day":
        game.status.show()
        show_players()
        return

class Command:
    def __init__(self):
        self.query = ""
        self.params = ""
    
    def ins(self):
        self.params = printq().split(" ")        
        self.query = self.params[0]
        self.params.pop(0)

        if self.query == "clear":
            clear(self.params)
            return
        
        if self.query == "help":
            help(self.params)
            return
        
        if self.query == "exit":
            self.query = exit(self.params)
            return
        
        if self.query == "log":
            log(self.params)
            return

        if self.query == "next":
            next(self.params)
            return

        if self.query == "player":
            player(self.params)
            return

        if self.query == "status":
            status(self.params)
            return
        
        if self.query == "":
            blanck_command()
            return
        
        prints(f"\"{self.query}\" is not a valid query", "err")