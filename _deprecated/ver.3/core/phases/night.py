from core.phases.base import PhaseBase
from utils.format import prints

class NightPhase(PhaseBase):
    NAME = "night"

    def on_enter(self):
        self.game.status.phase = "night"
        self.game.status.turn = "psychic"
        self.game.status.push()
        prints(f"night {self.game.status.day} has begun, eyes closed!", "stitle")
        self.role_manager.night()

    def next_phase(self):
        self.game.status.day += 1
        return "day"