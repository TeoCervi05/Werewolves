import data
from db import *
from log import log_this
from format import prints

def pull():
    try:
        backup_players = []

        for n in fetch_all("SELECT name FROM players ORDER BY id ASC"):
            att = fetch_one("SELECT role, soul, faction, active, romeo, alive FROM players WHERE name = ?", (n[0],))
            backup_players.append(Player(n[0], att[0], att[1], att[2], att[3], att[4], att[5]))

        return backup_players
    
    except:
        return []

# -- PLAYER LIST ACTIONS --

def insert(name, role, soul, faction):
    execute_commit("INSERT INTO players (name, role, soul, faction) VALUES (?, ?, ?, ?)", (name.upper(), role, soul, faction))
    log_this("players", f"{name.upper()} joined the game as {role}.")
    return Player(name.upper(), role, soul, faction, 0, 0, 1)

def remove(name):
    execute_commit("DELETE FROM players WHERE name = ?", (name.upper(),))
    log_this("players", f"{name.upper()} has been removes from the game.")
    game.players = pull()

def show_all():
    prints(f"day {game.status.day}:", "head")

    if not game.players == []:
        for p in game.players:
            p.show()
        return
    
    prints("There are no players in the list, yet...","body")

# -- CHECK --

def check_name(name):
    for l in game.players:
        if l.name == name:
            return True
    return False

def check_role(role):
    for l in game.players:
        if l.role == role and not role in ["PEASANT", "GUARD", "GUARD (CORRUPTED)"]:
            return True
    return False

# -- FIND --

def player_by_role(role, caller = None):
    if not caller:
        caller = role

    for l in game.players:
        if l.role == role:
            if l.alive:
                return l.name
            log_this(caller, f"The {role} is dead")
            prints(f"The {role} is dead", "body")
            return None

    log_this(caller, f"The {role} is not in the game")
    prints(f"The {role} is not in the game", "body")
    return None

class Player:
    def __init__(self, name, role, soul, faction, active, romeo, alive):
        self.name = name
        self.role = role
        self.soul = soul
        self.faction = faction
        self.active = active
        self.romeo = romeo
        self.alive = alive

    def push(self):
        pass
        #execute_commit("UPDATE status SET day = ?, phase = ?, turn = ? WHERE id = ?", (self.day, self.phase, self.turn, 1))
        #execute_commit("INSERT INTO players SET (name = ?, role = ?, soul = ?, faction = ?, active = ?, romeo, alive)", (self.day, self.phase, self.turn, 1))

    #def push(self):
        #execute_commit("UPDATE players SET name = ?, role = ?, soul = ?, faction = ?, active = ?, romeo = ?,  WHERE id = ?", (self.day, self.phase, self.turn, 1))

    def show(self):
        dead = "" if self.alive else "X"
        used = "(active)" if self.active else ""
        engaged = "(Romeo)" if self.romeo else ""
        
        prints(f"{dead} {self.name} - {self.role} ({self.soul}, {self.faction}) {engaged} {used}", "bull")