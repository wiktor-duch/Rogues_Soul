from __future__ import annotations

from vizualization.render_order import RenderOrder
from components.base_component import BaseComponent

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities import Actor

class Fighter(BaseComponent):
    entity: Actor

    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp # Entity’s hit points
        self._hp = hp
        self.defense = defense # Damage taken reduction/ chance of not being hit
        self.power = power # Entity's raw attack power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        # Makes sure hp is not below 0 and above max_hp
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.entity.ai:
            self.die()

    def die(self) -> None:
        '''
        This method does the followig:
            - prints out a message, indicating that entity is dead
            - sets the entity's character to '%' - corpse
            - sets blocks_movement to False
            - removes the AI component
            - sets the entity's name to 'Remains of {entity name}'
        '''
        if self.engine.agent is self.entity:
            self.engine.message_log.add_message(
                'You died!'
            )

            '''
            The following two lines renders the screen before agents death.
            They should be uncommented for development process only.
            '''
            print('') # A simple line break in the console output
            self.engine.render()

            self.engine.game_over = True
        else:
            self.engine.message_log.add_message(
                f'{self.entity.name} is dead!'
            )

        # Checks if there is no entity already at this position
        x, y = self.entity.x, self.entity.y
        # TODO: function looking for two entities on one tile
        if self.entity.map.check_for_duplicates(x, y):
            if (not self.entity.map.is_entity_at(x-1, y)
                and not self.entity.map.is_blocked(x-1, y)):
                self.entity.x -= 1
            elif (not self.entity.map.is_entity_at(x, y-1)
                and not self.entity.map.is_blocked(x, y-1)):
                self.entity.y -= 1
            elif (not self.entity.map.is_entity_at(x+1, y)
                and not self.entity.map.is_blocked(x+1, y)):
                self.entity.x += 1
            elif (not self.entity.map.is_entity_at(x, y+1)
                and not self.entity.map.is_blocked(x, y+1)):
                self.entity.y += 1
            else:
                self.entity.x = -1
                self.entity.y = -1
            # NOTE: Extend if necessary

        self.entity.char = '%'
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f'Remains of {self.entity.name}'
        self.entity.render_order = RenderOrder.CORPSE