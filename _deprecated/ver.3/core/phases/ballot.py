from core.phases.base import PhaseBase
from utils.format import prints

class BallotPhase(PhaseBase):
    NAME = "ballot"

    def on_enter(self):
        self.game.status.phase = "ballot"
        self.game.status.turn = "village"
        self.game.status.push()
        prints(f"Day {self.game.status.day} ballot: eye closed!", "stitle") #Add voices from the inn - add dead bodies on the road

    def next_phase(self):
        return "night"