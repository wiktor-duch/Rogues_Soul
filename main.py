from copy import deepcopy

from engine import Engine
from entities import entity_factory
from map_generator import generate_dungeon

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
    room_min_size = 4 # Cannot be below 4 as otherwise it generates errors
    max_rooms = 12
    min_rooms = 6
    max_monsters_per_room = 2
    min_monsters_per_room = 0
    GAME_MODE_ON = True # Hides the undiscovered tiles if True
    print('Loading Rogue\'s Soul')

    # Spawns an agent
    agent = deepcopy(entity_factory.agent)

    # Create map
    map = generate_dungeon(
        min_rooms, 
        max_rooms, 
        room_min_size,
        room_max_size,
        min_monsters_per_room,
        max_monsters_per_room,
        terminal_width, 
        terminal_height, 
        agent)
    
    #Initialize engine
    engine = Engine(agent, map, GAME_MODE_ON)

    # Game mainloop
    gameOver = False
    while not gameOver:
        engine.render()
        key = input('Enter your choice: ')
        gameOver = engine.handle_events(key)

if __name__ == '__main__':
    main()