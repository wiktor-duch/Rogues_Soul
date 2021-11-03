from __future__ import annotations

from typing import TYPE_CHECKING

from entities import Entity
from vizualization.render_order import RenderOrder

if TYPE_CHECKING:
    from components.equippable_components import Equippable

class Equipment(Entity):
    def __init__(
        self,
        *,
        x :int = 0,
        y: int = 0,
        char: str = 'U',
        name: str = '<Unnamed>',
        equippable: Equippable
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM
        )

        self.equippable = equippable
        self.equippable.parent = self
        self.active = True