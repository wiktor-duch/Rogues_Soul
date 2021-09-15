from map_objects.map import Map
from entities.entity import Entity
from typing import Set
from map_objects.tile import TILE_TYPE

def render_map(map: Map, GAME_MODE_ON: bool) -> None:
    '''
    Renders the entire map.
    '''
    
    for y in range(map.height):
        for x in range(map.width):
            # If tile is undiscovered is rendered as a space
            if GAME_MODE_ON:
                if not map.tiles[y][x].discovered:
                    print(' ', end='')
                else:
                    entity_drawn = draw_entity(map.entities, x, y)
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
            
            # Activates development mode
            else:
                if map.tiles[y][x].type == TILE_TYPE.BACKGROUND:
                    print(' ', end='')
                else:
                    entity_drawn = draw_entity(map.entities, x, y)
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

def draw_entity(entities: Set[Entity], x_coord: int, y_coord: int) -> bool:
    '''
    Checks if there is an entity at the given coordinates to be drawn.
    Returns true if there is one.
    '''

    for entity in entities:
        if x_coord == entity.x and y_coord == entity.y:
            print(entity.char, end='')
            return True
    return False

def draw_game_title() -> None:
    '''
    Prints big game's title while launching the game.
    '''

    title = ''

    print(title)