from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from actions import Action, BumpAction, EscapeAction, SwitchModeAction
from vizualization import discover_tiles

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

if TYPE_CHECKING:
    from engine import Engine
    
class EventHandler:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def handle_events(self) -> None:
        '''
        Handles the keys passed by the player/AI
        '''

        # Input only from player. To be changed later
        key = input('\nEnter your choice: ')

        action: Optional[Action] = self.handle_keys(key)
        
        if action: # Checks if input was valid
            action.perform()
        
        self.engine.handle_enemy_turns()
        discover_tiles(self.engine.map, self.engine.agent) # Discovers tiles ahead of the agent

    def handle_keys(self, key: str) -> Optional[Action]:
        action: Optional[Action] = None # Returns None if no valid key was pressed

        agent = self.engine.agent

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(agent, dx, dy)

        # Additional actions used only while playing the game 
        elif key in QUIT_KEYS: # EXIT
            action = EscapeAction(agent)

        elif key in MODE_KEYS: # CHANGE MODE
            action = SwitchModeAction(agent)

        return action