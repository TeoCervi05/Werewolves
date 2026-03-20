# -- ROLE LISTS --

ROLE_LIST = [
    [1, "ASSASSIN", "white", "village"],
    [2, "DRUID", "white", "village"],
    [3, "GHOUL", "white", "vampires"],
    [4, "GUARD", "white", "village"],
    [5, "GUARD (CORRUPTED)", "black", "village"],
    [6, "HARLOT", "black", "village"],
    [7, "HEALER", "blue", "village"],
    [8, "INNKEEPER", "white", "village"],
    [9, "JULIET", "white", "village"],
    [10, "LAWYER", "white", "village"],
    [11, "MADMAN", "white", "village"],
    [12, "MAGE", "blue", "village"],
    [13, "MAGE (BLACK)", "blue black", "opponent"],
    [14, "MAJOR", "white", "village"],
    [15, "MEDIUM", "blue", "village"],
    [16, "MERCHANT", "white", "village"],
    [17, "ORATOR", "white", "village"],
    [18, "PEASANT", "white", "village"],
    [19, "PEASANT (HERO)", "white", "village"],
    [20, "PEASANT (WOLF)", "white", "village"],
    [21, "PRIEST", "white", "village"],
    [22, "PSYCHIC", "blue", "village"],
    [23, "SINNER", "white", "village"],
    [24, "SPY", "white", "village"],
    [25, "TRAITOR", "white", "wolves"],
    [26, "VAMPIRE", "black", "vampires"],
    [27, "VAMPIRE SLAYER", "white", "village"],
    [28, "WITCH", "blue", "village"],
    [29, "WITCH (BLACK)", "blue black", "opponent"],
    [30, "WOLF 1", "black", "wolves"],
    [31, "WOLF 2", "black", "wolves"],
    [32, "WOLF 3", "black", "wolves"],
]

def CHECK_ROLE_LIST():
    role_list = []

    for r in ROLE_LIST:
        role_list.append(r[1])

    return role_list

# -- HELPS --

setup_ACTIONS = "clear: erase the screen;_exit: close the program;_help: print queries list;_log: print the game log;_next: proceed to the next phase;_player: print or modify players list;_status: print or modify status infos;_leave blanck to print both status and players list."

# -- LISTS --

STATUS_TIME = [
    "setup",
    "day",
    "vote",
    "ballot", 
    "night"]

STATUS_TURN = [
    "master",
    "priest",
]

ACTIVES_NIGHT_ZERO = [
    "priest",
    "vampire slayer",
    "juliet",
    "guards",
    "vampire",
    "wolves",
    "psychic",
    "mage",
    "master"
]

ACTIVES_NIGHT = [
    "psychic",
    "mage",
    "medium",
    "witch",
    "vampire",
    "wolves",
    "healer",
    "master"
]

ACTIVES_VOTE = [
    "village",
    "lawyer",
    "master"
]

ACTIVES_BALLOT = [
    "village",
    "orator",
    "major"
]

# -- OBJECTS --

PLAYERS = None
STATUS = None