class GameContext:
    """
    Holds all mutable game state:
    - players list
    - status (day, phase, turn)
    - can be upgraded in future (config, RNG, rule engine, etc.)
    """
    def __init__(self, status, players):
        self.status = status
        self.players = players