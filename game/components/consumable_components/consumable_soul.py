from game.actions import ItemAction
from game.components.consumable_components.consumable import Consumable
from game.exceptions import ImpossibleAction

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

        # Update statistics
        if action.item.name == 'Soul':
            self.engine.stats.souls_collected += 1
            if self.engine.level == 1:
                self.engine.stats.souls_collected_lvl_1 += 1
            elif self.engine.level == 2:
                self.engine.stats.souls_collected_lvl_2 += 1
            elif self.engine.level == 3:
                self.engine.stats.souls_collected_lvl_3 += 1
