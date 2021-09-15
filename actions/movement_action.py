from __future__ import annotations

from actions.action_with_direction import ActionWithDirection

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entities import Entity

class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if self.engine.map.is_blocked(dest_x, dest_y):
            return # Destination is not walkable

        # The following two should never be executed as they are handled in BumbAction class
        if not self.engine.map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if self.engine.map.get_blocking_entity_at(dest_x, dest_y):
            return  # Destination is blocked by an entity.

        self.entity.move(self.dx, self.dy)