from __future__ import annotations

from game.actions import MeleeAction, MovementAction
from game.components.base_ai import BaseAI

from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from game.entities import Actor, Entity

class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
    
    def is_visible(self, target: Entity) -> bool:
        '''
        Checks if the target is in the room (is visible to the enemy).
        '''

        for room in self.entity.map.rooms:
            if (room.intersects_tile_at(target.x, target.y) and
                room.intersects_tile_at(self.entity.x, self.entity.y)):
                # NOTE: Standing at the entrance does not trigger the enemy as ai takes turn after agent
                return True
        return False

    def perform(self) -> None:
        # Sets the agent as a target
        target = self.engine.agent

        if self.is_visible(target):
            # Gets x and y distances to the target
            dx = target.x - self.entity.x
            dy = target.y - self.entity.y

            if (abs(dx) == 0 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 0):
                # Target is next to the entity
                return MeleeAction(self.entity, dx, dy).perform()

            dx, dy = self.get_next_move(target.x, target.y)
            return MovementAction(self.entity, dx, dy).perform()
        
        # Otherwise, entity does nothing