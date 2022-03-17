from abc import ABC
from typing import Callable, Type

from .actions import ActionsQuestionerCMD
from .enemies import EnemiesQuestionerCMD
from .items import ItemsQuestionerCMD
from .move import MovementQuestionerCMD
from .level_up import LevelUpQuestionerCMD
from .new_game import NewGameQuestionerCMD
from .skills import SkillsQuestionerCMD
from .save import SaveLoadQuestionerCMD


class QuestioningSystem(ABC):

    def __init__(self, arg) -> None:
        # TODO - This part will be a factory, so a if clause for different implementations will need to be placed
        # since CMD is the only current questioner, we can keep it hardcoded
        self.actions_questioner = ActionsQuestionerCMD()
        self.enemies_questioner = EnemiesQuestionerCMD()
        self.items_questioner = ItemsQuestionerCMD()
        self.movement_questioner = MovementQuestionerCMD()
        self.level_up_questioner = LevelUpQuestionerCMD()
        self.new_game_questioner = NewGameQuestionerCMD()
        self.skills_questioner = SkillsQuestionerCMD()
        self.save_load_questioner = SaveLoadQuestionerCMD()

    def __call__(self):
        return self


@QuestioningSystem
def get_questioning_system() -> QuestioningSystem:
    pass


def questioning_system_injector() -> Callable:
    def decorator(cls) -> Type:
        attr_name = 'questioning_system'
        setattr(cls, attr_name, get_questioning_system())  # Default value for that attribute
        return cls

    return decorator
