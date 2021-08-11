from project.interface import ISideEffect


class SideEffect(ISideEffect):
    def __init__(self, name: str, effect_type: str, attribute: str, base: int, duration: int, occurrence: str) -> None:
        self.name = name
        self.effect_type = effect_type
        self.attribute = attribute
        self.base = base
        self.duration = duration
        self.occurrence = occurrence
