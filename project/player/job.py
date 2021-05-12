from project.conf.conf import get_configuration


# TODO - Refactor to enable creating dynamic jobs, so the game configuration can be extended

class JobMeta(type):
    def __init__(self, clsname, superclasses, attributedict):
        super_class = superclasses[0]
        class_attributes = get_configuration('jobs').get(clsname, {})
        super_class.__init__(self, class_attributes.get('health_points', 0),
                             class_attributes.get('magic_points', 0),
                             class_attributes.get('move_speed', 0),
                             class_attributes.get('strength', 0),
                             class_attributes.get('intelligence', 0),
                             class_attributes.get('accuracy', 0),
                             class_attributes.get('armour', 0),
                             class_attributes.get('magic_resist', 0),
                             class_attributes.get('will', 0)
                             )


class Job:
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


class Knight(Job, metaclass=JobMeta):

    def __init__(self):
        pass


class Wizard(Job, metaclass=JobMeta):

    def __init__(self):
        pass


class Rogue(Job, metaclass=JobMeta):

    def __init__(self):
        pass


class Archer(Job, metaclass=JobMeta):

    def __init__(self):
        pass


class Priest(Job, metaclass=JobMeta):

    def __init__(self):
        pass
