from db import execute_commit, fetch_one
from models import list_players, list_madman_roles, find_player_by_role, find_player_by_id, find_players_by_role, find_role_by_player, is_alive_by_name, is_alive_by_role, is_active_by_name, check_soul, active_player, add_death_list, remove_death_list, list_deaths
from log import log_this
from settings import *

#Assassin
def assassin_turn(day, role):
    assassin = find_player_by_role("Assassin")
    if assassin and is_alive_by_name(assassin) and not is_active_by_name(assassin):
        print(f" {role.upper()} turn:")
        cmd = input("  Is the ASSASSIN awake? (y/n) > ")
        if cmd == "y":
            mystic = is_alive_by_role(role)
            if mystic:
                victim = find_player_by_role(role)
            else:
                valid = 0
                while not valid:
                    list_players()
                    cmd = int(input(" Kill someone. (id) > "))
                    if not is_alive_by_name(find_player_by_id(cmd)):
                        print("  Seriously?")
                    else:
                        victim = find_player_by_id(cmd)
                        add_death_list(day, victim, "by the ASSASSIN")
                        active_player(day, assassin)
            return mystic
    return 0

#Guards (only night zero)
def guards_turn():
    guards = find_players_by_role("Guard")
    guards.extend(find_players_by_role("Guard (corrupted)"))
    if len(guards) == 0:
        print(" The GUARDS are not in the game.")
        cmd = input()
        return
    print(" GUARDS (", ", ".join(guards), ") turn;\n   All GUARDS recognize each others.")
    log_this(0, "GUARDS", "All GUARDS recognize each others.")
    cmd = input()
    
#Healer
def healer_turn(day):
    healer = find_player_by_role("Healer")
    if not healer:
        print(" The HEALER is not in the game.")
        cmd = input()
        return
    if not is_alive_by_name(healer) or assassin_turn(day, "Healer"):
        print(" The HEALER is dead.")
        cmd = input()
        return
    if is_active_by_name(healer):
        print(f" The HEALER ( {healer} ) has already used his power.")
        cmd = input()
        return
    print(f" HEALER ( {healer} ) turn:")
    list_deaths()
    valid = 0
    while not valid:
        cmd = int(input("  Save someone? (id, 0 to pass) > "))
        if cmd == 0:
            print("  The HEALER decided not to act.")
            log_this(day, "HEALER", "The HEALER decided not to act.")
            cmd = input()
            return
        #if not is_alive_by_name(find_player_by_id(cmd)):
            #print("  Seriously?")
        else:
            saved = fetch_one("SELECT name FROM deathlist WHERE id = ?", (cmd,))
            remove_death_list(saved)
            print(f"  {saved} has been saved by the HEALER.")
            log_this(day, "HEALER", f"{saved} has been saved by the HEALER.")
            active_player(day, healer)
        cmd = input()

#Innkeeper
def innkeeper_turn(black_soul):
    innkeeper = find_player_by_role("Innkeeper")
    if is_alive_by_name(innkeeper) and black_soul:
        print(" Voices at the inn: a black soul was found!")
    else:
        print(" No voices at the inn...")

#Juliet (only night zero)
def juliet_turn():
    juliet = find_player_by_role("Juliet")
    if not juliet:
        print(" The JULIET is not in the game.")
        cmd = input()
        return
    print(f" JULIET ( {juliet} ) turn:")
    valid = False
    while not valid:
        list_players()
        rid = int(input("  Romeo? (id) > "))
        romeo = find_player_by_id(rid)
        if romeo == juliet:
            print("  Seriously?")
            cmd = input()
        elif romeo:
               execute_commit("UPDATE players SET romeo = ? WHERE id = ?", (1, rid,))
               print(f"  The JULIET has chosen {romeo} as ROMEO")
               log_this(0, "JULIET", f"The JULIET has chosen {romeo} as ROMEO")
               cmd = input()
               return
        else:
            print("  Player not found.")
            cmd = input()

#Lawyer
def lawyer_turn(day, ballot_list):
    lawyer = find_player_by_role("Lawyer")
    if not lawyer:
        print(" The LAWYER is not in the game.")
        cmd = input()
        return ballot_list
    if not is_alive_by_name(lawyer):
        print(" The LAWYER is dead.")
        cmd = input()
        return ballot_list
    print(f" LAWYER ( {lawyer} ) turn:")
    count = 0
    for b in ballot_list:
        count += 1
        print(f"   [{count}] {b}")
    cmd = int(input(f"  Remove someone? (id, 0 to continue) > "))
    if cmd == 0:
        print("  The LAWYER decided not to act.")
        log_this(day, "LAWYER", "The LAWYER decided not to act.")
        cmd = input()
        return ballot_list
    print(f"  {ballot_list[cmd - 1]} has been removed from ballot.")
    log_this(day, "LAWYER", f"{ballot_list[cmd - 1]} has been removed from ballot.")
    ballot_list.pop(cmd - 1)
    print("\n  New ballot list:")
    count = 0
    for b in ballot_list:
        count += 1
        print(f"   [{count}] {b}")
    ans = input()
    return ballot_list

#Innkeeper
def madman_turn(day):
    madman = find_player_by_role("Madman")
    if not madman:
        print(" The MADMAN is not in the game.")
        return
    if not is_alive_by_name(madman):
        print(" The MADMAN is dead.")
        return
    list_madman_roles()
    cmd = int(input(f"  Chose a mystic. (id) > "))
    execute_commit("UPDATE players SET role = ? WHERE name = ?", (madman_list[cmd - 1][1], madman))
    print(f"  The MADMAN has become {madman_list[cmd - 1][1]}.")
    log_this(day, "MADMAN", f"The MADMAN has become {madman_list[cmd - 1][1]}.")

#Mage
def mage_turn(day):
    mage = find_player_by_role("Mage")
    if not mage:
        print(" The MAGE is not in the game.")
        cmd = input()
        return
    if not is_alive_by_name(mage) or assassin_turn(day, "Mage"):
        print(" The MAGE is dead.")
        cmd = input()
        return
    print(f" MAGE ( {mage} ) turn:")
    black_mage = find_player_by_role("Mage (black)")
    list_players()
    valid = 0
    while valid == 0:
        cmd = int(input("  Suspect? (id, 0 to pass) > "))
        if cmd == 0:
            print("  The MAGE decided not to act.")
            log_this(day, "MAGE", "The MAGE decided not to act.")
            cmd = input()
            return
        suspect = find_player_by_id(cmd)
        if not is_alive_by_name(suspect):
            print(f"  {suspect} is dead.")
            cmd = input()
        else:
            if is_alive_by_name(black_mage):
                print("  Inverted response:")
                if check_soul(suspect) == "Blue" or check_soul(suspect) == "Blue Black":
                    print(f"  {suspect} doesn't have a blue soul.")
                    log_this(day, "MAGE", f"{suspect} doesn't have a blue soul.")
                    cmd = input()
                    return
                else:
                    print(f"  {suspect} has a blue soul.")
                    log_this(day, "MAGE", f"{suspect} has a blue soul.")
                    cmd = input()
                    return
            else:
                if check_soul(suspect) == "Blue" or check_soul(suspect) == "Blue Black":
                    print(f"  {suspect} has a blue soul.")
                    log_this(day, "MAGE", f"{suspect} has a blue soul.")
                    cmd = input()
                    return
                else:
                    print(f"  {suspect} doesn't have a blue soul.")
                    log_this(day, "MAGE", f"{suspect} doesn't have a blue soul.")
                    cmd = input()
                    return
    
#Major
def major_turn(day, winner):
    major = find_player_by_role("Major")
    if not major:
        print(" The MAJOR is not in the game.")
        cmd = input()
        return winner
    if not is_alive_by_name(major):
        print(" The MAJOR is dead.")
        cmd = input()
        return winner
    if is_active_by_name(major):
        print(f" The MAJOR ( {major} ) has already used his power.")
        cmd = input()
        return winner
    print(f" MAJOR ( {major} ) turn:")
    list_players()
    valid = 0
    while not valid:
        if winner:
            cmd = int(input(f"  {winner} has been sentenced to dead, sentence someone else? (id, 0 to pass) > "))
        else:
            cmd = int(input(f"  Nobody is going to burn today, sentence someone? (id, 0 to pass) > "))
        if cmd == 0:
            print("  The MAJOR decided not to act.")
            log_this(day, "MAJOR", "The MAJOR decided not to act.")
            cmd = input()
            return winner
        if not is_alive_by_name(find_player_by_id(cmd)):
            print("  Seriously?")
        else:
            winner = find_player_by_id(cmd)
            print(f"  {winner} has been sentenced by the MAJOR.")
            log_this(day, "MAJOR", f"{winner} has been sentenced by the MAJOR.")
            active_player(day, major)
        cmd = input()
        return winner
        
#Medium
def medium_turn(day):
    medium = find_player_by_role("Medium")
    if not medium:
        print(" The MEDIUM is not in the game.")
        cmd = input()
        return
    if not is_alive_by_name(medium) or assassin_turn(day, "Medium"):
        print(" The MEDIUM is dead.")
        cmd = input()
        return
    print(f" MEDIUM ( {medium} ) turn:")
    list_players()
    valid = 0
    while valid == 0:
        cmd = int(input("  Suspect? (id, 0 to pass) > "))
        if cmd == 0:
            print("  The MEDIUM decided not to act.")
            log_this(day, "MEDIUM", "The MEDIUM decided not to act.")
            cmd = input()
            return
        suspect = find_player_by_id(cmd)
        if is_alive_by_name(suspect):
            print(f"  {suspect} is alive.")
            cmd = input()
        else:
            if check_soul(suspect) == "Black" or check_soul(suspect) == "Blue Black":
                print(f"  {suspect} had a black soul.")
                log_this(day, "MEDIUM", f"{suspect} had a black soul.")
                cmd = input()
                return
            else:
                print(f"  {suspect} didn't have a black soul.")
                log_this(day, "MAGE", f"{suspect} didn't have a black soul.")
                cmd = input()
                return

#Merchant
def merchant_turn(day, ballot = []):
    merchant = find_player_by_role("Merchant")
    if not merchant:
        return 0
    if not is_alive_by_name(merchant):
        return 0
    if merchant in ballot:
        return 0
    print(" The MERCHANT is in the game, beware...\n")
    return 1

#Priest (only night zero)
def priest_turn():
    priest = find_player_by_role("Priest")
    if not priest:
        print(" The PRIEST is not in the game.")
        cmd = input()
        return
    print(f" PRIEST ( {priest} ) turn:")
    harlot = find_player_by_role("Harlot")
    sinner = find_player_by_role("Sinner")
    if harlot:
        print("  The HARLOT is in the game.")
        log_this(0, "PRIEST", "The HARLOT is in the game.")
    if sinner:
        print("  The SINNER is in the game.")
        log_this(0, "PRIEST", "The SINNER is in the game.")
    else:
        print("  Neither the HARLOT nor the SINNER are in the game.")
        log_this(0, "PRIEST", "Neither the HARLOT nor the SINNER are in the game.")
    cmd = input()
    
#Orator
def orator_turn(day, winner):
    orator = find_player_by_role("Orator")
    if not orator:
        print(" The ORATOR is not in the game.")
        cmd = input()
        return winner
    if not is_alive_by_name(orator):
        print(" The ORATOR is dead.")
        cmd = input()
        return winner
    print(f" ORATOR ( {orator} ) turn:")
    cmd = input(f"  {winner} has been sentenced to dead, save him? (y/n) > ")
    if not cmd == "y":
        print("  The ORATOR decided not to act.")
        log_this(day, "ORATOR", "The ORATOR decided not to act.")
        cmd = input()
        return winner
    print(f"  {winner} has been saved by the ORATOR.")
    log_this(day, "ORATOR", f"{winner} has been saved by the ORATOR.")
    return None
    
#Psychic
def psychic_turn(day):
    psychic = find_player_by_role("Psychic")
    if not is_alive_by_name(psychic) or assassin_turn(day, "Psychic"):
        print(" The PSYCHIC is dead.")
        cmd = input()
        return 0
    print(f" PSYCHIC ( {psychic} ) turn:")
    list_players()
    valid = 0
    while valid == 0:
        cmd = int(input("  Suspect? (id, 0 to pass) > "))
        if cmd == 0:
            print("  The PSYCHIC decided not to act.")
            log_this(day, "PSYCHIC", "The PSYCHIC decided not to act.")
            cmd = input()
            return 0
        suspect = find_player_by_id(cmd)
        if not is_alive_by_name(suspect):
            print(f"  {suspect} is dead.")
            cmd = input()
        else:
            if check_soul(suspect) == "Black" or check_soul(suspect) == "Blue Black":
                print(f"  {suspect} has a black soul.")
                log_this(day, "PSYCHIC", f"{suspect} has a black soul.")
                cmd = input()
                return 1
            else:
                print(f"  {suspect} doesn't have a black soul.")
                log_this(day, "PSYCHIC", f"{suspect} doesn't have a black soul.")
                cmd = input()
                return 0

#Vampire

#night zero
def vampire_ghoul_turn():
    vampire = find_player_by_role("Vampire")
    if not vampire:
        print(" The VAMPIRE is not in the game.")
        cmd = input()
        return
    print(f" VAMPIRE ( {vampire} ) turn:")
    ghoul = find_player_by_role("Ghoul")
    if ghoul:
        print(f"  The VAMPIRE know his GHOUL ( {ghoul} ), they recognize each other.")
        log_this(0, "VAMPIRE", "The VAMPIRE and the GHOUL recognize each other.")
    else:
        print("  The GHOUL is not in the game.")
        log_this(0, "VAMPIRE", "The GHOUL is not in the game.")
    cmd = input()

#other nights:
def vampire_turn(day):
    vampire = find_player_by_role("Vampire")
    if not vampire:
        print(" The VAMPIRE is not in the game.")
        cmd = input()
        return
    if not is_alive_by_name(vampire):
        print(" The VAMPIRE is dead.")
        return
    print(f" VAMPIRE ( {vampire} ) turn:")
    list_players()
    cmd = int(input("  Vampirize someone? (id, 0 to pass) > "))
    if cmd == 0:
        print("  The VAMPIRE decided not to act.")
        log_this(day, "VAMPIRE", "The VAMPIRE decided not to act.")
        cmd = input()
        return
    vampirized = find_player_by_id(cmd)
    if not is_alive_by_name(vampirized):
        print(f"  {vampirized} is dead.")
        cmd = input()
        return
    else:
        if check_soul(vampirized) == "Blue" or check_soul(vampirized) == "Blue Black" or find_role_by_player(vampirized) == "Priest":
            print("  The attack has failed.\n")
            log_this(day, "VAMPIRE", "The attack has failed.")
            cmd = input()
            return
        if find_role_by_player(vampirized) == "Wolf 1" or find_role_by_player(vampirized) == "Wolf 2" or find_role_by_player(vampirized) == "Wolf 3" or find_role_by_player(vampirized) == "Wolf 4":
            print("  The attack has failed.\n")
            log_this(day, "VAMPIRE", "The attack has failed.")
            add_death_list(day, vampire, "by attacking a WOLF")
            cmd = input()
            return
        if find_role_by_player(vampirized) == "Vampire slayer":
            print("  The attack has failed.\n")
            log_this(day, "VAMPIRE", "The attack has failed.")
            add_death_list(day, vampire, "by attacking the VAMPIRE SLAYER")
            cmd = input()
            return
        execute_commit(
            "UPDATE players SET role = ?, soul = ?, faction = ? WHERE name = ?",
            ("Vampirized", "Black", "Vampires", vampirized)
        )
        print(f"  {vampirized} has been vampirized.")
        log_this(day, "VAMPIRE", f"{vampirized} has been vampirized.")
        cmd = input()

#Vampire slayer (only night zero)
def vampire_slayer_turn():
    vampire_slayer = find_player_by_role("Vampire slayer")
    if not vampire_slayer:
        print(" The VAMPIRE SLAYER is not in the game.")
        cmd = input()
        return
    print(f" VAMPIRE SLAYER ( {vampire_slayer} ) turn:")
    vampire = find_player_by_role("Vampire")
    if vampire:
        print("  The VAMPIRE is in the game.")
        log_this(0, "VAMPIRE SLAYER", "The VAMPIRE SLAYER is in the game.")
    else:
        print("  The VAMPIRE is not in the game.")
        log_this(0, "VAMPIRE SLAYER", "The VAMPIRE is not in the game.")
    cmd = input()
    
#Witch
def witch_turn(day):
    witch = find_player_by_role("Witch")
    if not witch:
        print(" The WITCH is not in the game.")
        cmd = input()
        return None
    if not is_alive_by_name(witch) or assassin_turn(day, "Witch"):
        print(" The WITCH is dead.")
        cmd = input()
        return None
    print(f" WITCH ( {witch} ) turn:")
    black_witch = find_player_by_role("Witch (black)")
    list_players()
    valid = 0
    while valid == 0:
        cmd = int(input("  Protect someone by the wolves? (id, 0 to pass) > "))
        if cmd == 0:
            print("  The WITCH decided not to act.")
            log_this(day, "WITCH", "The WITCH decided not to act.")
            cmd = input()
            return None
        protect = find_player_by_id(cmd)
        if not is_alive_by_name(protect):
            print(f"  {suspect} is dead.")
            cmd = input()
        else:
            if is_alive_by_name(black_witch):
                print("  The protection has failed.")
                log_this(day, "WITCH", "The protection has failed.")
                cmd = input()
                return None
            else:
                print(f"  {protect} is protected by the WITCH.")
                log_this(day, "WITCH", f"{protect} is protected by the WITCH.")
                cmd = input()
                return protect
    
#Wolves
#first met and wolf 4 met
def wolves_meeting_turn(day = 0):
    wolves = [find_player_by_role("Wolf 1"), find_player_by_role("Wolf 2")]
    if find_player_by_role("Wolf 3"):
        wolves.append(find_player_by_role("Wolf 3"))
    if find_player_by_role("Wolf 4"):
        wolves.append(find_player_by_role("Wolf 4"))
    print(" WOLVES (", ", ".join(wolves), ") turn:\n  All WOLVES recognize each others.")
    grade = 0
    for w in wolves:
        grade += 1
        print(f"   WOLF {grade}: {w}")
    log_this(day, "WOLVES", "All WOLVES recognize each others.")
    cmd = input()
    
#other nights:
def wolves_turn(day, protection):
    wolves = [find_player_by_role("Wolf 1"), find_player_by_role("Wolf 2")]
    alives = [is_alive_by_name(wolves[0]), is_alive_by_name(wolves[1])]
    if find_player_by_role("Wolf 3"):
        wolves.append(find_player_by_role("Wolf 3"))
        alives.append(find_player_by_role(wolves[2]))
    else:
        alives.append(0)
    if find_player_by_role("Wolf 4"):
        wolves.append(find_player_by_role("Wolf 4"))
        alives.append(find_player_by_role(wolves[3]))
    else:
        alives.append(0)
    if alives == [0, 0, 0, 0]:
        print(" All the WOLVES are dead.")
        return
    if alives[0]:
        print(f" WOLF 1 ( {wolves[0]} ) turn:")
        active = wolves[0]
    elif alives[1]:
        print(f" WOLF 2 ( {wolves[1]} ) turn:")
        active = wolves[1]
    elif alives[3]:
        print(f" WOLF 4 ( {wolves[3]} ) turn:")
        if alives[2]:
            active = wolves[2]
        else:
            active = wolves[3]
    else:
        print(" WOLF 3 can't kill by himself.")
        return
    print("  All the wolves (", ", ".join(wolves), " ) open their eyes:\n")
    list_players()
    cmd = int(input("  Attack someone? (id, 0 to pass) > "))
    if cmd == 0:
        print("  The WOLVES decided not to act.")
        log_this(day, "WOLVES", "The WOLVES decided not to act.")
        cmd = input()
        return
    victim = find_player_by_id(cmd)
    if not is_alive_by_name(victim):
        print(f"  {victim} is dead.")
        cmd = input()
        return
    else:
        if victim == protection or find_role_by_player(victim) == "Druid":
            print("  The attack has failed.")
            log_this(day, "WOLVES", "The attack has failed.")
            cmd = input()
            return
        if find_role_by_player(victim)== "Traitor" and not is_active_by_name(victim):
            active_player(day, victim)
            print(f"  {victim} turn out to be the TRAITOR. He open his eyes and recognize the WOLVES.")
            cmd = input()
            return
        if find_role_by_player(victim) == "Peasant (wolf)":
            execute_commit(
                "UPDATE players SET role = ?, soul = ?, faction = ? WHERE name = ?",
                ("Wolf 4", "Black", "Wolves", victim)
            )
            print(f"  {victim} turn out to be WOLF 4.")
            wolves_meeting_turn(day)
            return
        if find_role_by_player(victim) == "Peasant (hero)":
                add_death_list(day, active, "by attacking a PEASANT (HERO)")
        add_death_list(day, victim, "by the WOLVES")
        log_this(day, "WOLVES", f"{victim} has been devoured.")
        cmd = input()
