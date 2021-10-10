from __future__ import annotations

from vizualization.render_order import RenderOrder

from copy import deepcopy
from typing import Optional, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from map_objects import Map

E = TypeVar('E', bound='Entity')

class Entity:
    '''
    A generic object to represent player, enemies, items, etc.
    '''

    parent: Map

    def __init__(
        self,
        parent: Optional[Map] = None,
        x: int = 0,
        y: int = 0,
        char: str = 'U',
        name: str = '<Unnamed>',
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
        ):

        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            # If parent is not provided now, it will be set later
            self.parent = parent
            parent.entities.add(self)

    @property
    def map(self) -> Map:
        return self.parent

    def spawn(self: E, map: Map, x: int, y: int) -> E:
        '''
        Spawn a copy of this instance at the given x and y position.
        '''
        
        clone = deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = map
        map.entities.add(clone)
        return clone
    
    def place(self, x: int, y: int, map: Optional[Map] = None) -> None:
        '''
        Places entities at new locations and handles moving across maps
        '''

        self.x = x
        self.y = y
        if map:
            if hasattr(self, 'parent'): # Can be uninitialized
                if self.parent is self.map:
                    self.map.entities.remove(self)
            self.parent = map
            map.entities.add(self)


    def move(self, dx: int, dy: int) -> None:
        '''
        Changes the x and y coordinates of the entity.
        '''

        self.x += dx
        self.y += dy