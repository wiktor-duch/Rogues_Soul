from __future__ import annotations

from typing import TYPE_CHECKING
from game.actions.action import Action

if TYPE_CHECKING:
    from entities import Actor, Item

class ItemAction(Action):
    def __init__(
        self,
        entity: Actor,
        item: Item,
    ):
        super().__init__(entity)
        self.item = item

    def perform(self) -> None:
        '''
        Invoke this item ability.
        '''

        self.item.consumable.activate(self)