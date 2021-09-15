from __future__ import annotations

from actions.action import Action

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entities.entity import Entity

class SwitchModeAction(Action):
    def perform(self, engine: Engine, entity: Entity):
        if engine.GAME_MODE_ON is True:
            engine.GAME_MODE_ON = False
        else:
            engine.GAME_MODE_ON = True