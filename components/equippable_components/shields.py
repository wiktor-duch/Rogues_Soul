from components.equippable_components.equippable import Equippable
from components.equippable_components.equipment_types import EquipmentType

class SoldiersShield(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.SHIELD,
            defense_bonus=1
        )

class KiteShield(Equippable):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.SHIELD,
            defense_bonus=2
        )