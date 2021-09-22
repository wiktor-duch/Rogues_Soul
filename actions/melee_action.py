from __future__ import annotations

from actions.action_with_direction import ActionWithDirection

from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities import Entity

class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        
        target = self.target_actor

        if not target:
            return  # No entity to attack.

        # Defense gives the target a chance of avoiding the attack
        if randint(0, target.fighter.defense) == 0:
            # Attack is successful
            target.fighter.hp -= self.entity.fighter.power
            if target.ai:
                print(f'{self.entity.name} attacks {target.name}!')
            
        else:
            # Attack missed
            print(f'{self.entity.name} missed the attack!')