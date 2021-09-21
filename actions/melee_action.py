from __future__ import annotations

from actions.action_with_direction import ActionWithDirection

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities import Entity

class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        
        target = self.blocking_entity

        if not target:
            return  # No entity to attack.

        if self.entity.char == '@':
            print(f"The agent attacked the {target.name} with their cursed sword!")
        else:
            print('You were attacked!')