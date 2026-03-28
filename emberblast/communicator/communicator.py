import sys
from typing import Callable, Type

from emberblast.interface.interface import ICommunicator

from .communicator_cmd import CommunicatorCMD


def communicator_injector() -> Callable:
    def decorator(cls) -> Type:
        attr_name = "communicator"
        setattr(cls, attr_name, communicator)
        return cls

    return decorator


def communicator_factory() -> ICommunicator:
    if sys.stdin and sys.stdin.isatty():
        return CommunicatorCMD()


communicator: ICommunicator = communicator_factory()


def create_textual_communicator(app):
    """Create a communicator wired to the Textual app."""
    from emberblast.tui.questioner import TextualQuestioner
    from emberblast.tui.renderer import TextualRenderer

    class TextualCommunicator:
        def __init__(self, app):
            self.informer = TextualRenderer(app)
            self.questioner = TextualQuestioner(app)
            app.set_questioner(self.questioner)

    return TextualCommunicator(app)
