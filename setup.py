'''
Handles initialization of game.
'''
from copy import deepcopy

from engine import Engine
from entities import entity_factory
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
    room_max_size = 8
    room_min_size = 4 # Should not be below 4 as otherwise it may generate errors
    max_rooms = 12
    min_rooms = 6

    # ENTITY CONFIGURATION
    max_enemies_per_room = 2
    min_enemies_per_room = 1
    max_health_potions_per_room = 1
    min_health_potions_per_room = 0
    max_souls_per_room = 1
    min_souls_per_room = 1
    max_chests_per_room = 1
    min_chests_per_room = 0

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
        engine = engine,
        map_width = map_width, 
        map_height = map_height,
        min_rooms = min_rooms, 
        max_rooms = max_rooms, 
        room_min_size = room_min_size,
        room_max_size = room_max_size,
        min_enemies_per_room = min_enemies_per_room,
        max_enemies_per_room = max_enemies_per_room,
        min_health_potions_per_room = min_health_potions_per_room,
        max_health_potions_per_room = max_health_potions_per_room,
        min_souls_per_room = min_souls_per_room,
        max_souls_per_room = max_souls_per_room,
        min_chests_per_room = min_chests_per_room,
        max_chests_per_room = max_chests_per_room
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