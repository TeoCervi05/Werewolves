from data.db import fetch_all, fetch_one, execute_commit
from utils.log import log_this
from utils.format import prints

def pull():
    """
    Pull all players from the database in a single query and return a list of Player objects.
    """

    players = []

    for n in fetch_all("SELECT name FROM players ORDER BY id ASC"):
        row = fetch_one(
            "SELECT role, soul, faction, active, romeo, alive FROM players WHERE name = ?",
            (n[0],)
        )
        players.append(Player(
            n[0], row[0], row[1], row[2], row[3], row[4], row[5]
        ))

    return players

# -- PLAYER LIST ACTIONS --

def insert(name, role, soul, faction, game):
    # Store name uppercase in DB for consistent comparisons
    execute_commit(
        "INSERT INTO players (name, role, soul, faction) VALUES (?, ?, ?, ?)",
        (name.upper(), role, soul, faction))
    log_this("players", f"{name.upper()} joined as {role}.", game.status.day)

    player = Player(name.upper(), role, soul, faction, 0, 0, 1)
    game.players.append(player)
    return player

def remove(name, game):
    execute_commit("DELETE FROM players WHERE name = ?", (name.upper(),))
    log_this("players", f"{name.upper()} has been removed", game.status.day)
    game.players[:] = pull()

def show_all(players):
    if not players:
        prints("There are no players in the list yet...", "body")
        return

    for p in players:
        p.show()

# -- CHECK --

def check_name(name, players):
    # Normalize input and compare uppercase names
    name = name.upper()
    return any(p.name == name for p in players)

def check_role(role, players):
    # Check if a role is already assigned (special-case some multiple roles)
    for p in players:
        if p.role == role and role not in ["PEASANT", "GUARD", "GUARD (CORRUPTED)"]:
            return True
    return False

# -- FIND --

def player_by_role(game, role, caller=None):
    """
    Find a player by role. If the player exists and is alive, return the player's name.
    If not present or dead, log and print a message attributed to caller (if provided).
    """
    if caller is None:
        caller = role

    for p in game.players:
        if p.role == role:
            if p.alive:
                return p.name
            prints(f"The {role} is dead", "body")
            log_this(caller, f"{role} is dead", game.status.day)
            return None

    prints(f"The {role} is not in the game", "body")
    log_this(caller, f"{role} is not in the game", game.status.day)
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

    def show(self):
        dead = "" if self.alive else "X"
        used = "(active)" if self.active else ""
        engaged = "(Romeo)" if self.romeo else ""

        prints(f"{dead} {self.name} - {self.role} ({self.soul}, {self.faction}) {engaged} {used}", "bullet")