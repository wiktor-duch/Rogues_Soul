from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from actions import Action, ItemAction
from components.base_component import BaseComponent
from entities import item

if TYPE_CHECKING:
    from entities import Actor, Item

class Consumable(BaseComponent):
    parent: Item

    def activate(self, action: ItemAction) -> None:
        '''
        Invoke this items ability.

        The 'action' is the context for this activation.
        '''
        raise NotImplementedError() 
