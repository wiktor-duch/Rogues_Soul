from __future__ import annotations

from actions.action import Action

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entities.entity import Entity

class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity):
        engine.game_over = True