from core.phases.base import PhaseBase

class SetupPhase(PhaseBase):
    NAME = "setup"

    HELP = "status - show or modify current status;"

    def on_enter(self):
        self.game.status.phase = self.NAME
        self.game.status.turn = "master"
        self.game.status.push()

    """
    def next_phase(self):
        if self.game.status.day == 0:
            return "night_zero"
        return "day"
    """