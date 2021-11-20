from __future__ import annotations

from typing import List, TYPE_CHECKING

from game.components.base_component import BaseComponent

if TYPE_CHECKING:
    from game.entities import Actor, Item


class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []

    def equip(self, item: Item) -> None:
        '''
        Allows to add an item to the player's inventory.

        A message also apears on a screen.
        '''
        self.items.append(item)
        self.engine.message_log.add_message(f'You have found {item.name}!')