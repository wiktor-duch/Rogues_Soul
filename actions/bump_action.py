from __future__ import annotations

from actions.action_with_direction import ActionWithDirection
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entities.entity import Entity

class BumpAction(ActionWithDirection):
    def perform(self) -> None:

        if self.blocking_entity:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()