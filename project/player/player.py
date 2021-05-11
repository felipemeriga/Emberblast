class Player:
    def __init__(self, name):
        self.name = name
        self.health_points = 10
        self.magic_points = 10
        self.move_speed = 2
        self.strength = 2
        self.intelligence = 2
        self.accuracy = 4
        self.armour = 2
        self.magic_resist = 2
        self.level = 1
        self.will = 2

class ControlledPlayer(Player):
    def __init__(self, name):
        self.name = name


class BotPlayer(Player):
    def __init__(self, name):
        self.name = name
