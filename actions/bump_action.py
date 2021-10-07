from __future__ import annotations

from actions.action_with_direction import ActionWithDirection
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities import Entity

class BumpAction(ActionWithDirection):
    def perform(self) -> None:

        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()