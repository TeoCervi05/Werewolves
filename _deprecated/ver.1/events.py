from db import fetch_one, fetch_all
from models import change_day, find_player_by_role, add_vote_list, add_death_list, commit_death_list
from roles import *

# ---day---

def ballot(day, ballot_list):
    valid = 0
    while valid == 0:
        ress = fetch_all("SELECT name FROM players WHERE alive = ?", (1,))
        village_list = []
        for v in ress:
            village_list.append(v["name"])
        total = len(village_list) - len(ballot_list)
        winner = add_vote_list(day, "ballot", ballot_list, total + 1) if merchant_turn(day, ballot_list) else add_vote_list(day, "ballot", ballot_list, total + 1)
        print(f"\n Result:")
        for w in winner:
            print(f"  {w}")
        cmd = input()
        if winner == [] or len(winner) > 1:
            cmd = input("\n Repeat the ballot? (y/n) > ")
            if not cmd == "y":
                return None
        else:
            print()
            winner[0] = orator_turn(day, winner[0])
            winner[0] = major_turn(day, winner[0])
            return winner[0]

def vote(day):
    valid = 0
    winner = None
    while valid == 0:
        ress = fetch_all("SELECT name FROM players WHERE alive = ?", (1,))
        ballot_list = []
        for b in ress:
            ballot_list.append(b["name"])
        total = len(ballot_list)
        ballot_list = add_vote_list(day, "vote", ballot_list, total + 1) if merchant_turn(day) else add_vote_list(day, "vote", ballot_list, total)
        print("\n Results:")
        for b in ballot_list:
            print(f"  {b}")
        cmd = input()
        if ballot_list == [] or len(ballot_list) == total:
            cmd = input(" Repeat the vote? (y/n) > ")
            if not cmd == "y":
                if find_player_by_role("Madman"):
                    cmd = input(" Has the MADMAN declared as a mystic? (y/n) > ")
                    if cmd == "y":
                        madman_turn(day)
                    elif day == 2:
                        add_death_list(day, find_player_by_role("Madman"), "by himself")
            valid = 1
        else:
            print()
            ballot_list = lawyer_turn(day, ballot_list)
            cmd = input("Discussion...")
            if find_player_by_role("Madman"):
                cmd = input(" Has the MADMAN declared as a mystic? (y/n) > ")
                if cmd == "y":
                    madman_turn(day)
                elif day == 2:
                    add_death_list(day, find_player_by_role("Madman"), "by himself")
            winner = ballot(day, ballot_list)
            valid = 1
    if winner:
        add_death_list(day, winner, "by the stake")
        commit_death_list()
    night(day)

# --- night ---

def end_night(day, black_soul):
    print(f"--- END OF night {day} ---\n")
    deaths = commit_death_list()
    if deaths:
        print(", ".join(deaths), "founded dead on the road.")
    else:
        print(" No corpses on the road!")
    innkeeper_turn(black_soul)
    cmd = input()
    change_day(day, day + 1)
    
def night(day):
    print(f"\n--- night {day} HAS BEGUN, EYES CLOSED ---\n")
    execute_commit("DELETE FROM deathlist")
    black_soul = psychic_turn(day)
    mage_turn(day)
    medium_turn(day)
    protection = witch_turn(day)
    vampire_turn(day)
    wolves_turn(day, protection)
    healer_turn(day)
    end_night(day, black_soul)

def night_zero():
    #check init conditions
    total = fetch_one("SELECT COUNT(*) FROM players")[0]
    psychic = find_player_by_role("Psychic")
    wolf1 = find_player_by_role("Wolf 1")
    wolf2 = find_player_by_role("Wolf 2")
    if total < 8 or not psychic or not wolf1 or not wolf2:
        print(" The game can't start, initial conditions not met.")
        return
    #start
    print("\n--- night 0 HAS BEGUN, EYES CLOSED ---\n")
    priest_turn()
    vampire_slayer_turn()
    juliet_turn()
    guards_turn()
    vampire_ghoul_turn()
    wolves_meeting_turn()
    black_soul = psychic_turn(0)
    mage_turn(0)
    end_night(0, black_soul)
