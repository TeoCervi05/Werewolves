from core.phases.base import PhaseBase
from utils.format import prints

class NightZeroPhase(PhaseBase):
    NAME = "night_zero"

    def on_enter(self):
        self.game.status.phase = "night"
        self.game.status.turn = "priest"
        self.game.status.push()
        prints("night 0 has begun, eyes closed!", "stitle")
        self.role_manager.night_zero()

    def next_phase(self):
        self.game.status.day += 1
        return "day"