class SingletonAction(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonAction, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Action(metaclass=SingletonAction):
    def __init__(self):
        pass

    def act(self):
        pass

    def compute_analytics(self):
        pass


class Move(Action):
    def __init__(self):
        pass


class Defend(Action):
    def __init__(self):
        pass


class Hide(Action):
    def __init__(self):
        pass


class Search(Action):
    def __init__(self):
        pass


class Attack(Action):
    def __init__(self):
        pass


class Skill(Action):
    def __init__(self):
        pass


class Item(Action):
    def __init__(self):
        pass
