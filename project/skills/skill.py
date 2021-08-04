class Skill:

    def __init__(self, name: str, description: str, damage: int, level_requirement: int, job: str) -> None:
        self.name = name
        self.description = description
        self.damage = damage
        self.level_requirement = level_requirement
        self.job = job
