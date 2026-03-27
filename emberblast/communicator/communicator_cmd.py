from emberblast.interface import ICommunicator
from emberblast.renderer import RichCLIRenderer

from .questioner_cmd import QuestionerCMD


class CommunicatorCMD(ICommunicator):
    def __init__(self) -> None:
        self.informer = RichCLIRenderer()
        self.questioner = QuestionerCMD()
