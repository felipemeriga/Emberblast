from .player import Player
from project.questions import ask_attributes_to_improve


class ControlledPlayer(Player):
    def __init__(self, name, job, race):
        super().__init__(name, job, race)

    def _level_up(self):
        improvements = ask_attributes_to_improve()
        for improvement in improvements:
            attribute = improvement.get('attribute', 'health_points')
            points = improvement.get('value', 0)
            self.__setattr__(attribute, points + self.__getattribute__(attribute))