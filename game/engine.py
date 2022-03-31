from __future__ import annotations
from re import S
from game.statistics import Statistics

from game.handlers import EventHandler
from game.messages import MessageLog
from game.vizualization import render_map, render_break_line, render_bottom_bar
import game.exceptions as exceptions

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from game.entities import Actor
    from game.map_objects import Map, World

class Engine:
    map: Map
    world: World

    def __init__(
        self,
        agent: Actor,
        num_levels: int,
        game_mode: int = 0,
        seed: Optional[int] = None
    ):
        '''
        Initializes the engine that handles game's logic
        '''

        self.num_levels = num_levels
        self.game_completed: bool = False
        self.agent = agent
        self.message_log = MessageLog()
        self.event_handler: EventHandler = EventHandler(self)
        self.game_mode = game_mode # Mode is reseponsible for different game settings
        self.game_over = False
        self.seed = seed
        self.stats = Statistics(max_lvl=num_levels)
    
    @property
    def level(self):
        return self.world.current_level

    def set_seed(self, seed: int) -> None:
        self.seed = seed
    
    def get_seed(self) -> Optional[int]:
        return self.seed

    def delete_seed(self) -> None:
        '''
        Sets seed's value to None
        '''
        self.seed = None

    def set_game_mode(self, mode: int) -> None:
        '''
        Sets the mode of the game.
            - 0: Game mode
            - 1: Developer mode (map is discovered)
        if mode is not 0 or 1, nothing is set.
        '''
        if mode in range(2):
            self.game_mode = mode
    
    def get_game_mode(self) -> int:
        return self.game_mode

    def handle_enemy_turns(self) -> None:
        for actor in set(self.map.actors) - {self.agent}:
            if actor.ai:
                try:
                    actor.ai.perform()
                except exceptions.ImpossibleAction:
                    pass # Ignore impossible action exceptions from entity AI.
    
    def render(self, print_title: bool = False) -> None:
        if print_title:
            print('Rogue\'s Soul')

        render_break_line(self.map.width)
        print('') # Prevents the messages from rendering after the break line

        if self.message_log.messages: # If there are messages to print
            self.message_log.render()
            self.message_log.clear()
        else:
            print('\n')
        
        if self.game_mode == 0:
            game_mode_on = True
        elif self.game_mode == 1:
            game_mode_on = False
        
        render_map(self.map, game_mode_on)

        render_bottom_bar(
            curr_level=self.level,
            num_levels=self.num_levels,
            agent=self.agent
        )

        render_break_line(self.map.width)
        print()