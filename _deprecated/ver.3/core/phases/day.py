from core.phases.base import PhaseBase
from utils.format import prints

class DayPhase(PhaseBase):
    NAME = "day"

    def on_enter(self):
        self.game.status.phase = "day"
        self.game.status.turn = "village"
        self.game.status.push()
        prints(f"day {self.game.status.day} has begun!", "stitle") #Add voices from the inn - add dead bodies on the road

    def next_phase(self):
        return "vote"