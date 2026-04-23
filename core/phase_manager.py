from core.phases.setup import SetupPhase

class PhaseManager:
    def __init__(self, game):
        self.game = game
        self.phases = {
            "setup": SetupPhase
        }

        self.current = None
        self.help = ""

    def start(self, pname):
        get_class = self.phases[pname]
        self.current = get_class(self.game)
        self.current.on_enter()
        self.help = self.current.HELP