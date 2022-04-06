import random
from typing import Dict, Callable

from emberblast.player import dynamic_races_classes, dynamic_jobs_classes, ControlledPlayer
from .test import BaseTestCase
from .test_item import mock_healing_item
from emberblast.item import Bag, Equipment
from emberblast.effect import SideEffect


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
        player = ControlledPlayer(name='test player', job=mock_player.job, race=mock_player.race, bag=Bag(),
                                  equipment=Equipment())
        setattr(func, 'mock_player', player)
        return func

    return wrapper


@mock_healing_item()
@mock_player()
class TestModulePlayer(BaseTestCase):
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
        self.mock_player.heal('health_points', 10000)

    def test_player_heal(self) -> None:
        self.mock_player.suffer_damage(1)
        self.mock_player.spend_mana(1)
        self.mock_player.heal('health_points', 1)
        self.mock_player.heal('magic_points', 1)

        self.assertEqual(self.mock_player.life, self.mock_player.health_points)
        self.assertEqual(self.mock_player.mana, self.mock_player.magic_points)

    def test_use_healing_item(self) -> None:
        if self.mock_healing_item.attribute == 'health_points':
            self.mock_player.suffer_damage(2)
        elif self.mock_healing_item.attribute == 'magic_points':
            self.mock_player.spend_mana(2)
        self.mock_player.use_item(self.mock_healing_item)
        self.assertEqual(self.mock_player.life, self.mock_player.health_points)
        self.assertEqual(self.mock_player.mana, self.mock_player.magic_points)

    def test_add_equal_side_effect(self) -> None:
        side_effect_1 = SideEffect('poison', 'debuff', 'health_points', 2, 4, 'iterated')
        side_effect_2 = SideEffect('poison', 'debuff', 'health_points', 2, 4, 'iterated')
        self.mock_player.add_side_effect(side_effect_1)
        self.mock_player.add_side_effect(side_effect_2)
        self.assertEqual(len(self.mock_player.side_effects), 1)
