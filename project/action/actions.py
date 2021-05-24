"""
The plan here would be, as actions controls the game,
there will be a Singleton class called actions coordinator, that will
manage all the plays for all the players.

As the actions can be the same for each of the players, they will be considered Singletons
too.

Another thing to remember when creating the actions, is to use function generators and yield
for coordinating the move + another action per turn for each player.

Also, before this, we need to think about how it would be the difference between single player and
multiplayer, considering that it's ideal to use the same game class structure, to avoid copying similar
functionalities
"""


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
