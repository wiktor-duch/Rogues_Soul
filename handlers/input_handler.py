from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from actions import Action, BumpAction, EscapeAction, SwitchModeAction
from vizualization import discover_tiles

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
        key = input('Enter your choice: ')

        action: Optional[Action] = self.handle_keys(key)

        self.engine.handle_enemy_turns()
        action.perform()
        discover_tiles(self.engine.map, self.engine.agent) # Discovers tiles ahead of the agent

    def handle_keys(self, key: str) -> Optional[Action]:
        action: Optional[Action] = None #Returns None if no valid key was pressed

        agent = self.engine.agent

        if key == '1': # LEFT
            action = BumpAction(agent, -1, 0)

        elif key == '2': # UP
            action = BumpAction(agent, 0, -1)
        
        elif key == '3': # RIGHT
            action = BumpAction(agent, 1, 0)
        
        elif key == '4': #DOWN
            action = BumpAction(agent, 0, 1)

        # Additional actions used only while playing the game 
        elif key == 'q' or key == 'Q': # EXIT
            action = EscapeAction(agent)

        elif key == 'm' or key == 'M': # CHANGE MODE
            action = SwitchModeAction(agent)

        return action