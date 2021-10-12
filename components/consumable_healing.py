from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from actions import Action, ItemAction
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entities import Actor, Item

class ConsumableHealing(BaseComponent):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        self.engine.message_log.add_message(
            f'Agent consumes {self.parent.name} and recover {amount_recovered} HP.'
        )