from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from game.actions import (
    Action,
    BumpAction,
    EscapeAction, 
    PrintEquipmentAction,
    SwitchModeAction
)
from game.vizualization import discover_tiles
import game.exceptions as exceptions

MOVE_KEYS ={
    # Alphabetic keys
    'a': (-1, 0),
    'w': (0, -1),
    's': (0, 1),
    'd': (1, 0),

    # Numpad keys
    '4': (-1, 0),
    '2': (0, -1),
    '8': (0, 1),
    '6': (1, 0),
}

QUIT_KEYS = {
    'q',
    'Q',
}

MODE_KEYS = {
    'm',
    'M',
}

PRINT_KEY = {
    'p',
    'P'
}

if TYPE_CHECKING:
    from engine import Engine
    
class EventHandler:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def handle_player_events(self) -> bool:
        '''
        Handles the keys passed by the player.

        Returns True if the action will advance a turn.
        '''

        # Input only from player. To be changed later
        key = input('\nEnter your choice: ')

        action: Optional[Action] = self.handle_keys(key)

        if action is None:
            return False
        
        try:
            action.perform()
        except exceptions.ImpossibleAction as exc:
            self.engine.message_log.add_message(exc.args[0])
            self.engine.stats.invalid_actions += 1
            return False  # Skip enemy turn on exceptions.
        
        self.engine.handle_enemy_turns()
        
        room_updated, corr_updated =  discover_tiles(self.engine.map, self.engine.agent) # Discovers tiles ahead of the agent
        # Update statistics
        if room_updated:
            self.engine.stats.fov_updates += 1
            self.engine.stats.rooms_visted += 1
            if self.engine.num_levels == 1:
                self.engine.stats.rooms_visited_lvl_1 += 1
            elif self.engine.num_levels == 2:
                self.engine.stats.rooms_visited_lvl_2 += 1
            elif self.engine.num_levels == 3:
                self.engine.stats.rooms_visited_lvl_3 += 1
        elif corr_updated:
            self.engine.stats.fov_updates += 1
        
        return True


    def handle_keys(self, key: str) -> Optional[Action]:
        action: Optional[Action] = None # Returns None if no valid key was pressed

        agent = self.engine.agent

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(agent, dx, dy)
            self.engine.stats.valid_actions += 1

        # Additional actions used only while playing the game 
        elif key in QUIT_KEYS: # EXIT
            action = EscapeAction(agent)

        elif key in MODE_KEYS: # CHANGE MODE
            action = SwitchModeAction(agent)
        
        elif key in PRINT_KEY: # PRINT EQUIPMENT
            action = PrintEquipmentAction(agent)

        return action