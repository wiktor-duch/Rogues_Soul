from __future__ import annotations

from actions.action import Action

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine

class EscapeAction(Action):
    def perform(self):
        self.engine.game_over = True