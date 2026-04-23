class PhaseBase:
    NAME = None

    HELP = None

    def __init__(self, game):
        self.game = game
        
    #call on script starting
    def on_start(self):
        pass

    #callable actions
    def prompt(self):
        pass

    """
    # next command
    def next_phase(self):
        raise NotImplementedError

    # who can act during this phase
    def allowed_turns(self):
        return[]
    """