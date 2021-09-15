from __future__ import annotations

from actions.action_with_direction import ActionWithDirection
from vizualization.fov_functions import discover_tiles

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entities.entity import Entity

class MovementAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.map.is_blocked(dest_x, dest_y):
            return # Destination is not walkable

        # The following two should never be executed as they are handled in BumbAction class
        if not engine.map.in_bounds(dest_x, dest_y):
            return  # Destination is out of bounds.
        if engine.map.get_blocking_entity_at(dest_x, dest_y):
            return  # Destination is blocked by an entity.

        entity.move(self.dx, self.dy)
        discover_tiles(engine.map, engine.agent) # Discovers tiles ahead of the agent