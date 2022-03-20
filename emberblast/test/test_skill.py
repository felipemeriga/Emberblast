from emberblast.test.test import BaseTestCase
from .test_player import mock_player
from emberblast.skill import get_player_available_skills, get_instantiated_skill, Steal
from ..interface import ISkill


@mock_player()
class TestModuleSkill(BaseTestCase):

    def test_get_player_available_skills(self) -> None:
        result = get_player_available_skills(self.mock_player)
        if len(result) > 0:
            assert isinstance(result[0], ISkill)

    def test_get_instantiated_skill(self) -> None:
        skill = {
            "Steal": {
                "name": "Steal",
                "description": "test",
                "base": 2,
                "cost": 1,
                "kind": "inflict",
                "level_requirement": 1,
                "ranged": 0,
                "area": 0,
                "job": "Rogue",
                "side_effects": [],
                "punishment_side_effects": [],
                "base_attribute": "strength"
            }
        }
        skill = get_instantiated_skill(skill)
        assert isinstance(skill, ISkill)
        assert isinstance(skill, Steal)
