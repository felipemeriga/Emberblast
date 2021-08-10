from project.test.test import BaseTestCase
from .test_player import mock_player
from project.skill import get_player_available_skills, get_instantiated_skill


@mock_player()
class TestModuleSkill(BaseTestCase):

    def test_get_player_available_skills(self) -> None:
        result = get_player_available_skills(self.mock_player)
        assert isinstance(result, dict)

    def test_get_instantiated_skill(self) -> None:
        skill = {
            "Fireball": {
                "name": "Fireaball",
                "description": "test",
                "damage": 2,
                "level_requirement": 1,
                "field": 0,
                "job": "Rogue"
            }
        }
        skill = get_instantiated_skill(skill)
        print(skill)
