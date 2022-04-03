from typing import List, Union, Dict

from .player import Player
from emberblast.interface import IBag, IEquipment, IJob, IRace, IControlledPlayer


class ControlledPlayer(IControlledPlayer, Player):
    def __init__(self, name: str, job: IJob, race: IRace, bag: IBag, equipment: IEquipment) -> None:
        """
        Constructor of bot player.

        :param str name: Player's name.
        :param IJob job: The selected job.
        :param IRace race: The selected race.
        :param IBag bag: Player's bag.
        :param IEquipment equipment: Player's equipment.
        :rtype: None.
        """
        super().__init__(name, job, race, bag, equipment)

    def level_up(self, improvements: Union[List, Dict]) -> None:
        """
        Implementation this method from Player class, this function will ask the controlled player
        which attributes he wants to raise, on level up.

        :rtype: None.
        """
        for improvement in improvements:
            attribute = improvement.get('attribute', 'health_points')
            points = improvement.get('value', 0)
            self.__setattr__(attribute, points + self.__getattribute__(attribute))
        self.level = self.level + 1
