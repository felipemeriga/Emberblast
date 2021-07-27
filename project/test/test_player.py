import random
from typing import Dict, Callable

from project.player import dynamic_races_classes, dynamic_jobs_classes, Player
from .test import BaseTestCase


def mock_job() -> Callable:
    def wrapper(func):
        jobs = dynamic_jobs_classes
        job = random.choice(list(jobs.values()))
        setattr(func, 'job', job)
        return func

    return wrapper


def mock_race() -> Callable:
    def wrapper(func):
        races = dynamic_races_classes
        race = random.choice(list(races.values()))
        setattr(func, 'race', race)
        return func

    return wrapper


@mock_race()
@mock_job()
def mock_player() -> Callable:
    def wrapper(func):
        player = Player(name='test player', job=mock_player.job, race=mock_player.race)
        setattr(func, 'mock_player', player)
        return func

    return wrapper


@mock_player()
class TestModulePlayer(BaseTestCase):
    def test_module(self) -> None:
        self.test_create_dynamic_races()
        self.test_create_dynamic_jobs()

    def check_race_job_attributes(self, instances_dict: Dict) -> None:
        for instance in instances_dict.values():
            self.assertHasAttr(instance, 'health_points')
            self.assertHasAttr(instance, 'magic_points')
            self.assertHasAttr(instance, 'move_speed')
            self.assertHasAttr(instance, 'strength')
            self.assertHasAttr(instance, 'intelligence')
            self.assertHasAttr(instance, 'accuracy')
            self.assertHasAttr(instance, 'armour')
            self.assertHasAttr(instance, 'magic_resist')
            self.assertHasAttr(instance, 'will')

    def test_create_dynamic_races(self) -> None:
        races = dynamic_races_classes
        self.check_race_job_attributes(races)

    def test_create_dynamic_jobs(self) -> None:
        jobs = dynamic_jobs_classes
        self.check_race_job_attributes(jobs)

    def test_player_suffer_damage(self) -> None:
        self.mock_player.suffer_damage(10000)
        self.assertFalse(self.mock_player.is_alive())
