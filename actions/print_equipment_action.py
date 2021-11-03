from __future__ import annotations

from typing import TYPE_CHECKING
from actions.action import Action

if TYPE_CHECKING:
    from entities import Actor

class PrintEquipmentAction(Action):
    def __init__(
        self,
        entity: Actor,
    ):
        super().__init__(entity)

    def perform(self) -> None:
        '''
        Prints entity's equipment.
        '''

        print(f'\n{self.entity.name}\'s EQUIPMENT\n')
        
        if self.entity.actor_equipment.armour is not None:
            print(f'ARMOUR: {self.entity.actor_equipment.armour.name} '
                + f'(HP+{self.entity.actor_equipment.armour.equippable.health_bonus})\n')
        else:
            print('ARMOUR: None\n')

        if self.entity.actor_equipment.sword is not None:
            print(f'SWORD: {self.entity.actor_equipment.sword.name} ' 
                + f'(POW+{self.entity.actor_equipment.sword.equippable.power_bonus})\n')
        else:
            print('SWORD: None\n')

        if self.entity.actor_equipment.shield is not None:
            print(f'SHIELD: {self.entity.actor_equipment.shield.name} '
                + f'(DEF+{self.entity.actor_equipment.shield.equippable.defense_bonus})\n')
        else:
            print('SHIELD: None\n')
        
        input('Press [enter] to continue.\n')