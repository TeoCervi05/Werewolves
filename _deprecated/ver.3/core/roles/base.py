#Defining a base class for all the roles, with instructions for each phase.

class RoleBase:
    NAME = None # role name in players.role

    def __init__(self, game):
        self.game = game

    # -- phases instruction --

    def on_night_zero(self):
        pass

    def on_night(self):
        pass

    def on_day(self):
        pass

    def on_vote(self):
        pass
    
    def on_ballot(self):
        pass