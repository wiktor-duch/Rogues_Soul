'''
Inspired by:
http://rogueliketutorials.com/tutorials/tcod/v2/
'''
from game.components.equippable_components.equippable import Equippable
from game.components.equippable_components.equipment_types import EquipmentType

class LightChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.ARMOUR,
            health_bonus=2
        )

class CursedRoguesArmour(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.ARMOUR,
            health_bonus=4
        )

class DragonArmour(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.ARMOUR,
            health_bonus=7
        )