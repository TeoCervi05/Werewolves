from core.phases.setup import SetupPhase
from core.phases.day import DayPhase
from core.phases.night import NightPhase
from core.phases.night_zero import NightZeroPhase
from core.phases.vote import VotePhase
from core.phases.ballot import BallotPhase

class PhaseManager:
    def __init__(self, game, role_manager):
        self.game = game
        self.role_manager = role_manager

        self.phases = {
            "setup": SetupPhase,
            "night_zero": NightZeroPhase,
            "night": NightPhase,
            "day": DayPhase,
            "vote": VotePhase,
            "ballot": BallotPhase,
        }

        self.current = None

    def enter(self, phase_name):
        phase_class = self.phases[phase_name]
        self.current = phase_class(self.game, self.role_manager)
        self.current.on_enter()

    def start(self):
        self.enter(self.game.status.phase)

    def next(self):
        next_phase = self.current.next_phase()
        self.enter(next_phase)