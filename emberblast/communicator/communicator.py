import sys
from typing import Callable, Type

from emberblast.interface.interface import ICommunicator
from .communicator_cmd import CommunicatorCMD


def communicator_injector() -> Callable:
    def decorator(cls) -> Type:
        attr_name = 'communicator'
        setattr(cls, attr_name, communicator)
        return cls

    return decorator


def communicator_factory() -> ICommunicator:
    if sys.stdin and sys.stdin.isatty():
        return CommunicatorCMD()


communicator: ICommunicator = communicator_factory()
