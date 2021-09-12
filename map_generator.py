from __future__ import annotations

from entities import entity_factory
from map_objects.map import Map
from map_objects.rectangle import Rectangle as Rect
from map_objects.tile import TILE_TYPE
from random import randint, random

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity
  
def place_enemies(map: Map, room: Rect, min_monsters: int, max_monsters: int):
    # Gets random number of monster in the room
    num_monsters = randint(min_monsters, max_monsters)

    for _ in range(num_monsters):
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in map.entities):
            if random() < 0.8:
                # Place a Bat here
                entity_factory.bat.spawn(map=map, x_coord=x, y_coord=y)
            else:
                # Place a Demon here
                entity_factory.demon.spawn(map=map, x_coord=x, y_coord=y)

def generate_vert_tunnel(map: Map, y1: int, y2: int, x: int) -> None:
    '''
    Creates a vertical tunnel between y1 and y2 at x.
    Requires list of rooms to set the tiles type.
    '''

    for y in range(min(y1, y2), max(y1,y2)+1):
        intersection = False
        entrance = False
        corner_detected = False
        
        # Checks if a tile intersects a room
        for room in map.rooms:
            if room.intersects_tile_at(x, y):
                intersection = True
                # Corner detection
                if ((x == room.x1 and y == room.y1) or (x == room.x1 and y == room.y2) or
                    (x == room.x2 and y == room.y1) or (x == room.x2 and y == room.y2)):
                    
                    corner_detected = True

                    # Check for right corner (from room perspective)
                    if room.intersects_tile_at(x-1, y):
                        x -= 1
                        # Check if there is no entrance on the left already
                        if not map.tiles[y][x-1].type == TILE_TYPE.ENTRANCE:
                            entrance = True
                        # If NOT a right bottom corner and the first tunnel tile
                        if map.tiles[y-1][x].type == TILE_TYPE.BACKGROUND and y > min(y1, y2):
                            map.tiles[y-1][x].type = TILE_TYPE.CORRIDOR
                            map.tiles[y-1][x].blocked = False
                        
                    # Left corner (from room perspective)
                    else:
                        x += 1
                        # Check if there is no entrance on the right already
                        if not map.tiles[y][x+1].type == TILE_TYPE.ENTRANCE:
                            entrance = True
                        # If NOT a left bottom corner and the first tunnel tile
                        if map.tiles[y-1][x].type == TILE_TYPE.BACKGROUND and y > min(y1, y2):
                            map.tiles[y-1][x].type = TILE_TYPE.CORRIDOR
                            map.tiles[y-1][x].blocked = False
                        
                # Wall detection
                if ((y == room.y1 or y == room.y2) and 
                    not (map.tiles[y][x-1].type == TILE_TYPE.ENTRANCE or map.tiles[y][x+1].type == TILE_TYPE.ENTRANCE)):
                    entrance = True
                
                break # Intersection found
        
        # The last tile
        if y == max(y1, y2):
            # Tunnel goes through the room and ends at the bottom wall
            if map.tiles[y-1][x].type == TILE_TYPE.FLOOR and entrance is True:
                return None # Don't go to the next if statement and end the method
        # The first tile
        elif y == min(y1, y2) and entrance is True:
            entrance = False
        
        # All tiles
        if entrance is True: # Entrance detected
            map.tiles[y][x].type = TILE_TYPE.ENTRANCE
            map.tiles[y][x].blocked = False
        
        elif intersection is False and corner_detected is False: # Corridor detected
            map.tiles[y][x].type = TILE_TYPE.CORRIDOR
            map.tiles[y][x].blocked = False

def generate_horiz_tunnel(map: Map, x1: int, x2: int, y: int) -> None:
    '''
    Creates a horizontal tunnel between x1 and x2 at y.
    Requires list of rooms to set the Tile type.
    '''

    for x in range(min(x1, x2), max(x1,x2)+1):
        intersection = False
        entrance = False
        corner_detected = False

        # Checks if a tile intersects a room
        for room in map.rooms:
            if room.intersects_tile_at(x, y):
                intersection = True
                # Corner detection
                if ((x == room.x1 and y == room.y1) or (x == room.x1 and y == room.y2) or
                    (x == room.x2 and y == room.y1) or (x == room.x2 and y == room.y2)):
                    
                    corner_detected = True

                    # Check for bottom corner (from room perspective)
                    if room.intersects_tile_at(x, y-1):
                        y -= 1
                        # Check if there is no entrance above already
                        if not map.tiles[y-1][x].type == TILE_TYPE.ENTRANCE:
                            entrance = True
                        # If NOT a right bottom corner and the first tunnel tile
                        if map.tiles[y][x-1].type == TILE_TYPE.BACKGROUND and x > min(x1, x2):
                            map.tiles[y][x-1].type = TILE_TYPE.CORRIDOR
                            map.tiles[y][x-1].blocked = False
                        
                    # Top corner (from room perspective)
                    else:
                        y += 1
                        # Check if there is no entrance below already
                        if not map.tiles[y+1][x].type == TILE_TYPE.ENTRANCE:
                            entrance = True
                        # If NOT a right top corner and the first tunnel tile
                        if map.tiles[y][x-1].type == TILE_TYPE.BACKGROUND and x > min(x1, x2):
                            map.tiles[y][x-1].type = TILE_TYPE.CORRIDOR
                            map.tiles[y][x-1].blocked = False
                        
                # Wall detection
                if ((x == room.x1 or x == room.x2) and 
                    not (map.tiles[y-1][x].type == TILE_TYPE.ENTRANCE or map.tiles[y+1][x].type == TILE_TYPE.ENTRANCE)):
                    entrance = True
                
                break # Intersection found
        
        # The last tile
        if x == max(x1, x2):
            # Tunnel goes through the room and ends at the right wall
            if map.tiles[y][x-1].type == TILE_TYPE.FLOOR and entrance is True:
                return None # Don't go to the next if statement and end the method
        # The first tile
        elif x == min(x1, x2) and entrance is True:
            entrance = False
        
        # All tiles
        if entrance is True: # Entrance detected
            map.tiles[y][x].type = TILE_TYPE.ENTRANCE
            map.tiles[y][x].blocked = False
        
        elif intersection is False and corner_detected is False: # Corridor detected
            map.tiles[y][x].type = TILE_TYPE.CORRIDOR
            map.tiles[y][x].blocked = False

def generate_room(map: Map, room: Rect) -> None:
    '''
    Creates a new room on the map.
    '''

    for y in range(room.y1, room.y2+1):
        for x in range(room.x1, room.x2+1):
            if x == room.x1 or x == room.x2:
                map.tiles[y][x].type = TILE_TYPE.V_WALL
                map.tiles[y][x].blocked = True
            elif y == room.y1 or y == room.y2:
                map.tiles[y][x].type = TILE_TYPE.H_WALL
                map.tiles[y][x].blocked = True
            else:
                map.tiles[y][x].type = TILE_TYPE.FLOOR
                map.tiles[y][x].blocked = False

def generate_new_room(
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int
    ) -> Rect:
    '''
    Generates random dimensions for the room and returns the new room with this dimensions
    '''

    # Random width and height. We add 1 to account for walls
    w = randint(room_min_size, room_max_size) +1
    h = randint(room_min_size, room_max_size) +1
    # Random position without going out of the boundaries of our map
    x = randint(1, map_width-w-1)
    y = randint(1, map_height-h-1)

    return Rect(x, y, w, h)

def generate_dungeon(
    min_rooms: int,
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    min_monsters_per_room: int,
    max_monsters_per_room: int,
    map_width: int,
    map_height: int, 
    agent: Entity
    ) -> Map:
    '''
    Generates a new dungeon with random room layout.
    '''

    dungeon = Map(map_width, map_height, entities=[agent])

    num_rooms = 0

    for r in range(max_rooms):
        new_room = generate_new_room(room_min_size, room_max_size, map_width, map_height)

        # Run through the other rooms and check if they intersect
        intersection = False
        for other_room in dungeon.rooms:
            if new_room.intersects_room(other_room):
                intersection = True
                break
        if not intersection:
            # There are no intersections, so this room is valid
            generate_room(dungeon, new_room)
            (new_x, new_y) = new_room.center()

            if num_rooms == 0:
                # Agent starts at this room
                agent.x = new_x
                agent.y = new_y
                # Room is discovered
                dungeon.discover_room(new_room)
            else:
                # Add enemies
                place_enemies(dungeon, new_room, min_monsters_per_room, max_monsters_per_room)

            dungeon.rooms.append(new_room)
            num_rooms += 1
    
    # Last thing is to assure that we have at least min_rooms generated
    if num_rooms < min_rooms:
        num_loops = 0 # Ensures while loop breaks after a certain number of loops
        while num_rooms < min_rooms:
            num_loops += 1
            
            new_room = generate_new_room(room_min_size, room_max_size, map_width, map_height)

            # Run through the other rooms and check if they intersect
            intersection = False
            for other_room in dungeon.rooms:
                if new_room.intersects_room(other_room):
                    intersection = True
                    break
            if not intersection:
                # There are no intersections, so this room is valid
                generate_room(dungeon, new_room)
                place_enemies(dungeon, new_room, min_monsters_per_room, max_monsters_per_room)
                dungeon.rooms.append(new_room)
                num_rooms += 1
            
            if num_loops > 100:
                print("ERROR: Could not generate the minimum number of rooms specified!")
                break
    
    # Connecting all rooms
    for i in range(1, len(dungeon.rooms)):
        # Getting the center of a current room
        (curr_x, curr_y) = dungeon.rooms[i].center()

        # Getting the center of a current room
        (prev_x, prev_y) = dungeon.rooms[i-1].center()

        # Connecting the current room to the previous one
        # Flip a coin to check if we go horziontally and then vertically or the other way 
        if randint(0,1) == 1:
            # First go horizontally and then vertically
            generate_horiz_tunnel(dungeon, prev_x, curr_x, prev_y)
            generate_vert_tunnel(dungeon, prev_y, curr_y, curr_x)
        else:
            generate_vert_tunnel(dungeon, prev_y, curr_y, prev_x)
            generate_horiz_tunnel(dungeon, prev_x, curr_x, curr_y)
    
    return dungeon