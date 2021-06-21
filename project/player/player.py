class Player:
    def __init__(self, name, job, race):
        self.job = job
        self.race = race
        self.name = name
        self.health_points = 10
        self.magic_points = 10
        self.move_speed = 0
        self.strength = 2
        self.intelligence = 2
        self.accuracy = 2
        self.armour = 2
        self.magic_resist = 2
        self.will = 2
        self.level = 1
        self.experience = 0
        self.side_effects = []
        self._alive = True
        self.position = 0
        self._hidden = False

        self.add_attributes(self.job)
        self.add_attributes(self.race)

    def add_attributes(self, attributes=None):
        self.health_points += attributes.health_points
        self.magic_points += attributes.magic_points
        self.move_speed += attributes.move_speed
        self.strength += attributes.strength
        self.intelligence += attributes.intelligence
        self.accuracy += attributes.accuracy
        self.armour += attributes.armour
        self.magic_resist += attributes.magic_resist
        self.will += attributes.will

    def _level_up(self):
        raise NotImplementedError('Player::to_string() should be implemented!')

    def earn_xp(self, experience):
        self.experience = self.experience + experience
        if self.experience >= 100:
            self.experience = self.experience - 100
            self._level_up()

    def suffer_damage(self, damage: float) -> None:
        self.health_points = self.health_points - damage
        if self.health_points <= 0:
            self.die()

    def die(self) -> None:
        self._alive = False

    def is_alive(self) -> bool:
        return self._alive

    def set_position(self, position: str) -> None:
        self.position = position

    def set_hidden(self, state: bool) -> None:
        self._hidden = state

    def is_hidden(self) -> bool:
        return self._hidden

    '''
    This method it's used for getting the real value of an attribute
    computing and considering buffs/debuffs from side-effects, as well as
    items equipped to him.
    
    '''
    def get_attribute_real_value(self):
        pass