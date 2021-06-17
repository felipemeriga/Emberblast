class SideEffect:
    def __init__(self, type: str, attribute: str, base: int, duration: int, occurrence: str) -> None:
        self.type = type
        self.attribute = attribute
        self.base = base
        self.duration = duration
        self.occurrence = occurrence
