from map_objects.map import Map
from entity import Entity
from typing import List
from map_objects.tile import TILE_TYPE

def render_all(
    entities: List[Entity],
    map: Map,
    terminal_width: int,
    terminal_height: int
    ) -> None:
    '''
    Renders the entire map.
    '''
    
    for y in range(terminal_height):
        for x in range(terminal_width):
            background = map.tiles[y][x].block_sight
            if background:
                print(' ', end='')
            else:
                entity_drawn = draw_entity(entities, x, y)
                if entity_drawn is False:
                    if map.tiles[y][x].type == TILE_TYPE.V_WALL:
                        print("|", end="")
                    elif map.tiles[y][x].type == TILE_TYPE.H_WALL:
                        print("-", end="")
                    elif map.tiles[y][x].type == TILE_TYPE.CORRIDOR:
                        print('#', end='')
                    elif map.tiles[y][x].type == TILE_TYPE.ENTRANCE:
                        print('+', end='')
                    else:
                        print('.', end='')
        print('')

def draw_entity(entities: List[Entity], x_coord: int, y_coord: int) -> bool:
    '''
    Checks if there is an entity at the given coordinates to be drawn.
    Returns true if there is one.
    '''
    for entity in entities:
        if x_coord == entity.x and y_coord == entity.y:
            print(entity.char, end='')
            return True
    return False
