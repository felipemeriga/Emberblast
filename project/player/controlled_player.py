from .job import Job
from .player import Player
from project.questions import ask_attributes_to_improve
from .race import Race


class ControlledPlayer(Player):
    def __init__(self, job: Job, race: Race, name: str = None) -> None:
        """
        Constructor of bot player.

        :param Job job: The selected job.
        :param Race race: The selected race.
        :param str name: Player's name.
        :rtype: None.
        """
        super().__init__(name, job, race)

    def _level_up(self) -> None:
        """
        Implementation this method from Player class, this function will ask the controlled player
        which attributes he wants to raise, on level up.

        :rtype: None.
        """
        improvements = ask_attributes_to_improve()
        for improvement in improvements:
            attribute = improvement.get('attribute', 'health_points')
            points = improvement.get('value', 0)
            self.__setattr__(attribute, points + self.__getattribute__(attribute))
