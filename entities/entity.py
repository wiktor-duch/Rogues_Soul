from __future__ import annotations

from copy import deepcopy
from typing import Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from map_objects.map import Map

E = TypeVar('E', bound='Entity')

class Entity:
    """
    A generic object to represent player, enemies, items, etc.
    """

    def __init__(
        self,
        x_coord: int = 0,
        y_coord: int = 0,
        char: str = '!',
        name: str = '<Unnamed>',
        blocks_movement: bool = False
        ):

        self.x = x_coord
        self.y = y_coord
        self.char = char
        self.name = name
        self.blocks_movement = blocks_movement

    def spawn(self: E, map: Map, x_coord: int, y_coord: int) -> E:
        '''
        Spawn a copy of this instance at the given x and y position.
        '''
        
        clone = deepcopy(self)
        clone.x = x_coord
        clone.y = y_coord
        map.entities.add(clone)
        return clone

    def move(self, dx: int, dy: int) -> None:
        '''
        Changes the x and y coordinates of the entity.
        '''

        self.x += dx
        self.y += dy