from __future__ import annotations

from copy import deepcopy
from typing import Optional, Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from map_objects.map import Map

E = TypeVar('E', bound='Entity')

class Entity:
    '''
    A generic object to represent player, enemies, items, etc.
    '''

    map: Map

    def __init__(
        self,
        map: Optional[Map] = None,
        x: int = 0,
        y: int = 0,
        char: str = '!',
        name: str = '<Unnamed>',
        blocks_movement: bool = False
        ):

        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.blocks_movement = blocks_movement
        if map:
            # If map is not provided now, it will be set later
            self.map = map
            map.entities.add(self)

    def spawn(self: E, map: Map, x: int, y: int) -> E:
        '''
        Spawn a copy of this instance at the given x and y position.
        '''
        
        clone = deepcopy(self)
        clone.x = x
        clone.y = y
        clone.map = map
        map.entities.add(clone)
        return clone
    
    def place(self, x: int, y: int, map: Optional[Map] = None) -> None:
        '''
        Places entities at new locations and handles moving across maps
        '''

        self.x = x
        self.y = y
        if map:
            if hasattr(self, 'map'): # Can be uninitialized
                self.map.entities.remove(self)
            self.map = map
            map.entities.add(self)


    def move(self, dx: int, dy: int) -> None:
        '''
        Changes the x and y coordinates of the entity.
        '''

        self.x += dx
        self.y += dy