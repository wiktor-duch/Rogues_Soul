'''
Handles initialization of game.
'''
from copy import deepcopy
from typing import Dict, List, Tuple

from engine import Engine
from entities import entity_factory
from entities.entity import Entity
from exceptions import InvalidMap
from map_objects import World
from vizualization import render_game_intro

def new_engine(render_info:bool = False, verbose:bool = False) -> Engine:
    '''
    Returns a new game session as an Engine instance.
    '''

    # ENGINE CONFIGURATION
    num_levels = 2
    game_mode_on = True # Hides the undiscovered tiles if True

    # SPACE CONFIGURATION
    map_width = 80
    map_height = 25
    
    # Room sizes means the dimensions inside the room (NOT COUNTING WALLS)
    room_max_size = 6
    room_min_size = 4 # Should not be below 4 as otherwise it may generate errors
    num_rooms_per_level: List[Tuple[int, int, int]] = [
        # Level, Min, Max
        (1, 5, 10),
        (2, 7, 12)
    ]

    # ENTITY CONFIGURATION
    num_enemies_per_level: List[Tuple[int, int, int]] = [
        # Level, Min, Max
        (1, 1, 2),
        (2, 1, 3)
    ]
    enemy_types_per_level: Dict[int, List[Tuple[Entity, int]]] = {
        # Key: Level, Value: [(Entity, Percentage)...]
        1: [(entity_factory.bat, 80), (entity_factory.demon, 20)],
        2: [(entity_factory.crow, 70), (entity_factory.lost_knight, 30)]
    }
    num_health_potions_per_level: List[Tuple[int, int, int]] = [
        # Level, Min, Max
        (1, 0, 1)
    ]
    num_souls_per_level: List[Tuple[int, int, int]] = [
        # Level, Min, Max
        (1, 1, 1)
    ]
    num_chests_per_level: List[Tuple[int, int, int]] = [
        # Level, Min, Max
        (1, 0, 1),
        (2, 0, 2)
    ]

    if render_info:
        render_game_intro()

    if verbose:
        print('Loading Rogue\'s Soul...')

    # Spawns an agent
    agent = deepcopy(entity_factory.agent)
    if verbose:
        print('Player/Agent spawned...')

    #Initializes engine
    engine = Engine(agent, num_levels, game_mode_on)

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