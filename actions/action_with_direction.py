from __future__ import annotations

from actions.action import Action

from typing import Optional, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from entities import Actor, Entity, Equipment, Item

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
    def target_actor(self) -> (Actor | None):
        '''
        Returns an actor at this action's destination.
        '''

        return self.engine.map.get_actor_at(*self.dest_xy)

    @property
    def target_equipment(self) -> (Equipment | None):
        '''
        Returns a piece of equipment at this action's destination.
        '''
        return self.engine.map.get_equipment_at(*self.dest_xy)

    @property
    def target_item(self) -> (Item | None):
        '''
        Returns the item at this action's destination.
        '''

        if (self.engine.map.get_item_at(*self.dest_xy) is None 
            or  self.engine.map.get_item_at(*self.dest_xy).active is False):
            return None
        else:
            return self.engine.map.get_item_at(*self.dest_xy)
    
    @property
    def destination_is_exit(self):
        '''
        Returns True if the destination is the exit tile and False otherwise.
        '''

        dest_x, dest_y = self.dest_xy
        exit_x, exit_y = self.engine.map.exit_location
        
        if dest_x == exit_x and dest_y == exit_y:
            return True
        
        return False

    def perform(self) -> None:
        '''
        This method must be overridden by ActionWithDirection subclasses.
        '''
        
        raise NotImplementedError()