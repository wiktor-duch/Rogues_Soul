from entity import Entity
from vizualization.render_functions import render_all
from input_handler import handle_keys
from map_objects.map import Map
from typing import List

class Engine:
    def __init__(self, entities: List[Entity], agent: Entity, map: Map):
        '''
        Initializes the engine that handles game's logic
        '''

        self.entities = entities
        self.agent = agent
        self.map = map
    
    # Handles the keys passed by the player/AI
    def handle_events(self, key: str) -> bool:
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')

        if move:
            dx, dy = move
            if not self.map.is_blocked(self.agent.x+dx, self.agent.y+dy):
                self.agent.move(dx, dy)
            return False
        
        if exit:
            return True

    def render(self, terminal_width: int, terminal_height: int) -> None:
        render_all(self.entities, self.map, terminal_width, terminal_height)