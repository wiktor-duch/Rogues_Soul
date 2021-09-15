from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entities.entity import Entity

class Action:
    def __init__(self, entity: Entity) -> None:
        self.entity = entity
    
    @property
    def engine(self) -> Engine:
        '''
        Return the engine this action belongs to.
        '''
        
        return self.entity.map.engine

    def perform(self) -> None:
        '''
        Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        '''

        raise NotImplementedError()