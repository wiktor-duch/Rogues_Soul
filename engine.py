from entity import Entity
from vizualization.render_functions import render_all
from input_handler import handle_keys
from fov_functions import discover_tiles
from map_objects.map import Map
from typing import List

class Engine:
    def __init__(self, agent: Entity, map: Map, GAME_MODE_ON: bool):
        '''
        Initializes the engine that handles game's logic
        '''

        self.agent = agent
        self.map = map
        self.GAME_MODE_ON = GAME_MODE_ON
    
    # Handles the keys passed by the player/AI
    def handle_events(self, key: str) -> bool:
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        mode = action.get('mode')

        if move:
            dx, dy = move
            if not self.map.is_blocked(self.agent.x+dx, self.agent.y+dy):
                self.agent.move(dx, dy)
                discover_tiles(self.map, self.agent) # Discovers tiles ahead of the agent 
            return False
        
        if exit:
            return True
        
        if mode:
            if self.GAME_MODE_ON is True:
                self.GAME_MODE_ON = False
            else:
                self.GAME_MODE_ON = True

    def render(self) -> None:
        render_all(self.map, self.GAME_MODE_ON)