from actions.switch_mode_action import SwitchModeAction
from typing import Optional

from actions.action import Action
from actions.bump_action import BumpAction
from actions.escape_action import EscapeAction

def handle_keys(key: str) -> Optional[Action]:
    action: Optional[Action] = None #Returns None if no valid key was pressed

    if key == '1': # LEFT
        action = BumpAction(-1, 0)

    elif key == '2': # UP
        action = BumpAction(0, -1)
    
    elif key == '3': # RIGHT
        action = BumpAction(1, 0)
    
    elif key == '4': #DOWN
        action = BumpAction(0, 1)

    # Additional actions used only while playing the game 
    elif key == 'q' or key == 'Q': # EXIT
        action = EscapeAction()

    elif key == 'm' or key == 'M': # CHANGE MODE
        action = SwitchModeAction()

    return action