from __future__ import annotations

from typing import TYPE_CHECKING

from game.actions import ItemAction
from game.components.base_component import BaseComponent

if TYPE_CHECKING:
    from game.entities import Item

class Consumable(BaseComponent):
    parent: Item

    def activate(self, action: ItemAction) -> None:
        '''
        Invoke this items ability.

        The 'action' is the context for this activation.
        '''
        raise NotImplementedError() 
