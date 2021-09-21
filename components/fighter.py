from components.base_component import BaseComponent

class Fighter(BaseComponent):
    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp # Entity’s hit points
        self._hp = hp
        self.defense = defense # Damage taken reduction/ chance of not being hit
        self.power = power # Entity's raw attack power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        # Makes sure hp is not below 0 and above max_hp
        self._hp = max(0, min(value, self.max_hp))