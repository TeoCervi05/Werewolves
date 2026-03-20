from core.roles.priest import Priest

class RoleManager:
    def __init__(self, game):
        self.game = game
        self.roles = self.load_roles()

    #Instantiate roles
    def load_roles(self):
        role_classes = [
            Priest,
        ] #to be completed

        roles = {}

        for cls in role_classes:
            roles[cls.NAME] = cls(self.game)

        return roles

    # -- phases --

    def night_zero(self):
        for role in self.roles.values():
            role.on_night_zero()

    def night(self):
        for role in self.roles.values():
            role.on_night()

    def day(self):
        for role in self.roles.values():
            role.on_day()

    def vote(self):
        for role in self.roles.values():
            role.on_vote()

    def ballot(self):
        for role in self.roles.values():
            role.on_ballot()