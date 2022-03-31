'''
Inspired by:
http://rogueliketutorials.com/tutorials/tcod/v2/
'''
from game.entities import Entity
from game.map_objects import TILE_TYPE, Tile, Map
from typing import Tuple

def get_8_nearest_tiles(map: Map, x: int, y: int)-> Tuple[Tile]:
    '''
    Returns 8 nearest tiles to the given coordinates.
    '''

    return (map.tiles[y][x-1], map.tiles[y-1][x-1],
            map.tiles[y-1][x], map.tiles[y-1][x+1],
            map.tiles[y][x+1], map.tiles[y+1][x+1],
            map.tiles[y+1][x], map.tiles[y+1][x-1])

def discover_tiles(map: Map, agent: Entity) -> bool:
    '''
    Sets discovered to True for tiles in a given field of view radius.
    - If agent is located at the entrance tile of the room, then the 
      entire room is discovered.
    - Ig agent is located at the corridor tile, then the next 
      8 nearest tiles are discovered.

    Returns a pair of boolean values.
    First one is True if the new room was discovered and False otherwise.
    Second one is True if the corridor tiles were discovered and False otherwise.
    '''

    room_updated, corr_updated = False, False
    nearest_tiles = get_8_nearest_tiles(map, agent.x, agent.y)

    if map.tiles[agent.y][agent.x].type == TILE_TYPE.CORRIDOR:
        for tile in nearest_tiles:
            if ((tile.type == TILE_TYPE.CORRIDOR or tile.type == TILE_TYPE.ENTRANCE)
                and tile.discovered is False):
                tile.discovered = True
                corr_updated = True

    elif map.tiles[agent.y][agent.x].type == TILE_TYPE.ENTRANCE:
        # Check which room agent is about to enter
        for room in map.rooms:
            if room.intersects_tile_at(agent.x, agent.y):
                room_x, room_y = room.center
                # If room is not discovered yet
                if map.tiles[room_y][room_x].discovered is False:
                    map.discover_room(room)
                    room_updated = True
                # Discover all corridor tiles around the entrance
                for tile in nearest_tiles:
                    if ((tile.type == TILE_TYPE.CORRIDOR or tile.type == TILE_TYPE.ENTRANCE)
                        and tile.discovered is False):
                        tile.discovered = True
                        corr_updated = True
                break
    return room_updated, corr_updated

