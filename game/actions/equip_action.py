from __future__ import annotations

from typing import TYPE_CHECKING
from game.actions.action import Action

if TYPE_CHECKING:
    from entities import Actor, Equipment

class EquipAction(Action):
    def __init__(
        self,
        entity: Actor,
        equipment: Equipment,
    ):
        super().__init__(entity)
        self.equipment = equipment

    def perform(self) -> None:
        '''
        Equip the piece of equipment in front of the entity.
        '''

        # Change position
        self.entity.x = self.equipment.x
        self.entity.y = self.equipment.y

        # Equip
        self.entity.actor_equipment.equip_to_slot(
            equippable_item=self.equipment,
            add_message=True
        )
        
        # Remove the equipment
        self.engine.map.entities.remove(self.equipment)