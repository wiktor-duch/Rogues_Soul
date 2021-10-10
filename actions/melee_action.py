from __future__ import annotations

from actions.action_with_direction import ActionWithDirection

from random import randint
from typing import TYPE_CHECKING
import exceptions

if TYPE_CHECKING:
    from entities import Entity

class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        
        target = self.target_actor

        if not target:
            raise exceptions.ImpossibleAction('No target to attack.')

        # Defense gives the target a chance of avoiding the attack
        if randint(0, target.fighter.defense) == 0:
            # Attack is successful
            target.fighter.hp -= self.entity.fighter.power
            if target.ai:
                self.engine.message_log.add_message(
                    f'{self.entity.name} attacks {target.name}!'
                )
            
        else:
            # Attack missed
            self.engine.message_log.add_message(
                f'{self.entity.name} missed the attack!'
            )