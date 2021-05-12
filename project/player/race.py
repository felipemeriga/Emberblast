from project.conf.conf import get_configuration

# TODO - Refactor to enable creating dynamic races, so the game configuration can be extended
class RaceMeta(type):
    def __init__(self, clsname, superclasses, attributedict):
        super_class = superclasses[0]
        race_attributes = get_configuration('races').get(clsname, {})
        super_class.__init__(self, race_attributes.get('health_points', 0),
                             race_attributes.get('magic_points', 0),
                             race_attributes.get('move_speed', 0),
                             race_attributes.get('strength', 0),
                             race_attributes.get('intelligence', 0),
                             race_attributes.get('accuracy', 0),
                             race_attributes.get('armour', 0),
                             race_attributes.get('magic_resist', 0),
                             race_attributes.get('will', 0)
                             )

class Race(metaclass=RaceMeta):
    def __init__(self, health_points,
                 magic_points,
                 move_speed,
                 strength,
                 intelligence,
                 accuracy,
                 armour,
                 magic_resist,
                 will):
        self.health_points = health_points
        self.magic_points = magic_points
        self.move_speed = move_speed
        self.strength = strength
        self.intelligence = intelligence
        self.accuracy = accuracy
        self.armour = armour
        self.magic_resist = magic_resist
        self.will = will


class Human(Race, metaclass=RaceMeta):

    def __init__(self):
        pass

class Dwarf(Race, metaclass=RaceMeta):

    def __init__(self):
        pass

class Elf(Race, metaclass=RaceMeta):

    def __init__(self):
        pass

class Orc(Race, metaclass=RaceMeta):

    def __init__(self):
        pass

class Halflings(Race, metaclass=RaceMeta):

    def __init__(self):
        pass