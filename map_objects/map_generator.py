from __future__ import annotations

from entities import entity_factory
from exceptions import InvalidMap
from map_objects.map import Map
from map_objects.rectangle import Rectangle as Rect
from map_objects.tile import TILE_TYPE
from random import randint, choices, random, choice

from typing import TYPE_CHECKING, Dict, List, Tuple

if TYPE_CHECKING:
    from engine import Engine
    from entities import Item, Entity, Equipment

def place_item(
    map: Map,
    room: Rect,
    max_loops: int,
    item: Item,
    num_items_to_place: int
) -> None:
    '''
    Randomly places the given type of items in a provided room. Number of the items
    to be placed must also be specified.
    '''
    num_loops = 0
    num_items_placed = 0

    while num_items_placed < num_items_to_place:

        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in map.entities):
            item.spawn(map, x, y)
            num_items_placed += 1
        
        if num_loops > max_loops:
            raise InvalidMap(f'ERROR: Could not generate the minimum number of {item.name} specified!')

        num_loops += 1

def place_equipment(
    map: Map,
    room: Rect,
    max_loops: int,
    equipment_list: List[Equipment],
    spawn_equipment_prob: float
) -> None:
    '''
    Places one piece of equipment if it is not already placed on the map.
    '''
    equipment_available = []

    # Check for available equipment
    if map.equipment:
        for eq in equipment_list:
            available = True
            for item in map.equipment:
                if item.equippable.equipment_type == eq.equippable.equipment_type:
                    available = False
            if available:
                equipment_available.append(eq)
    else:
        equipment_available = equipment_list
    
    if len(equipment_available) > 0: # There are pieces of equipment which still can be placed
        # Choose a random piece of equipment
        item = choice(equipment_available)
        
        if random() < spawn_equipment_prob:
            num_loops = 0

            for _ in range(max_loops):

                x = randint(room.x1 + 1, room.x2 - 1)
                y = randint(room.y1 + 1, room.y2 - 1)

                if not any(entity.x == x and entity.y == y for entity in map.entities):
                    item.spawn(map, x, y)
                    break
                
                if num_loops > max_loops:
                    raise InvalidMap(f'ERROR: Could not generate the position for equipement to be placed!')

                num_loops += 1

def place_entities(
    map: Map,
    level: int,
    room: Rect, 
    num_enemies_per_level: List[Tuple[int, int, int]],
    enemy_types_per_level: Dict[int, List[Tuple[Entity, int]]],
    num_health_potions_per_level: List[Tuple[int, int, int]],
    num_souls_per_level: List[Tuple[int, int, int]],
    num_chests_per_level: List[Tuple[int, int, int]],
    equipment_per_level: Dict[int, List[Equipment]],
    spawn_equipment_prob: float,
) -> None:
    # Gets random number of monster in the room
    min_enemies, max_enemies = get_values_for_level(
        num_enemies_per_level, level
    )
    num_enemies = randint(min_enemies, max_enemies)
    
    min_health_potions, max_health_potions = get_values_for_level(
        num_health_potions_per_level, level
    )
    num_health_potions = randint(min_health_potions, max_health_potions)
    
    min_souls, max_souls = get_values_for_level(
        num_souls_per_level, level
    )
    num_souls = randint(min_souls, max_souls)
    
    min_chests, max_chests = get_values_for_level(
        num_chests_per_level, level
    )
    num_chests = randint(min_chests, max_chests)

    num_enemies_placed = 0

    num_loops = 0 # Ensures while loop breaks after a certain number of loops
    max_loops = 100

    # Place enemies
    enemies, probs = get_enemy_types_and_probs(
        enemy_types_per_level=enemy_types_per_level,
        level=level
    )
    if len(enemies) == 0:
        raise InvalidMap(f'ERROR: There are no enemy types to generate for level {level}')

    while num_enemies_placed < num_enemies:
        num_loops += 1

        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in map.entities):
            enemy: Entity = choices(
                enemies, weights=probs
            )[0]
            enemy.spawn(map, x, y)
            num_enemies_placed += 1
        
        if num_loops > max_loops:
            raise InvalidMap('ERROR: Could not generate the minimum number of enemies specified!')

    # Place health potions
    place_item(
        map=map,
        room=room,
        max_loops=max_loops,
        item=entity_factory.health_potion,
        num_items_to_place=num_health_potions
    )

    # Place souls
    place_item(
        map=map,
        room=room,
        max_loops=max_loops,
        item=entity_factory.soul,
        num_items_to_place=num_souls
    )

    # Place chests
    place_item(
        map=map,
        room=room,
        max_loops=max_loops,
        item=entity_factory.chest,
        num_items_to_place=num_chests
    )
    
    # Place equipment
    equipment_list = get_equipment_for_level(
        equipment_per_level=equipment_per_level,
        level=level
    )
    place_equipment(
        map=map,
        room=room,
        max_loops=max_loops,
        equipment_list=equipment_list,
        spawn_equipment_prob=spawn_equipment_prob
    )

def place_exit(map: Map) -> None:
    # Places the exit
    last_room = map.rooms[len(map.rooms)-1]
    
    for i in range(last_room.width*last_room.height):
        exit_x = randint(last_room.x1 + 2, last_room.x2 - 2)
        exit_y = randint(last_room.y1 + 2, last_room.y2 - 2)
        if not any(entity.x == exit_x and entity.y == exit_y for entity in map.entities):
            map.tiles[exit_y][exit_x].type = TILE_TYPE.EXIT
            map.tiles[exit_y][exit_x].blocked = False
            map.exit_location = (exit_x, exit_y)
            break
        if i == last_room.width*last_room.height -1:
            raise InvalidMap('Error: Could not generate the exit.')

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

def add_room_to_dungeon(map: Map, room: Rect) -> None:
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

def generate_new_rect(
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int
) -> Rect:
    '''
    Generates random dimensions for the room and returns the new Rectangle with this dimensions.
    '''

    # Random width and height. We add 1 to account for walls
    w = randint(room_min_size, room_max_size) +1
    h = randint(room_min_size, room_max_size) +1
    # Random position without going out of the boundaries of our map
    x = randint(1, map_width-w-1)
    y = randint(1, map_height-h-1)

    return Rect(x, y, w, h)

def get_values_for_level(
    values_by_level: List[Tuple[int, int, int]],
    level: int
) -> Tuple[int, int]:
    curr_min = 0
    curr_max = 0

    for level_min, min, max in values_by_level:
        if level_min > level:
            break
        else:
            curr_min = min
            curr_max = max

    return curr_min, curr_max

def get_equipment_for_level(
    equipment_per_level: Dict[int, List[Equipment]],
    level: int
) -> List[Equipment]:
    equipment = []

    for key, value in equipment_per_level.items():
        if key > level:
            break
        elif key == level:
            equipment = value

    return equipment

def get_enemy_types_and_probs(
    enemy_types_per_level: Dict[int, List[Tuple[Entity, int]]],
    level: int
) -> Tuple[List[Entity], List[int]]:
    '''
    Returns a dictionary of enemy types and the probabilities of them appearing.
    '''
    entities = []
    probs = []

    for key, values in enemy_types_per_level.items():
        if key > level:
            break
        elif key == level:
            for v in values:
                entities.append(v[0])
                probs.append(v[1])

    return entities, probs

def generate_dungeon(
    room_min_size: int,
    room_max_size: int,
    num_rooms_per_level: List[Tuple[int, int, int]],
    num_enemies_per_level: List[Tuple[int, int, int]],
    enemy_types_per_level: Dict[int, List[Tuple[Entity, int]]],
    num_health_potions_per_level: List[Tuple[int, int, int]],
    num_souls_per_level: List[Tuple[int, int, int]],
    num_chests_per_level: List[Tuple[int, int, int]],
    equipment_per_level: Dict[int, List[Equipment]],
    spawn_equipment_prob: float,
    map_width: int,
    map_height: int,
    engine: Engine
) -> Map:
    '''
    Generates a new dungeon with random room layout.
    '''

    agent = engine.agent
    dungeon = Map(engine, map_width, map_height, entities=[agent])
    level = engine.level

    min_rooms, max_rooms = get_values_for_level(num_rooms_per_level, level)
    num_rooms = 0

    for r in range(max_rooms):
        new_room = generate_new_rect(room_min_size, room_max_size, map_width, map_height)

        # Run through the other rooms and check if they intersect
        intersection = False
        for other_room in dungeon.rooms:
            if new_room.intersects_room(other_room):
                intersection = True
                break
        if not intersection:
            # There are no intersections, so this room is valid
            add_room_to_dungeon(dungeon, new_room)

            if num_rooms == 0:
                # Agent starts at this room
                agent.place(*new_room.center, dungeon)
                # Room is discovered
                dungeon.discover_room(new_room)
            else:
                # Add enemies
                place_entities(
                    map=dungeon,
                    level=level,
                    room=new_room, 
                    num_enemies_per_level=num_enemies_per_level,
                    enemy_types_per_level=enemy_types_per_level,
                    num_health_potions_per_level=num_health_potions_per_level,
                    num_souls_per_level=num_souls_per_level,
                    num_chests_per_level=num_chests_per_level,
                    equipment_per_level=equipment_per_level,
                    spawn_equipment_prob=spawn_equipment_prob
                )

            dungeon.rooms.append(new_room)
            num_rooms += 1
    
    # Last thing is to assure that we have at least min_rooms generated
    if num_rooms < min_rooms:
        num_loops = 0 # Ensures while loop breaks after a certain number of loops
        while num_rooms < min_rooms:
            num_loops += 1
            
            new_room = generate_new_rect(room_min_size, room_max_size, map_width, map_height)

            # Run through the other rooms and check if they intersect
            intersection = False
            for other_room in dungeon.rooms:
                if new_room.intersects_room(other_room):
                    intersection = True
                    break
            if not intersection:
                # There are no intersections, so this room is valid
                add_room_to_dungeon(dungeon, new_room)
                place_entities(
                    map=dungeon,
                    level=level,
                    room=new_room, 
                    num_enemies_per_level=num_enemies_per_level,
                    enemy_types_per_level=enemy_types_per_level,
                    num_health_potions_per_level=num_health_potions_per_level,
                    num_souls_per_level=num_souls_per_level,
                    num_chests_per_level=num_chests_per_level,
                    equipment_per_level=equipment_per_level,
                    spawn_equipment_prob=spawn_equipment_prob
                    )
                dungeon.rooms.append(new_room)
                num_rooms += 1
            
            if num_loops > 100:
                raise InvalidMap('ERROR: Could not generate the minimum number of rooms specified!')
    
    # Add the exit
    try:
        place_exit(map=dungeon)
    except InvalidMap as exc:
        raise exc

    # Connecting all rooms
    for i in range(1, len(dungeon.rooms)):
        # Getting the center of a current room
        (curr_x, curr_y) = dungeon.rooms[i].center

        # Getting the center of a current room
        (prev_x, prev_y) = dungeon.rooms[i-1].center

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