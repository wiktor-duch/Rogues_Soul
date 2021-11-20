from typing import List
import numpy as np
from game.map_objects import Map, TILE_TYPE
from game.entities import Item, Equipment, Actor

# Tiles have values 0 to 9
tile_type_to_int = {
    TILE_TYPE.BACKGROUND: 0,
    TILE_TYPE.FLOOR : 1,
    TILE_TYPE.V_WALL : 2,
    TILE_TYPE.H_WALL : 2,
    TILE_TYPE.ENTRANCE : 3,
    TILE_TYPE.CORRIDOR : 4,
    TILE_TYPE.EXIT : 5
}

# Enemies have values 10 to 19
enemy_to_int = {
    'Bat' : 10,
    'Crow' : 11,
    'Demon' : 12,
    'Knight': 13,
    'Agent' : 19
}

# Items have values 20 to 29
item_to_int = {
    'Health Potion' : 20,
    'Soul' : 21,
    'Chest' : 22
}

# Pieces of equipment have values 30-39
equipment_to_int = {
    'Short Sword' : 30,
    'Soldier\'s Shield' : 31,
    'Light Chain Mail' : 32,
    'Long Sword' : 33,
    'Kite Shield' : 34,
    'Cursed Rogue\'s Armour' : 35 # Current max value
}

def get_min_value_in_obs_space() -> int:
    '''
    Returns the lowest value that can occur in the observation space.
    '''
    return 0

def get_max_value_in_obs_space() -> int:
    '''
    Returns the highest value that can occur in the observation space.
    '''
    return 40

def get_next_observation(map: Map) -> List[List[int]]:
    # obs_space = np.empty(shape=(map.height+1, map.width), dtype=np.int16)
    obs_space = [[-1 for x in range(map.width)] for y in range(map.height+1)]

    for y in range(map.height):
        for x in range(map.width):
            if map.engine.get_game_mode() == 0:
                
                if not map.tiles[y][x].discovered: # Sets undiscovered tiles to background
                    obs_space[y][x] = tile_type_to_int.get(TILE_TYPE.BACKGROUND)
                else:
                    entity_added = add_entity(map, x, y, obs_space)
                    if entity_added is False:
                        obs_space[y][x] = tile_type_to_int.get(map.tiles[y][x].type)
    
            elif map.engine.get_game_mode() == 1:
                
                entity_added = add_entity(map, x, y, obs_space)
                if entity_added is False:
                    obs_space[y][x] = tile_type_to_int.get(map.tiles[y][x].type)

    # Last row contains agents statistics
    last_y = map.height

    # Set Level
    obs_space[last_y][0] = map.engine.level
    obs_space[last_y][1] = map.engine.num_levels
    # Set Souls
    obs_space[last_y][2] = map.engine.agent.souls
    # Set HP
    obs_space[last_y][3] = map.engine.agent.fighter.hp
    obs_space[last_y][4] = map.engine.agent.fighter.max_hp
    # Set Power
    obs_space[last_y][5] = map.engine.agent.fighter.power
    # Set Defense
    obs_space[last_y][6] = map.engine.agent.fighter.defense

    for x in range(7, map.width):
        obs_space[last_y][x] = tile_type_to_int.get(TILE_TYPE.BACKGROUND)

    obs_space = np.array(obs_space)

    return obs_space   

def add_entity(map: Map, x: int, y: int, arr: List[List[int]]) -> bool:
    '''
    Checks if there is an entity at the given coordinates to 
    be added to observation space.
    
    Returns True if there is one and False otherwise.
    '''
    entities = map.entities

    entities_sorted_for_rendering = sorted(
        entities, key=lambda x: x.render_order.value
    )

    if len(entities_sorted_for_rendering) != 0:
        for entity in entities_sorted_for_rendering:
            if x == entity.x and y == entity.y:
                if isinstance(entity, Item):
                    arr[y][x] = item_to_int.get(entity.name)
                elif isinstance(entity, Actor):
                    if entity.is_alive():
                        arr[y][x] = enemy_to_int.get(entity.name)
                    else:
                        arr[y][x] = tile_type_to_int.get(entity.name)
                elif isinstance(entity, Equipment):
                    arr[y][x] = equipment_to_int.get(entity.name)
                else:
                    print('No such entity type defiend in helper functions.')
                    return False
                
                return True
    
    return False            