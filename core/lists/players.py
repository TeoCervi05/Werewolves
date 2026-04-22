"""
LIST OF AVAIBLE CHARACTERS
note on the 'active' parameter:
for single shot active characters, like the mayor:
    - 1 (default), action not yet performed;
    - 0, action performed;
for the traitor:
    - 0 (default), not discovered by the wolves;
    - 1, discovered by the wolves;
"""

ROLE_LIST = [
    [1, "ASSASSIN", "white", "village", 1],
    [2, "DRUID", "white", "village", 0],
    [3, "GHOUL", "white", "vampires", 0],
    [4, "GUARD", "white", "village", 0],
    [5, "GUARD (CORRUPTED)", "black", "village", 0],
    [6, "HARLOT", "black", "village", 0],
    [7, "HEALER", "blue", "village", 1],
    [8, "INNKEEPER", "white", "village", 0],
    [9, "JULIET", "white", "village", 0],
    [10, "LAWYER", "white", "village", 1], #NOT SURE, CHECK THE RULES
    [11, "MADMAN", "white", "village", 0],
    [12, "MAGE", "blue", "village", 0],
    [13, "MAGE (BLACK)", "blue black", "opponent", 0],
    [14, "MAJOR", "white", "village", 1],
    [15, "MEDIUM", "blue", "village", 0],
    [16, "MERCHANT", "white", "village", 0],
    [17, "ORATOR", "white", "village", 0], #NOT SURE, CHECK THE RULES
    [18, "PEASANT", "white", "village", 0],
    [19, "PEASANT (HERO)", "white", "village", 0],
    [20, "PEASANT (WOLF)", "white", "village", 0],
    [21, "PRIEST", "white", "village", 0],
    [22, "PSYCHIC", "blue", "village", 0],
    [23, "SINNER", "white", "village", 0],
    [24, "SPY", "white", "village", 0],
    [25, "TRAITOR", "white", "wolves", 0],
    [26, "VAMPIRE", "black", "vampires", 0],
    [27, "VAMPIRE SLAYER", "white", "village", 0],
    [28, "WITCH", "blue", "village", 0],
    [29, "WITCH (BLACK)", "blue black", "opponent", 0],
    [30, "WOLF 1", "black", "wolves", 0],
    [31, "WOLF 2", "black", "wolves", 0],
    [32, "WOLF 3", "black", "wolves", 0],
]

class Player:
    def __init__(self):
        self.name
        self.role
        self.soul
        self.faction
        self.active
        self.romeo
        self.alive