from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from game.components.base_component import BaseComponent
from game.components.equippable_components.equipment_types import EquipmentType

if TYPE_CHECKING:
    from game.entities import Equipment

class ActorsEquipment(BaseComponent):
    def __init__(
        self,
        sword: Optional[Equipment] = None,
        shield: Optional[Equipment] = None,
        armour: Optional[Equipment] = None
    ) -> None:
        self.sword = sword
        self.shield = shield
        self.armour = armour
    
    @property
    def power_bonus(self) -> int:
        bonus = 0

        if self.sword is not None and self.sword.equippable is not None:
            bonus = self.sword.equippable.power_bonus
        
        return bonus

    @property
    def defense_bonus(self) -> int:
        bonus = 0

        if self.shield is not None and self.shield.equippable is not None:
            bonus = self.shield.equippable.defense_bonus
        
        return bonus
    
    @property
    def health_bonus(self) -> int:
        bonus = 0

        if self.armour is not None and self.armour.equippable is not None:
            bonus = self.armour.equippable.health_bonus
        
        return bonus
    
    def is_equipped(self, item: Equipment) -> bool:
        if (
            self.sword == item or
            self.shield == item or
            self.armour == item
        ):
            return True
    
    def is_better(self, item1: Equipment, item2: Equipment) -> bool:
        '''
        Checks if item1 is better than item2.
        '''
        if (
            item1.equippable.power_bonus > item2.equippable.power_bonus or
            item1.equippable.defense_bonus > item2.equippable.defense_bonus or
            item1.equippable.health_bonus > item2.equippable.health_bonus
        ):
            return True
        
        return False
    
    def equip_message(self, item_name: str) -> None:
        self.parent.map.engine.message_log.add_message(
            f'You found and equipped {item_name}'
        )

    def equip_to_slot(
        self, 
        equippable_item: Equipment,
        add_message: bool = False
    ) -> None:
        # Check which slot to equip
        if equippable_item.equippable.equipment_type == EquipmentType.SWORD:
            
            if self.sword is not None:
                if self.is_better(equippable_item, self.sword):
                    self.sword = equippable_item
                    if add_message:
                        self.equip_message(equippable_item.name)
            else:
                self.sword = equippable_item
                if add_message:
                    self.equip_message(equippable_item.name)
            
        elif equippable_item.equippable.equipment_type == EquipmentType.SHIELD:
            
            if self.shield is not None:
                if self.is_better(equippable_item, self.shield):
                    self.shield = equippable_item
                    if add_message:
                        self.equip_message(equippable_item.name)
            else:
                self.shield = equippable_item
                if add_message:
                    self.equip_message(equippable_item.name)
        elif (
            equippable_item.equippable.equipment_type == EquipmentType.ARMOUR
        ):
            if self.armour is not None:
                if self.is_better(equippable_item, self.armour):
                    self.armour = equippable_item
                    if add_message:
                        self.equip_message(equippable_item.name)
            else:
                self.armour = equippable_item
                if add_message:
                    self.equip_message(equippable_item.name)