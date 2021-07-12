from random import randrange

from project.questions import improve_attributes_automatically
from .race import dynamic_races_classes, Race
from .job import dynamic_jobs_classes, Job
from .player import Player
from project.conf import get_configuration
from project.utils import JOBS_SECTION, RACES_SECTION
from project.utils.name_generator import generate_name


class BotPlayer(Player):
    def __init__(self, job: Job, race: Race, name: str =None) -> None:
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
        Implementation this method from Player class, this function will improve the attribute
        in an automated way, every time a bot player levels up, considering its race and job, to
        promote the proper combination of attributes.

        :rtype: None.
        """
        improvements = improve_attributes_automatically(self.job.get_name(), self.race.get_name())
        for key, value in improvements.items():
            self.__setattr__(key, value + self.__getattribute__(value))


def bot_factory(number_of_bots):
    """
    Function that will generated all the bots, depending of the number that was informed as the argument,
    each bot race and job, will be picked randomly.

    :rtype: None.
    """
    bots = []
    jobs = list(get_configuration(JOBS_SECTION).keys())
    races = list(get_configuration(RACES_SECTION).keys())
    for n in range(int(number_of_bots)):
        name = generate_name()
        chosen_job = jobs[randrange(len(jobs))]
        chosen_race = races[randrange(len(races))]
        job = dynamic_jobs_classes[chosen_job]()
        race = dynamic_races_classes[chosen_race]()
        bots.append(BotPlayer(job, race, name))

    return bots