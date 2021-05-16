

class Player:
    def __init__(self, name, gender, job, race):
        self.job = job
        self.race = race
        self.name = name
        self.gender = gender
        self.health_points = 10
        self.magic_points = 10
        self.move_speed = 2
        self.strength = 2
        self.intelligence = 2
        self.accuracy = 4
        self.armour = 2
        self.magic_resist = 2
        self.will = 2
        self.level = 1
        self.add_attributes(self.job)
        self.add_attributes(self.race)

    def add_attributes(self, attributes=None):
        self.health_points += attributes.health_points
        self.magic_points += attributes.magic_points
        self.move_speed += attributes.move_speed
        self.strength += attributes.strength
        self.intelligence += attributes.intelligence
        self.accuracy += attributes.accuracy
        self.armour += attributes.armour
        self.magic_resist += attributes.magic_resist
        self.will += attributes.will


class ControlledPlayer(Player):
    def __init__(self, name, gender, job, race):
        super().__init__(name, gender, job, race)


class BotPlayer(Player):
    def __init__(self, job, race, name=None):
        super().__init__(name, job, race)

def bot_factory(number_of_bots):
    bots = []

