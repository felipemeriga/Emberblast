from project.questions import improve_attributes_automatically
from .player import Player
from project.interface import IBag, IJob, IRace, IEquipment, IBotPlayer


class BotPlayer(IBotPlayer, Player):
    def __init__(self, name: str, job: IJob, race: IRace, bag: IBag, equipment: IEquipment) -> None:
        """
        Constructor of bot player.

        :param Job job: The selected job.
        :param Race race: The selected race.
        :param str name: Player's name.
        :rtype: None.
        """
        super().__init__(name, job, race, bag, equipment)

    def _level_up(self) -> None:
        """
        Implementation this method from Player class, this function will improve the attribute
        in an automated way, every time a bot player levels up, considering its race and job, to
        promote the proper combination of attributes.

        :rtype: None.
        """
        improvements = improve_attributes_automatically(self.job.get_name(), self.race.get_name())
        for key, value in improvements.items():
            self.__setattr__(key, value + self.__getattribute__(value))
