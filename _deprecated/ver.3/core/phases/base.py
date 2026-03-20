class PhaseBase:
    NAME = None

    def __init__(self, game, role_manager):
        self.game = game
        self.role_manager = role_manager
        
    # entering the phase
    def on_enter(self):
        pass

    # next command
    def next_phase(self):
        raise NotImplementedError

    # who can act during this phase
    def allowed_turns(self):
        return[]