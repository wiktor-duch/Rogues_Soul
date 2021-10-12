from copy import deepcopy
import traceback

from engine import Engine
from entities import entity_factory
from map_objects import generate_dungeon
from vizualization import render_game_intro

'''
Based on:
http://rogueliketutorials.com/tutorials/tcod/v2/
https://www.youtube.com/watch?v=zAVEsKPq8x0
'''

def main():
    # CONFIGURATION SPACE
    terminal_width = 80
    terminal_height = 25
    # Room sizes means the dimensions inside the room (NOT COUNTING WALLS)
    room_max_size = 8
    room_min_size = 4 # Should not be below 4 as otherwise it may generate errors
    max_rooms = 12
    min_rooms = 6
    max_enemies_per_room = 2
    min_enemies_per_room = 1
    max_health_potions_per_room = 1
    min_health_potions_per_room = 0
    num_levels=3
    game_mode_on = True # Hides the undiscovered tiles if True
    verbose = False # Prints some additional information while game loading

    render_game_intro()

    print('Loading Rogue\'s Soul...')

    # Spawns an agent
    agent = deepcopy(entity_factory.agent)
    if verbose:
        print('Player/Agent spawned...')

    #Initialize engine
    engine = Engine(agent, num_levels, game_mode_on)

    # Add welcome message
    engine.message_log.add_message('Rogue\'s Soul: Welcome to your grave and destiny my lost soul eater.')

    # Create map
    if verbose:
        print('Generating the dungeon...')
    engine.map = generate_dungeon(
        min_rooms, 
        max_rooms, 
        room_min_size,
        room_max_size,
        min_enemies_per_room,
        max_enemies_per_room,
        min_health_potions_per_room,
        max_health_potions_per_room,
        terminal_width, 
        terminal_height, 
        engine)
    
    if verbose:
        print('Dungeon generated...\n')
    else:
        print('')
    
    # Game mainloop
    while not engine.game_over:
        engine.render()
        
        try:
            engine.event_handler.handle_events()
        except Exception:
            engine.message_log.add_message(traceback.format_exc())
        
        print('\n') # Adds a line break beetween terminal outputs

if __name__ == '__main__':
    main()