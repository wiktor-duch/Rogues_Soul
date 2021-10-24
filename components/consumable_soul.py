from actions import ItemAction
from components.consumable import Consumable
from exceptions import ImpossibleAction

class ConsumableSoul(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: ItemAction) -> None:
        consumer = action.entity
        
        if action.entity.name != 'Agent':
            raise ImpossibleAction(f'{action.entity.name} cannot pick up {self.parent.name}!')
        
        # Remove item from map
        self.engine.map.entities.remove(self.parent)
        
        # Move the entity
        dx = self.parent.x - consumer.x
        dy = self.parent.y - consumer.y
        consumer.move(dx, dy)

        # Add souls
        consumer.souls += self.amount
        self.engine.message_log.add_message(
            f'Agent consumes {self.amount} souls.'
        )
