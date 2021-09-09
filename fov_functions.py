from entity import Entity
from map_objects.tile import TILE_TYPE, Tile
from map_objects.map import Map
from typing import Tuple

def get_8_nearest_tiles(map: Map, x_coord: int, y_coord: int)-> Tuple[Tile]:
    '''
    Returns 8 nearest tiles to the given coordinates.
    '''

    return (map.tiles[y_coord][x_coord-1], map.tiles[y_coord-1][x_coord-1],
            map.tiles[y_coord-1][x_coord], map.tiles[y_coord-1][x_coord+1],
            map.tiles[y_coord][x_coord+1], map.tiles[y_coord+1][x_coord+1],
            map.tiles[y_coord+1][x_coord], map.tiles[y_coord+1][x_coord-1])

def discover_tiles(map: Map, agent: Entity) -> None:
    '''
    Sets discovered to True for tiles in a given field of view radius.
    - If agent is located at the entrance tile of the room, then the 
      entire room is discovered.
    - Ig agent is located at the corridor tile, then the next 
      8 nearest tiles are discovered.
    '''
    nearest_tiles = get_8_nearest_tiles(map, agent.x, agent.y)

    if map.tiles[agent.y][agent.x].type == TILE_TYPE.CORRIDOR:
        for tile in nearest_tiles:
            if ((tile.type == TILE_TYPE.CORRIDOR or tile.type == TILE_TYPE.ENTRANCE)
                and tile.discovered is False):
                tile.discovered = True

    elif map.tiles[agent.y][agent.x].type == TILE_TYPE.ENTRANCE:
        # Check which room agent is about to enter
        for room in map.rooms:
            if room.intersect_tile_at(agent.x, agent.y):
                room_x, room_y = room.center()
                # If room is not discovered yet
                if map.tiles[room_y][room_x].discovered is False:
                    map.discover_room(room)

                # Discover all corridor tiles around the entrance
                for tile in nearest_tiles:
                    if ((tile.type == TILE_TYPE.CORRIDOR or tile.type == TILE_TYPE.ENTRANCE)
                        and tile.discovered is False):
                        tile.discovered = True
                break

