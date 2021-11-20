from __future__ import annotations

from game.entities import Entity
from game.vizualization.render_order import RenderOrder

from typing import Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from components import (
        ActorsEquipment,
        BaseAI,
        Fighter,
        Inventory
    )

class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = 'U',
        name: str = '<Unnamed>',
        ai_cls: Type[BaseAI],
        actor_equipment: ActorsEquipment,
        fighter: Fighter,
        inventory: Inventory
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR
        )

        # Sets the AI component
        self.ai: Optional[BaseAI] = ai_cls(self)

        # Sets the Equipment
        self.actor_equipment: ActorsEquipment = actor_equipment
        self.actor_equipment.parent = self

        # Sets the Fighter component
        self.fighter: Fighter = fighter
        self.fighter.parent = self

        # Sets the Inventory
        self.inventory: Inventory = inventory
        self.inventory.parent = self

        # Sets souls
        self.souls = 0

    def is_alive(self) -> bool:
        '''
        Returns true as long as this entity can perform actions.
        '''

        if self.fighter.hp > 0:
            return True
        
        return False