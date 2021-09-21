from __future__ import annotations

from handlers import EventHandler
from vizualization import render_map
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities import Actor
    from map_objects import Map
class Engine:
    map: Map

    def __init__(self, agent: Actor, game_mode_on: bool):
        '''
        Initializes the engine that handles game's logic
        '''

        self.agent = agent
        self.event_handler: EventHandler = EventHandler(self)
        self.game_mode_on = game_mode_on
        self.game_over = False
    
    def handle_enemy_turns(self) -> None:
        for actor in set(self.map.actors) - {self.agent}:
            if actor.ai:
                actor.ai.perform()
    
    def render(self) -> None:
        print('Rogue\'s Soul')
        render_map(self.map, self.game_mode_on)
        # TODO: print interface with stats