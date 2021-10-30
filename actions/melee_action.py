from __future__ import annotations

from actions.action_with_direction import ActionWithDirection

from random import randint
from typing import TYPE_CHECKING
from exceptions import ImpossibleAction

if TYPE_CHECKING:
    from entities import Entity

class MeleeAction(ActionWithDirection):
    def perform_with_randomness(self) -> None:
        '''
        It differs from perform by adding randomness.
        '''
        target = self.target_actor

        if not target:
            raise ImpossibleAction('No target to attack.')

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
    
    def perform(self) -> None:
        '''
        It differs from perform by adding randomness.
        '''
        target = self.target_actor

        if not target:
            raise ImpossibleAction('No target to attack.')

        damage = self.entity.fighter.power - target.fighter.defense
        
        if damage > 0:
            # Attack successful
            target.fighter.take_damage(damage)
            if target.ai:
                self.engine.message_log.add_message(
                    f'{self.entity.name} attacks {target.name} for {damage} HP!'
                )
            
        else:
            # Attack missed
            self.engine.message_log.add_message(
                f'{self.entity.name} missed the attack!'
            )