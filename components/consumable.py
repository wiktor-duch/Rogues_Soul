from __future__ import annotations

from typing import TYPE_CHECKING

from actions import ItemAction
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entities import Item

class Consumable(BaseComponent):
    parent: Item

    def activate(self, action: ItemAction) -> None:
        '''
        Invoke this items ability.

        The 'action' is the context for this activation.
        '''
        raise NotImplementedError() 
