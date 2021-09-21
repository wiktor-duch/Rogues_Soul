from __future__ import annotations
from entities.entity import Entity

from typing import Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from components.entity_ai import BaseAI
    from components.fighter import Fighter

class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = 'U',
        name: str = '<Unnamed>',
        ai_cls: Type[BaseAI],
        fighter: Fighter
    ):
        super().__init__(x=x, y=y, char=char, name=name, blocks_movement=True)

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.fighter = fighter
        self.fighter.entity = self

    def is_alive(self) -> bool:
        '''
        Returns true as long as this entity can perform actions.
        '''
        return bool(self.ai)