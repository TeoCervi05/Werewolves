from core.roles.base import RoleBase
from core.players import player_by_role
from utils.log import log_this
from utils.format import prints

class Priest(RoleBase):
    NAME = "PRIEST"

    def on_night_zero(self):
        priest_name = player_by_role(self.game, "PRIEST")
        if not priest_name:
            return
        
        prints(f"priest turn ({priest_name}):", "head")

        if player_by_role(self.game, "SINNER", "PRIEST"):
            prints("There is a SINNER in the village", "body")
            log_this("priest", "SINNER detected", self.game.status.day)

        if player_by_role(self.game, "HARLOT", "PRIEST"):
            prints("There is a HARLOT in the village", "body")
            log_this("priest", "HARLOT detected", self.game.status.day)