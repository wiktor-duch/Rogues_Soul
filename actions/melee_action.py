from __future__ import annotations

from actions.action_with_direction import ActionWithDirection

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entities.entity import Entity

class MeleeAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        target = engine.map.get_blocking_entity_at(dest_x, dest_y)
        if not target:
            return  # No entity to attack.

        print(f"You attacked the {target.name} with your sword!")