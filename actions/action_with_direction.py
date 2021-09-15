from __future__ import annotations

from actions.action import Action

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entities.entity import Entity

class ActionWithDirection(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        '''
        This method must be overridden by ActionWithDirection subclasses.
        '''

        raise NotImplementedError()