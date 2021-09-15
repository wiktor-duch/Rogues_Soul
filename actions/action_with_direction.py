from __future__ import annotations

from actions.action import Action

from typing import Optional, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from entities.entity import Entity

class ActionWithDirection(Action):
    def __init__(self, entity: Entity, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        '''
        Returns this actions destination.
        '''
        
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        '''
        Return the blocking entity at this actions destination.
        '''
        
        return self.engine.map.get_blocking_entity_at(*self.dest_xy)

    def perform(self) -> None:
        '''
        This method must be overridden by ActionWithDirection subclasses.
        '''
        
        raise NotImplementedError()