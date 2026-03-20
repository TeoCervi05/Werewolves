from data import data
from data.data import STATUS_TIME
from data.db import delete_database
from core.players import insert, remove, check_name, check_role, show_all
from utils.log import log_this, delete_log, print_log
from utils.format import prints, printq, printh

class Command:
    def __init__(self, game, phase_manager):
        self.game = game
        self.phase_manager = phase_manager
        self.query = ""
        self.params = []

    def show_state(self):
        if self.game.status.phase in ("setup", "day"):
            self.game.status.show()
            print()
            show_all(self.game.players)

    def clear(self, params):
        import os
        if len(params) == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            return

    def exit(self, params):
        if len(params) == 0:
            log_this("system", "game terminated", self.game.status.day)
            return "exit"

        if len(params) == 1 and params[0] in ("-d", "-delete"):
            delete_database()
            log_this("system", "database delected", self.game.status.day)
            return "exit"

        prints("Invalid parameter", "err")
        return ""

    def help(self, params):
        prints("coming soon...", "body")

    def log(self, params):
        if len(params) == 0:
            prints("log:", "head")
            log_data, style = print_log()
            prints(log_data, style)
            return
        
        if params[0] in ("-d", "-delete"):
            msg, style = delete_log()
            prints(msg, style)
            return

        prints("Invalid parameter", "err")

    def next(self, params):
        self.phase_manager.next()

    def player(self, params):
        #will be update with a more advanced logic
        prints("Player command editing ongoing...", "body")

    def status(self, params):
        prints("Status command editing ongoing...", "body")

    def ins(self):
        parts = printq().split(" ")
        self.query = parts[0]
        self.params = parts[1:]

        q = self.query

        if q == "":
            self.show_state()
            return

        if q == "clear":
            self.clear(self.params)
            return

        if q == "help":
            self.help(self.params)
            return

        if q == "exit":
            self.query = self.exit(self.params)
            return

        if q == "log":
            self.log(self.params)
            return

        if q == "next":
            self.next(self.params)
            return

        if q == "player":
            self.player(self.params)
            return

        if q == "status":
            self.status(self.params)
            return

        prints(f"\"{q}\" is not a valid query", "err")


















"""

def clear(params):
    if len(params) == 0:
        # clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        return

    if len(params) == 1:
        # get help
        if params[0] in ("-h", "-help"):
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

def exit_cmd(params):
    if len(params) == 0:
        # exit the game (break the main loop)
        log_this("system", "the game has been terminated.", day=getattr(game.status, "day", None))
        return "exit"

    if len(params) == 1:
        # delete the database (use at the end of the session)
        if params[0] in ("-d", "-delete"):
            prints("Deleting database...", "body")
            delete_database()
            log_this("system", "database has been deleted.", day=getattr(game.status, "day", None))
            log_this("system", "the game has been terminated.", day=getattr(game.status, "day", None))
            return "exit"

        # get help
        if params[0] in ("-h", "-help"):
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

def help_cmd(params):
    if len(params) == 0:
        # print all the query with a simple descripion
        prints(f"avaible queries ({game.status.phase} actions):", "head")
        if game.status.phase == "setup":
            prints(data.setup_ACTIONS, "bullet")
            return

        prints("coming soon...", "body")  # add in future
        return

    if len(params) == 1:
        # get help (show how to use the -h tag)
        if params[0] in ("-h", "-help"):
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

def log_cmd(params):
    # print log
    if len(params) == 0:
        prints("log:", "head")
        res = print_log()
        # print_log returns [text, style] as before
        prints(res[0], res[1])
        return

    if len(params) == 1:
        # delete log
        if params[0] in ("-d", "-delete"):
            res = delete_log()
            prints(res[0], res[1])
            return

        # get help
        if params[0] in ("-h", "-help"):
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

def next_cmd(params):
    if len(params) == 0:
        # next phase
        if game.status.phase == "setup":
            game.status.phase = "night"
            game.status.push()
            prints(f"night {game.status.day} has begun, eye closed!", "stitle")
            if game.status.day == 0:
                game.status.turn = "priest"
                priest()
            return

    if len(params) == 1:
        # get help
        if params[0] in ("-h", "-help"):
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

def player_cmd(params):
    # TO ADD:
    # -c (-change): change the name or the role of a player (-n = name -r = role)
    # -s (-status): turn on/off status switches of a player (-u = active -r = romeo -a = alive)

    # print players list
    if len(params) == 0:
        show_players()
        return

    if len(params) == 1:
        # add a new player
        if params[0] in ("-a", "-add"):
            if game.status.phase == "setup":
                name = printq("What's the name of the player?")
                if check_name(name.upper()):
                    prints(f"{name} is already in the game", "err")
                    return
                print()
                for r in data.ROLE_LIST:
                    prints(f"[{r[0]}] {r[1]}", "bullet")
                role = printq("What character he/she's gonna play?", "range", 1, 32)
                if check_role(data.ROLE_LIST[role - 1][1]):
                    prints(f"{name} is already in the game", "err")
                    return
                game.players.append(insert(name, data.ROLE_LIST[role - 1][1], data.ROLE_LIST[role - 1][2], data.ROLE_LIST[role - 1][3]))
                show_players()
                return

            prints("new players can be added only during the setup phase", "err")
            return

        # get help
        if params[0] in ("-h", "-help"):
            printh(
                "player",
                "This query is used to operate with the list of players, whitout any tag it only prints the players list.",
                "player {tag} {infos 1} {infos 2}",
                [["-a (-add)", "Add a new player to the game: this tag can be completed with the player informations showed in the syntax section (the \"role\" parameter can be max two words long). If not given, the program will ask for the name and the role of the player, that is the only way to add one word longer names;"], ["-r (-remove)", "Remove a player from the game: this tag can be completed with the player's name; if not given, the program will ask for it."]]
            )
            return

        # remove a player
        if params[0] in ("-r", "-remove"):
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
        # add a new player with name
        if params[0] in ("-a", "-add"):
            if game.status.phase == "setup":
                name = params[1].upper()
                if check_name(name):
                    prints(f"{name} is already in the game", "err")
                    return
                for r in data.ROLE_LIST:
                    prints(f"[{r[0]}] {r[1]}", "bullet")
                role = printq("What character he/she's gonna play?", "range", 1, 32)
                game.players.append(insert(name, data.ROLE_LIST[role - 1][1], data.ROLE_LIST[role - 1][2], data.ROLE_LIST[role - 1][3]))
                show_players()
                return

            prints("new players can be added only during the setup phase", "err")
            return

        # remove a player
        if params[0] in ("-r", "-remove"):
            if game.status.phase == "setup":
                remove(params[1])
                show_players()
                return

            prints("players can be removed only during the setup phase", "err")
            return

        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return

    if len(params) == 3:
        # add a new player with name and role
        if params[0] in ("-a", "-add"):
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
        # add a new player with name and role (2 words)
        if params[0] in ("-a", "-add"):
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

def status_cmd(params):
    if len(params) == 0:
        # print current status (day, phase, turn)
        game.status.show()
        return

    if len(params) == 1:
        # modify a value
        if params[0] in ("-c", "-change"):
            while True:
                ans = printq("Wich value is to be modified?", "list", opt=["Day", "Phase", "Turn"])

                # modify day
                if ans == "Day":
                    game.status.day = printq("New day?", "int")
                    game.status.push()
                    prints(f"Day has been changed to {game.status.day}.")
                    log_this("status", f"Day has been changed to {game.status.day}.", day=game.status.day)
                    return

                # modify phase
                if ans == "Phase":
                    game.status.phase = printq("New phase?", "list", opt=game.status_TIME)
                    if game.status.phase in ("setup", "day"):
                        game.status.turn = "master"
                    elif game.status.phase in ("vote", "village"):
                        game.status.turn = "village"
                    elif game.status.phase == "night" and game.status.day == 0:
                        game.status.turn = "priest"
                    else:
                        game.status.turn = "psychic"
                    game.status.push()
                    prints(f"Phase has been changed to {game.status.phase}.")
                    log_this("status", f"Phase has been changed to {game.status.phase}.", day=game.status.day)
                    return

                # modifty turn
                if ans == "Turn":
                    if game.status.phase == "night" and game.status.day == 0:
                        game.status.turn = printq("New turn?", "list", opt=data.ACTIVES_NIGHT_ZERO)
                    elif game.status.phase == "night":
                        game.status.turn = printq("New turn?", "list", opt=data.ACTIVES_NIGHT)
                    elif game.status.phase == "vote":
                        game.status.turn = printq("New turn?", "list", opt=data.ACTIVES_VOTE)
                    elif game.status.phase == "ballot":
                        game.status.turn = printq("New turn?", "list", opt=data.ACTIVES_BALLOT)
                    else:
                        prints("turn cannot be changed, only the master can act in this phase...", "err")
                        return
                    game.status.push()
                    prints(f"Turn has been changed to {game.status.turn}.")
                    log_this("status", f"Turn has been changed to {game.status.turn}.", day=game.status.day)
                    return

        # get help
        if params[0] in ("-h", "-help"):
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
        if params[0] in ("-c", "-change"):

            # change day
            if params[1] in ("-d", "-day"):
                game.status.day = printq("New day?", "int")
                game.status.push()
                prints(f"day has been changed to {game.status.day}.")
                log_this("status", f"day has been changed to {game.status.day}.", day=game.status.day)
                return

            # change phase
            if params[1] in ("-p", "-phase"):
                game.status.phase = printq("New phase?", "list", opt=game.status_TIME)
                if game.status.phase in ("setup", "day"):
                    game.status.turn = "master"
                elif game.status.phase in ("vote", "village"):
                    game.status.turn = "village"
                elif game.status.phase == "night" and game.status.day == 0:
                    game.status.turn = "priest"
                else:
                    game.status.turn = "psychic"
                game.status.push()
                prints(f"phase has been changed to {game.status.phase}.")
                log_this("status", f"phase has been changed to {game.status.phase}.", day=game.status.day)
                return

            # change turn
            if params[1] in ("-t", "-turn"):
                if game.status.phase == "night" and game.status.day == 0:
                    game.status.turn = printq("New turn?", "list", opt=data.ACTIVES_NIGHT_ZERO)
                elif game.status.phase == "night":
                    game.status.turn = printq("New turn?", "list", opt=data.ACTIVES_NIGHT)
                elif game.status.phase == "vote":
                    game.status.turn = printq("New turn?", "list", opt=data.ACTIVES_VOTE)
                elif game.status.phase == "ballot":
                    game.status.turn = printq("New turn?", "list", opt=data.ACTIVES_BALLOT)
                else:
                    prints("turn cannot be changed, only the master can act in this phase...", "err")
                    return
                game.status.push()
                prints(f"turn has been changed to {game.status.turn}.")
                log_this("status", f"turn has been changed to {game.status.turn}.", day=game.status.day)
                return

            prints(f"\"{params[1]}\" is not a valid parameter", "err")
            return

        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return

    if len(params) == 3:
        if params[0] in ("-c", "-change"):

            # change day
            if params[1] in ("-d", "-day"):
                try:
                    game.status.day = int(params[2])
                    prints(f"day has been changed to {game.status.day}.")
                    log_this("status", f"day has been changed to {game.status.day}.", day=game.status.day)
                except ValueError:
                    prints("an \"int\" value was expected", "err")
                game.status.push()
                return

            # change phase
            if params[1] in ("-p", "-phase"):
                if params[2].lower() in game.status_TIME:
                    game.status.phase = params[2].lower()
                    if game.status.phase in ("setup", "day"):
                        game.status.turn = "master"
                    elif game.status.phase in ("vote", "village"):
                        game.status.turn = "village"
                    elif game.status.phase == "night" and game.status.day == 0:
                        game.status.turn = "priest"
                    else:
                        game.status.turn = "psychic"
                    game.status.push()
                    prints(f"phase has been changed to {game.status.phase}.")
                    log_this("status", f"phase has been changed to {game.status.phase}.", day=game.status.day)
                    return
                prints(f"phase {params[2]} is not a valid option", "err")
                return

            # change turn
            if params[1] in ("-t", "-turn"):
                if game.status.phase == "night" and game.status.day == 0:
                    if params[2].lower() not in data.ACTIVES_NIGHT_ZERO:
                        prints(f"turn \"{params[2]}\" is not a valid option", "err")
                        return
                elif game.status.phase == "night":
                    if params[2].lower() not in data.ACTIVES_NIGHT:
                        prints(f"turn \"{params[2]}\" is not a valid option", "err")
                        return
                elif game.status.phase == "vote":
                    if params[2].lower() not in data.ACTIVES_VOTE:
                        prints(f"turn \"{params[2]}\" is not a valid option", "err")
                        return
                elif game.status.phase == "ballot":
                    if params[2].lower() not in data.ACTIVES_BALLOT:
                        prints(f"turn \"{params[2]}\" is not a valid option", "err")
                        return
                else:
                    prints("turn cannot be changed, only the master can act in this phase...", "err")
                    return

                game.status.turn = params[2].lower()
                game.status.push()
                prints(f"turn has been changed to {game.status.turn}.")
                log_this("status", f"turn has been changed to {game.status.turn}.", day=game.status.day)
                return

            prints(f"\"{params[1]}\" is not a valid parameter", "err")
            return

        prints(f"\"{params[0]}\" is not a valid parameter", "err")
        return

    prints(f"\"status\" only accept 2 tags and 1 parameter, {len(params)} inputs were given", "err")

def blanck_command():
    if game.status.phase in ("setup", "day"):
        game.status.show()
        show_players()
        return

"""