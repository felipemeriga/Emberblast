class Player:
    def __init__(self, name):
        self.name = name


class ControlledPlayer(Player):
    def __init__(self, name):
        self.name = name


class BotPlayer(Player):
    def __init__(self, name):
        self.name = name
