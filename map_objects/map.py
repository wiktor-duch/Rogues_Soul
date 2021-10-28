from __future__ import annotations

from entities import Actor, Item
from map_objects.tile import Tile
from map_objects.rectangle import Rectangle as Rect

from typing import (
    Iterable,
    Iterator,
    Optional,
    Tuple,
    List,
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from engine import Engine
    from entities import Entity
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

    @property
    def map(self) -> Map:
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        '''
        Iterates over this map's actors that are still alive.
        '''

        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive()
        )
    
    @property
    def items(self) -> Iterator[Item]:
        yield from (
            entity
            for entity in self.entities 
            if isinstance(entity, Item)
        )


    def get_blocking_entity_at(self, x: int, y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == x and entity.y == y:
                return entity
        
        return None
    
    def is_entity_at(self, x: int, y: int) -> bool:
        '''
        Returns True if there is an entity at x and y.
        '''
        
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                return True
        
        return False

    def check_for_duplicates(self, x: int, y:int) -> bool:
        '''
        Returns True is there are two entities at a tile with the
        given x and y coordinates 
        '''

        list_of_entity_coordinates: List[Tuple[int]] = []
        for entity in self.entities:
            list_of_entity_coordinates.append((entity.x, entity.y))

        num_entities = list_of_entity_coordinates.count((x, y))
        if num_entities > 1:
            return True
        else:
            return False

    def get_actor_at(self, x:int, y:int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        
        return None
    
    def get_item_at(self, x:int, y:int) -> Optional[Item]:
        for item in self.items:
            if item.x == x and item.y == y:
                return item
        
        return None

    def initialize_tiles(self) -> List[List[Tile]]:
        '''
        Initialize the 2D array of Tiles.
        '''
        
        tiles = [[Tile() for x in range(self.width)] for y in range(self.height)]
        return tiles
    
    def is_blocked(self, x: int, y: int) -> bool:
        '''
        Returns true if a tile is blocked.
        '''

        if self.tiles[y][x].blocked:
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