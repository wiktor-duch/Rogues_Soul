from game.components.equippable_components.equippable import Equippable
from game.components.equippable_components.equipment_types import EquipmentType

class ShortSword(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.SWORD,
            power_bonus=1
        )

class LongSword(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.SWORD,
            power_bonus=2
        )