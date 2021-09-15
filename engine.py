from entities.entity import Entity
from vizualization.render_functions import render_map
from handlers.input_handler import handle_keys
from vizualization.fov_functions import discover_tiles
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
        self.game_over = False
    
    def handle_enemy_turns(self) -> None:
        for entity in self.map.entities - {self.agent}:
            pass
    
    # Handles the keys passed by the player/AI
    def handle_events(self, key: str) -> None:
        action = handle_keys(key)

        action.perform(self, self.agent)

    def render(self) -> None:
        print('Rogue\'s Soul')
        render_map(self.map, self.GAME_MODE_ON)
        # TODO: print interface with stats