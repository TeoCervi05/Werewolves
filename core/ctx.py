from core.lists.status import Status

class Context:
    """
    Pull data from the database and store here for the game.
    Called also in for list operations (like reading or writing).
    """
    def __init__(self):
        self.status = Status()
