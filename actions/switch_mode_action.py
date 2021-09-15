from __future__ import annotations

from actions.action import Action

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entities.entity import Entity

class SwitchModeAction(Action):
    def perform(self):
        if self.engine.game_mode_on is True:
            self.engine.game_mode_on = False
        else:
            self.engine.game_mode_on = True