from emberblast.interface import ICommunicator
from .informer_cmd import InformerCMD
from .questioner_cmd import QuestionerCMD


class CommunicatorCMD(ICommunicator):
    def __init__(self) -> None:
        self.informer = InformerCMD()
        self.questioner = QuestionerCMD()
