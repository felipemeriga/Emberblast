from random import randrange
from project.conf.conf import get_configuration
from project.player.job import dynamic_jobs_classes
from project.player.race import dynamic_races_classes
from project.utils.constants import JOBS_SECTION, RACES_SECTION
from project.utils.name_generator.fantasy_name_generator import generate_name


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

    def level_up(self):
        raise NotImplementedError('Player::to_string() should be implemented!')

    def earn_xp(self, experience):
        self.experience = self.experience + experience
        if self.experience >= 100:
            self.experience = self.experience - 100
            self.level_up()


class ControlledPlayer(Player):
    def __init__(self, name, job, race):
        super().__init__(name, job, race)

    def level_up(self):
        pass


class BotPlayer(Player):
    def __init__(self, job, race, name=None):
        super().__init__(name, job, race)

    def level_up(self):
        pass

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
