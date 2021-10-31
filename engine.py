from __future__ import annotations

from handlers import EventHandler
from messages import MessageLog
from vizualization import render_map, render_break_line, render_bottom_bar
from typing import TYPE_CHECKING
import exceptions

if TYPE_CHECKING:
    from entities import Actor
    from map_objects import Map, World
class Engine:
    map: Map
    world: World

    def __init__(self, agent: Actor, num_levels: int, game_mode_on: bool):
        '''
        Initializes the engine that handles game's logic
        '''

        self.num_levels = num_levels
        self.game_completed: bool = False
        self.agent = agent
        self.message_log = MessageLog()
        self.event_handler: EventHandler = EventHandler(self)
        self.game_mode_on = game_mode_on
        self.game_over = False
    
    @property
    def level(self):
        return self.world.current_level

    def handle_enemy_turns(self) -> None:
        for actor in set(self.map.actors) - {self.agent}:
            if actor.ai:
                try:
                    actor.ai.perform()
                except exceptions.ImpossibleAction:
                    pass # Ignore impossible action exceptions from entity AI.
    
    def render(self) -> None:
        print('Rogue\'s Soul')

        render_break_line(self.map.width)
        print('') # Prevents the messages from rendering after the break line

        if self.message_log.messages: # If there are messages to print
            self.message_log.render()
            self.message_log.clear()
        else:
            print('\n')

        render_map(self.map, self.game_mode_on)

        render_bottom_bar(
            curr_level=self.level,
            num_levels=self.num_levels,
            agent_hp=self.agent.fighter.hp,
            max_hp=self.agent.fighter.max_hp,
            souls=self.agent.souls
        )

        render_break_line(self.map.width)