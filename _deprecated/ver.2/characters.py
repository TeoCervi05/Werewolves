from players import player_by_role
from log import log_this
from format import prints

#Priest (only night zero)
def priest():
    priest = player_by_role("PRIEST")
    if priest:
        prints(f"priest turn ({priest}):", "head")
        if player_by_role("SINNER", "PRIEST"):
            prints("There is a SINNER in the village", "body")
            log_this("priest", "The SINNER is in the game.")
        if player_by_role("HARLOT", "PRIEST"):
            prints("There is a HARLOT in the village", "body")
            log_this("priest", "The HARLOT is in the game.")