from db import fetch_one, fetch_all, execute_commit
from log import log_this
from settings import *

# --- day utilities ---
def get_day():
    #Create table if empty, else continue the game
    day = fetch_one("SELECT value FROM day LIMIT 1")
    if day:
        return day["value"]
    execute_commit("INSERT INTO day (value) VALUES (0)")
    return 0

def change_day(old_day, new_day):
    execute_commit("UPDATE day SET value = ? WHERE value = ?", (new_day, old_day))
    print(f"\nRise of day {new_day}.")
    log_this(old_day, "day CHANGED", f"day changed to {new_day}.")

# --- Player utilities ---

def list_players(show_all=False, prefix=""):
    players = fetch_all("SELECT * FROM players ORDER BY id ASC")
    for p in players:
        marker = " " if p["alive"] else "X"
        base = f" {prefix}[{p['id']}] {marker} {p['name']}"
        if show_all:
            status = "(Activated)" if p["active"] else ""
            romeo = "(Romeo)" if p["romeo"] else ""
            print(f"{base}: {p['role']} {status} {romeo} ({p['soul']} - {p['faction']})")
        else:
            print(base)
    print()
    
def list_roles(show_all=False):
    if show_all:
        for r in role_list_complete:
            print(f" [{r[0]}] {r[1]} ({r[2]} - {r[3]})")
    else:
        for r in role_list:
            print(f" [{r[0]}] {r[1]} ({r[2]} - {r[3]})")
    print()
    
def list_madman_roles():
    for r in madman_list:
        print(f" [{r[0]}] {r[1]}")

def find_player_by_role(role):
    res = fetch_one("SELECT name FROM players WHERE role = ? LIMIT 1", (role,))
    return res["name"] if res else None

def find_player_by_id(pid):
    res = fetch_one("SELECT name FROM players WHERE id = ? LIMIT 1", (pid,))
    return res["name"] if res else None
    
def find_players_by_role(role):
    ress = fetch_all("SELECT name FROM players WHERE role = ?", (role,))
    res = []
    for r in ress:
        res.append(r["name"])
    return res

def find_role_by_player(name):
    res = fetch_one("SELECT role FROM players WHERE name = ? LIMIT 1", (name,))
    return res["role"] if res else None

def is_alive_by_name(name):
    res = fetch_one("SELECT alive FROM players WHERE name = ? LIMIT 1", (name,))
    return res["alive"] if res else 0

def is_alive_by_role(role):
    res = fetch_one("SELECT alive FROM players WHERE role = ? LIMIT 1", (role,))
    return res["alive"] if res else 0

def is_active_by_name(name):
    res = fetch_one("SELECT active FROM players WHERE name = ? LIMIT 1", (name,))
    return res["active"] if res else 0

def active_player(day, name):
    execute_commit("UPDATE players SET active = ? WHERE name = ?", (1, name,))
    log_this(day, "PLAYER UPDATED", f"{name} has been activated")

def check_soul(name):
    res = fetch_one("SELECT soul FROM players WHERE name = ? LIMIT 1", (name,))
    return res["soul"] if res else ""

# --- Player managment ---

def change_name(pid, new_name, day):
    old_name = find_player_by_id(pid)
    if not old_name:
        print(" Player not found.")
        return
    execute_commit("UPDATE players SET name = ? WHERE id = ?", (new_name, pid))
    log_this(day, "PLAYER UPDATED", f"{old_name} has changed name to {new_name}.")
    print(f" {old_name} has changed name to {new_name}.")

def change_role(pid, day):
    name = find_player_by_id(pid)
    if not name:
        print(" Player not found.")
        return
    list_roles(True)
    cmd = int(input(" Role > "))
    row = role_list_complete[cmd - 1]
    execute_commit(
        "UPDATE players SET role = ?, soul = ?, faction = ? WHERE id = ?",
        (row[1], row[2], row[3], pid)
    )
    log_this(day, "PLAYER UPDATED", f"{name} has changed role to {row[1]}.")
    print(f" {name} has changed role to {row[1]}.")

def change_active(pid, day):
    name = find_player_by_id(pid)
    if not name:
        print(" Player not found.")
        return
    active = fetch_one("SELECT active FROM players WHERE id = ? LIMIT 1", (pid,))[0]
    if active == 0:
        active = 1
    else:
        active = 0
    execute_commit("UPDATE players SET active = ? WHERE id = ?", (active, pid,))
    log_this(day, "PLAYER UPDATED", f"{name} has is active parameter set to {active}")

def change_alive(pid, day):
    name = find_player_by_id(pid)
    if not name:
        print(" Player not found.")
        return
    alive = fetch_one("SELECT alive FROM players WHERE id = ? LIMIT 1", (pid,))[0]
    if not alive:
        alive = True
    else:
        alive = False
    execute_commit("UPDATE players SET alive = ? WHERE id = ?", (alive, pid,))
    log_this(day, "PLAYER UPDATED", f"{name} has is alive parameter set to {alive}")

def change_romeo(pid, day):
    name = find_player_by_id(pid)
    if not name:
        print(" Player not found.")
        return
    romeo = fetch_one("SELECT romeo FROM players WHERE id = ? LIMIT 1", (pid,))[0]
    if romeo == 0:
        romeo = 1
    else:
        romeo = 0
    execute_commit("UPDATE players SET romeo = ? WHERE id = ?", (romeo, pid,))
    log_this(day, "PLAYER UPDATED", f"{name} has is Romeo parameter set to {romeo}")
    
# --- vote list management ---

def add_vote_list(day, phase, voting_list, total):
    execute_commit("DELETE FROM votes")
    print(f"--- {phase.upper()} {day} HAS BEGUN, EYES CLOSED! ---\n")
    log_this(day, f"{phase.upper()}", f"{phase} {day} has begun.")
    print(f" Expected {total} votes:")
    check = 0
    for v in voting_list:
        cmd = int(input(f"  votes for {v}? > "))
        check = check + cmd
        execute_commit("INSERT INTO votes (name, votes) VALUES (?, ?)", (v, cmd))
    if check == total:
        ress = fetch_all("SELECT name FROM votes WHERE votes = (SELECT MAX(votes) FROM votes)")
        winners = []
        for r in ress:
            winners.append(r["name"])
        if phase == "vote":
            for w in winners:
                execute_commit("DELETE FROM votes WHERE name = ?", (w,))
            ress = fetch_all("SELECT name FROM votes WHERE votes = (SELECT MAX(votes) FROM votes)")
            for r in ress:
                winners.append(r["name"])
        return winners
    print(" The vote is not valid.")
    return []

# --- Death list management ---

def list_deaths():
    deaths = fetch_all("SELECT * FROM deathlist ORDER BY id ASC")
    for d in deaths:
        print(f" [{d['id']}] {d['name']}")
    print()

def add_death_list(day, name, cause, secondary = 1):
    if fetch_one("SELECT role FROM players WHERE name = ? LIMIT 1", (name,))["role"] == "Harlot" and cause == "by the stake":
        print(f" The HARLOT ( {name} ) can't be killed by the stake.")
        log_this(day, "HARLOT", "The HARLOT can't be killed by the stake.")
        return
    if fetch_one("SELECT role FROM players WHERE name = ? LIMIT 1", (name,))["role"] == "Wolf 3" and cause == "by the stake":
        #The following code was meant to be def wolf3_turn()
        valid = 0
        while not valid:
            list_players()
            cmd = int(input("  kill someone. (id, 0 to pass) > "))
            if cmd == 0:
                print("  Wolf 3 has died alone (stupid).")
                valid = 1
            if not is_alive_by_name(find_player_by_id(cmd)):
                print("  Seriously?")
            else:
                victim = find_player_by_id(cmd)
                add_death_list(day, victim, "by WOLF 3")
                valid = 1
    execute_commit("INSERT INTO deathlist (name) VALUES (?)", (name,))
    print(f" {name} has been killed {cause}.")
    log_this(day, "DEAD", f"{name} has been killed {cause}.")
    if secondary:
        if fetch_one("SELECT role FROM players WHERE name = ? LIMIT 1", (name,))["role"] == "Juliet":
            romeo = fetch_one("SELECT name FROM players WHERE romeo = ? LIMIT 1", (1,))
            add_death_list(day, romeo["name"], "indirectly", 0)
        if fetch_one("SELECT romeo FROM players WHERE name = ? LIMIT 1", (name,))["romeo"]:
            juliet = fetch_one("SELECT name FROM players WHERE role = ? LIMIT 1", ("Juliet",))
            add_death_list(day, juliet["name"], "indirectly", 0)
            
def remove_death_list(name):
    if not name:
        print(" Player not found.")
        return
    execute_commit("DELETE FROM deathlist WHERE name = ?", (name,))

def commit_death_list():
    ress = fetch_all("SELECT name FROM deathlist")
    res = []
    for r in ress:
        res.append(r["name"])
        execute_commit("UPDATE players SET alive = 0 WHERE name = ?", (r["name"],))
    execute_commit("DELETE FROM deathlist")
    return res
