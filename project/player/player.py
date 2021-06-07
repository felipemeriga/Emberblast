from random import randrange

from project.conf import get_configuration
from .job import dynamic_jobs_classes
from .race import dynamic_races_classes
from project.questions import ask_attributes_to_improve, improve_attributes_automatically
from project.utils import JOBS_SECTION, RACES_SECTION
from project.utils.name_generator import generate_name


class Player:
    def __init__(self, name, job, race):
        self.job = job
        self.race = race
        self.name = name
        self.health_points = 10
        self.magic_points = 10
        self.move_speed = 2
        self.strength = 2
        self.intelligence = 2
        self.accuracy = 4
        self.armour = 2
        self.magic_resist = 2
        self.will = 2
        self.level = 1
        self.experience = 0
        self.buffs = []
        self.debuffs = []
        self._alive = True
        self.position = 0
        self._hidden = False

        self.add_attributes(self.job)
        self.add_attributes(self.race)

    def add_attributes(self, attributes=None):
        self.health_points += attributes.health_points
        self.magic_points += attributes.magic_points
        self.move_speed += attributes.move_speed
        self.strength += attributes.strength
        self.intelligence += attributes.intelligence
        self.accuracy += attributes.accuracy
        self.armour += attributes.armour
        self.magic_resist += attributes.magic_resist
        self.will += attributes.will

    def _level_up(self):
        raise NotImplementedError('Player::to_string() should be implemented!')

    def earn_xp(self, experience):
        self.experience = self.experience + experience
        if self.experience >= 100:
            self.experience = self.experience - 100
            self._level_up()

    def suffer_damage(self, damage: float) -> None:
        self.health_points = self.health_points - damage
        if self.health_points <= 0:
            self.die()

    def die(self) -> None:
        self._alive = False

    def is_alive(self) -> bool:
        return self._alive

    def set_position(self, position: str) -> None:
        self.position = position

    def set_hidden(self, state: bool) -> None:
        self._hidden = state

    def is_hidden(self) -> bool:
        return self._hidden


class ControlledPlayer(Player):
    def __init__(self, name, job, race):
        super().__init__(name, job, race)

    def _level_up(self):
        improvements = ask_attributes_to_improve()
        for improvement in improvements:
            attribute = improvement.get('attribute', 'health_points')
            points = improvement.get('value', 0)
            self.__setattr__(attribute, points + self.__getattribute__(attribute))


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
