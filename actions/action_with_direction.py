from __future__ import annotations

from actions.action import Action

from typing import Optional, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from entities import Actor, Entity

class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
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
        Returns the blocking entity at this actions destination.
        '''
        
        return self.engine.map.get_blocking_entity_at(*self.dest_xy)
    
    @property
    def target_actor(self):
        '''
        Returns the actor at this action's destination.
        '''

        return self.engine.map.get_actor_at(*self.dest_xy)

    @property
    def target_item(self):
        '''
        Returns the item at this action's destination.
        '''

        if (self.engine.map.get_item_at(*self.dest_xy) is None 
            or  self.engine.map.get_item_at(*self.dest_xy).active is False):
            return None
        else:
            return self.engine.map.get_item_at(*self.dest_xy)

    def perform(self) -> None:
        '''
        This method must be overridden by ActionWithDirection subclasses.
        '''
        
        raise NotImplementedError()