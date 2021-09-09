from engine import Engine
from input_handler import handle_keys
from entity import Entity
from map_objects.map import Map
import engine

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
    
    print('Rogue\'s Soul')

    # Create entities
    agent = Entity(int(terminal_width/2), int(terminal_height/2), '@')
    npc = Entity(int(terminal_width/2-2), int(terminal_height/2+2), 'n')
    entities = [agent, npc]

    # Create map
    map = Map(terminal_width, terminal_height)
    map.generate_dungeon(min_rooms, max_rooms, room_min_size, room_max_size, terminal_width, terminal_height, agent)
    
    #Initialize engine
    engine = Engine(entities, agent, map)

    # Game mainloop
    gameOver = False
    while not gameOver:
        engine.render(terminal_width, terminal_height)
        key = input('Enter your choice: ')
        gameOver = engine.handle_events(key)

if __name__ == '__main__':
    main()