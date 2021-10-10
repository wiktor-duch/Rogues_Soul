from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entities import Entity
    from map_objects import Map

class BaseComponent:
    parent: Entity # Has entity instance

    @property
    def map(self) -> Map:
        return self.parent.map

    @ property
    def engine(self) -> Engine:
        return self.map.engine