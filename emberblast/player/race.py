from emberblast.conf import get_configuration

from emberblast.utils import RACES_SECTION
from emberblast.interface import IRace


class RaceMeta(type):
    def __init__(self, clsname, superclasses, attributedict):
        if clsname == 'Race':
            return
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


class Race(IRace, metaclass=RaceMeta):
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

    def get_name(self):
        return self.__class__.__name__


# dynamic constructor
def constructor(self):
    pass


# dynamic example method
def display_method(self, arg):
    print(arg)


# dynamic class method
@classmethod
def class_method(cls, arg):
    print(arg)


@classmethod
def get_name(self):
    return self.name


def create_dynamic_races():
    races_dynamic_classes = {}
    race_from_config = get_configuration(RACES_SECTION)
    for race in race_from_config:
        custom_race = type(race, (Race,), {
            # constructor
            "__init__": constructor,

            "name": race,
            # member functions
            "func_arg": display_method,
            "class_func": class_method,
            "get_name": get_name
        })
        races_dynamic_classes[race] = custom_race

    return races_dynamic_classes


dynamic_races_classes = create_dynamic_races()
