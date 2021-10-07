from __future__ import annotations
from entities import entity

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entities import Entity

class BaseComponent:
    entity: Entity # Has entity instance

    @ property
    def engine(self) -> Engine:
        return self.entity.map.engine