'''
Handles initialization of game.

Adapted from:
http://rogueliketutorials.com/tutorials/tcod/v2/
'''
from copy import deepcopy
from typing import Dict, List, Tuple

from game.engine import Engine
from game.entities import Actor, entity_factory, Equipment
from game.exceptions import InvalidMap
from game.map_objects import World
from game.vizualization import render_game_intro

def new_engine(render_info:bool = False, verbose:bool = False) -> Engine:
    '''
    Returns a new game session as an Engine instance.
    '''

    # ENGINE CONFIGURATION
    num_levels = 3
    game_mode = 0 # Hides the undiscovered tiles if 0 and shows all tiles if 1

    # SPACE CONFIGURATION
    map_width = 50  # (tiles)
    # NOTE: Width should be above 10 to render statistics bar (see helper functions) 
    map_height = 25  # (tiles)
    
    # Room sizes means the dimensions inside the room (NOT COUNTING WALLS)
    room_max_size = 8
    room_min_size = 4 # Should not be below 4 as otherwise it may generate errors
    num_rooms_per_level: List[Tuple[int, int, int]] = [
        # Level, Min, Max
        (1, 3, 4),
        (2, 4, 6),
        (3, 5, 8)
    ]

    # ENTITY CONFIGURATION
    num_enemies_per_level: List[Tuple[int, int, int]] = [
        # Level, Min, Max
        (1, 1, 2),
        (2, 2, 2),
        (3, 2, 3)
    ]
    enemy_types_per_level: Dict[int, List[Tuple[Actor, int]]] = {
        # Key: Level, Value: [(Entity, Percentage)...]
        1: [(entity_factory.bat, 90), (entity_factory.demon, 10)],
        2: [(entity_factory.crow, 70), (entity_factory.lost_knight, 30)],
        3: [(entity_factory.rat, 50), (entity_factory.skeleton, 50)]
    }
    num_health_potions_per_level: List[Tuple[int, int, int]] = [
        # Level, Min, Max
        (1, 1, 1),
        (2, 0, 1)
    ]
    num_souls_per_level: List[Tuple[int, int, int]] = [
        # Level, Min, Max
        (1, 1, 1)
    ]
    num_chests_per_level: List[Tuple[int, int, int]] = [
        # Level, Min, Max
        (1, 0, 1)
    ]
    # Equipment configuration
    equipment_per_level: Dict[int, List[Equipment]] = {
        # Key: Level, Value: [Equipment, ...]
        1: [
            entity_factory.short_sword,
            entity_factory.soldiers_shield,
            entity_factory.light_chain_mail
        ],
        2: [
            entity_factory.long_sword,
            entity_factory.kite_shield,
            entity_factory.cursed_rogues_armour
        ],
        3: [
            entity_factory.bastard_sword,
            entity_factory.greatshield,
            entity_factory.dragon_armour
        ]
    }
    # The higher, the more pieces of equipment can be placed on the map
    spawn_equipment_prob = 0.85

    if render_info:
        render_game_intro()

    if verbose:
        print('Loading Rogue\'s Soul...')

    # Spawns an agent
    agent = deepcopy(entity_factory.agent)
    if verbose:
        print('Player/Agent spawned...')

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
    return engine

def new_map(engine:Engine, verbose:bool=False) -> bool:
    '''
    Creates new map instance.

    Returns True if map was correctly generated and False otherwise.
    '''
    
    if verbose:
        print('Generating the dungeon...')
    
    # Create map
    try:
        engine.world.generate_level()
    except InvalidMap as exc:
        print(f'Error occured while map generation.\n{exc}')
        return False
    
    if verbose:
        print('Dungeon generated...\n')
    
    return True