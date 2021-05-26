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
    def __init__(self, independent: bool, repeatable: bool) -> None:
        """
        Constructor of the Base Class for Actions.

        :param bool independent: If it's True, the execution of this action will not block others in the same turn.
        :param bool repeatable: If it's True, can be performed many times in a single turn.
        :rtype: None
        """
        self.independent = independent
        self.repeatable = repeatable

    def act(self) -> None:
        pass

    def compute_analytics(self) -> None:
        pass


class Move(Action):
    def __init__(self, independent: bool, repeatable: bool) -> None:
        super(Move, self).__init__(independent, repeatable)


class Defend(Action):
    def __init__(self, independent: bool, repeatable: bool) -> None:
        super(Defend, self).__init__(independent, repeatable)


class Hide(Action):
    def __init__(self, independent: bool, repeatable: bool) -> None:
        super(Hide, self).__init__(independent, repeatable)


class Search(Action):
    def __init__(self, independent: bool, repeatable: bool) -> None:
        super(Search, self).__init__(independent, repeatable)


class Attack(Action):
    def __init__(self, independent: bool, repeatable: bool) -> None:
        super(Attack, self).__init__(independent, repeatable)


class Skill(Action):
    def __init__(self, independent: bool, repeatable: bool) -> None:
        super(Skill, self).__init__(independent, repeatable)


class Item(Action):
    def __init__(self, independent: bool, repeatable: bool) -> None:
        super(Item, self).__init__(independent, repeatable)


class Check(Action):
    def __init__(self, independent: bool, repeatable: bool) -> None:
        super(Check, self).__init__(independent, repeatable)


class Pass(Action):
    def __init__(self, independent: bool, repeatable: bool) -> None:
        super(Pass, self).__init__(independent, repeatable)
