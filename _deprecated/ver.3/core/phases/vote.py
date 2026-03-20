from core.phases.base import PhaseBase
from utils.format import prints

class VotePhase(PhaseBase):
    NAME = "vote"

    def on_enter(self):
        self.game.status.phase = "vote"
        self.game.status.turn = "village"
        self.game.status.push()
        prints(f"Day {self.game.status.day} votes: eye closed!", "stitle") #Add voices from the inn - add dead bodies on the road

    def next_phase(self):
        return "ballot"