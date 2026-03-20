from db import execute_commit, fetch_all
from models import find_player_by_id, list_roles
from log import log_this
from settings import *

def add_player(name, day):
    list_roles()
    rid = int(input(" Role > "))
    row = role_list[rid - 1]
    execute_commit(
        "INSERT INTO players (name, role, soul, faction) VALUES (?, ?, ?, ?)",
        (name, row[1], row[2], row[3])
    )
    log_this(day, "NEW PLAYER", f"{name} has joined the game as {row[1]}.")

def remove_player(pid, day):
    name = find_player_by_id(pid)
    if not name:
        print(" Player not found.")
        return
    log_this(day, "PLAYER REMOVED", f"{name} is no longer in the game.")
    execute_commit("DELETE FROM players WHERE id = ?", (pid,))
    print(f" Removed {name}.")

def kill_player(pid, day):
    name = find_player_by_id(pid)
    if not name:
        print(" Player not found.")
        return
    log_this(day, "DEAD", f"{name} has been killed by the master.")
    execute_commit("UPDATE players SET alive = 0 WHERE id = ?", (pid,))
    print(f" {name} has been killed by the master.")

