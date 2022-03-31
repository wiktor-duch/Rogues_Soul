from game.actions import ItemAction
from game.components.consumable_components.consumable import Consumable

from random import random

class ConsumableReward(Consumable):
    def __init__(self, pct: float, num_souls: int, amount_hp: int):
        self.percent = 1-pct
        self.hp = amount_hp
        self.souls = num_souls

    def activate(self, action: ItemAction) -> None:
        consumer = action.entity

        # Deactivate item
        self.parent.active = False
        
        random_pct = random() 

        if random_pct < self.percent:
            # This chest give soul
            consumer.souls += self.souls
            self.parent.char='<'
            self.engine.message_log.add_message(
                f'Agent opens {self.parent.name} and gets {self.souls} souls.'
            )
            # Update statistics
            if action.item.name == 'Chest':
                self.engine.stats.opened_rewards += 1
                self.engine.stats.opened_chests += 1
        else:
            # This chest is a trap
            consumer.fighter.take_damage(amount=self.hp)
            self.parent.char='!'
            self.engine.message_log.add_message(
                f'{self.parent.name} was a trap and Agents loses {self.hp} HP.'
            )
             # Update statistics
            if action.item.name == 'Chest':
                self.engine.stats.hp_lost += self.hp
                self.engine.stats.opened_traps += 1
                self.engine.stats.opened_chests += 1
        self.parent.name = 'Opened Chest'
