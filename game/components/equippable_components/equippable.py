'''
Based on:
http://rogueliketutorials.com/tutorials/tcod/v2/
'''
from __future__ import annotations

from typing import TYPE_CHECKING

from game.components.base_component import BaseComponent

if TYPE_CHECKING:
    from game.entities import Equipment
    from game.components.equippable_components.equipment_types import EquipmentType

class Equippable(BaseComponent):
    parent: Equipment

    def __init__(
        self,
        equipment_type: EquipmentType,
        power_bonus: int = 0,
        defense_bonus: int = 0,
        health_bonus: int = 0
    ) -> None:

        self.equipment_type = equipment_type

        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.health_bonus = health_bonus