from random import randrange

from project.questions import improve_attributes_automatically
from .race import dynamic_races_classes
from .job import dynamic_jobs_classes
from .player import Player
from project.conf import get_configuration
from project.utils import JOBS_SECTION, RACES_SECTION
from project.utils.name_generator import generate_name


class BotPlayer(Player):
    def __init__(self, job, race, name=None):
        super().__init__(name, job, race)

    def _level_up(self):
        improvements = improve_attributes_automatically(self.job.get_name(), self.race.get_name())
        for key, value in improvements.items():
            self.__setattr__(key, value + self.__getattribute__(value))


def bot_factory(number_of_bots):
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