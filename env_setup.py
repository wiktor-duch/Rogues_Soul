'''
Handles initialization of the engine for the OpenAI custom environment.
'''
from copy import deepcopy
from typing import Dict, List, Tuple

from game.engine import Engine
from game.entities import Actor, entity_factory, Equipment
from game.exceptions import InvalidMap
from game.map_objects import World

def new_engine(verbose:bool = False) -> Engine:
    '''
    Returns a new game session as an Engine instance.
    '''

    # GENERAL CONFIGURATION
    num_levels = 1
    game_mode = 0 # Hides the undiscovered tiles if 0 and shows all tiles if 1

    # SPACE CONFIGURATION
    map_width = 20 # (tiles)
    # NOTE: Width should be above 10 to render statistics bar (see helper functions) 
    map_height = 20 # (tiles)

    # Room sizes means the dimensions inside the room (NOT COUNTING WALLS)
    room_max_size = 6
    room_min_size = 4 # Should not be below 4 as otherwise it may generate errors
    num_rooms_per_level: List[Tuple[int, int, int]] = [
        # Level, Min, Max
        (1, 3, 3),
    ]

    # ENTITY CONFIGURATION
    num_enemies_per_level: List[Tuple[int, int, int]] = [
        # Level, Min, Max
        (1, 1, 2),
    ]
    enemy_types_per_level: Dict[int, List[Tuple[Actor, int]]] = {
        # Key: Level, Value: [(Entity, Percentage), ...]
        1: [(entity_factory.bat, 80), (entity_factory.demon, 20)],
    }
    num_health_potions_per_level: List[Tuple[int, int, int]] = [
        # Level, Min, Max
        (1, 0, 1)
    ]
    num_souls_per_level: List[Tuple[int, int, int]] = [
        # Level, Min, Max
        (1, 1, 1)
    ]
    num_chests_per_level: List[Tuple[int, int, int]] = [ # No chests for now
        # Level, Min, Max
        (1, 0, 0),
    ]
    # Equipment configuration
    equipment_per_level: Dict[int, List[Equipment]] = { # Will not spawn for now
        # Key: Level, Value: [Equipment, ...]
        1: [
            entity_factory.short_sword,
            entity_factory.soldiers_shield,
            entity_factory.light_chain_mail
        ],
    }
    # The higher, the more pieces of equipment can be placed on the map
    spawn_equipment_prob = 0.0
    if verbose:
        print('Engine configuration loaded...')

    # Spawns an agent
    agent = deepcopy(entity_factory.agent)
    if verbose:
        print('Agent spawned...')

    #Initializes engine
    engine = Engine(agent, num_levels, game_mode)

    # Initializes world
    engine.world = World(
        engine=engine,
        map_width = map_width, 
        map_height = map_height,
        room_min_size = room_min_size,
        room_max_size = room_max_size,
        num_rooms_per_level = num_rooms_per_level,
        num_enemies_per_level = num_enemies_per_level,
        enemy_types_per_level=enemy_types_per_level,
        num_health_potions_per_level = num_health_potions_per_level,
        num_souls_per_level = num_souls_per_level,
        num_chests_per_level= num_chests_per_level,
        spawn_equipment_prob = spawn_equipment_prob,
        equipment_per_level = equipment_per_level
    )
    if verbose:
        print('World initialized...')

    return engine

def new_map(engine:Engine, verbose:bool=False) -> bool:
    '''
    Creates new map instance.

    Returns True if map was correctly generated and False otherwise.
    '''
    
    # Create a new dungeon
    try:
        engine.world.generate_level()
        if verbose:
            print('New level generated...\n')
    except InvalidMap as exc:
        print(f'Error: Could not generated the level.\nError Message: {exc}')
        return False
    
    return True