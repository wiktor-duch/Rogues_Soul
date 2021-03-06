'''
Based on:
http://rogueliketutorials.com/tutorials/tcod/v2/
'''
from game.actions import ItemAction
from game.components.consumable_components.consumable import Consumable

class ConsumableHealing(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        # Remove the item
        self.engine.map.entities.remove(self.parent)

        # Move the entity
        dx = self.parent.x - consumer.x
        dy = self.parent.y - consumer.y
        consumer.move(dx, dy)

        self.engine.message_log.add_message(
            f'Agent consumes {self.parent.name} and recover {amount_recovered} HP.'
        )

        # Update statistics
        if action.item.name == 'Health Potion':
            self.engine.stats.potions_used += 1