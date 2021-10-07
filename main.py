from copy import deepcopy

from engine import Engine
from entities import entity_factory
from map_objects.map_generator import generate_dungeon

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
    max_monsters_per_room = 2
    min_monsters_per_room = 1
    game_mode_on = True # Hides the undiscovered tiles if True
    verbose = False # Prints some additional information while game loading
    print('Loading Rogue\'s Soul...')

    # Spawns an agent
    agent = deepcopy(entity_factory.agent)
    if verbose:
        print('Player/Agent spawned...')

    #Initialize engine
    engine = Engine(agent, game_mode_on)

    # Create map
    if verbose:
        print('Generating the dungeon...')
    engine.map = generate_dungeon(
        min_rooms, 
        max_rooms, 
        room_min_size,
        room_max_size,
        min_monsters_per_room,
        max_monsters_per_room,
        terminal_width, 
        terminal_height, 
        engine)
    
    if verbose:
        print('Dungeon generated..')
 
    # Game mainloop
    while not engine.game_over:
        engine.render()
        engine.event_handler.handle_events()

if __name__ == '__main__':
    main()