from components.equippable_components.equippable import Equippable
from components.equippable_components.equipment_types import EquipmentType

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