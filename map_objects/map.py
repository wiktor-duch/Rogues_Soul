from __future__ import annotations

from map_objects.tile import Tile
from map_objects.rectangle import Rectangle as Rect
from typing import Iterable, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entities.entity import Entity
class Map:
    '''
    Generates a new game map.
    '''

    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity]=()):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles: List[List[Tile]] = self.initialize_tiles()
        self.rooms: List[Rect] = []

    def get_blocking_entity_at(self, x_coord: int, y_coord: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == x_coord and entity.y == y_coord:
                return entity
        
        return None

    def initialize_tiles(self) -> List[List[Tile]]:
        '''
        Initialize the 2D array of Tiles.
        '''
        
        tiles = [[Tile() for x in range(self.width)] for y in range(self.height)]
        return tiles
    
    def is_blocked(self, x_coord: int, y_coord: int) -> bool:
        '''
        Returns true if a tile is blocked.
        '''

        if self.tiles[y_coord][x_coord].blocked:
            return True
        
        return False
    
    def discover_room(self, room: Rect) -> None:
        '''
        Sets all tiles in a room to discovered
        '''

        for y in range(room.y1, room.y2+1):
            for x in range(room.x1, room.x2+1):
                self.tiles[y][x].discovered = True
            
    def in_bounds(self, x_coord: int, y_coord: int) -> bool:
        '''
        Return True if x and y are inside of the bounds of this map.
        '''
        
        return 0 <= x_coord < self.width and 0 <= y_coord < self.height