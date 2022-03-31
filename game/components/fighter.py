'''
Based on:
http://rogueliketutorials.com/tutorials/tcod/v2/
'''
from __future__ import annotations
from game.map_objects.tile import TILE_TYPE

from game.vizualization.render_order import RenderOrder
from game.components.base_component import BaseComponent

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.entities import Actor

class Fighter(BaseComponent):
    parent: Actor

    def __init__(
        self,
        base_hp: int,
        base_defense: int,
        base_power: int
    ):
        self.base_max_hp = base_hp # Entity’s max hit points
        self._hp = base_hp
        self.base_defense = base_defense # Damage taken reduction/ chance of not being hit
        self.base_power = base_power # Entity's raw attack power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        # Makes sure hp is not below 0 and above max_hp
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()
    
    @property
    def max_hp(self) -> int:
        return self.base_max_hp + self.bonus_hp

    @property
    def defense(self) -> int:
        return self.base_defense + self.bonus_defense

    @property
    def power(self) -> int:
        return self.base_power + self.bonus_power

    @property
    def bonus_hp(self) -> int:
        if self.parent.actor_equipment:
            return self.parent.actor_equipment.health_bonus
        else:
            return 0

    @property
    def bonus_defense(self) -> int:
        if self.parent.actor_equipment:
            return self.parent.actor_equipment.defense_bonus
        else:
            return 0

    @property
    def bonus_power(self) -> int:
        if self.parent.actor_equipment:
            return self.parent.actor_equipment.power_bonus
        else:
            return 0

    def heal(self, amount: int) -> int:
        '''
        Increases the parent hp by the given amount.
        Returns the difference in hp.
        '''
        if self.hp == self.max_hp:
            return 0
        
        new_hp = self.hp + amount

        if new_hp > self.max_hp:
            new_hp = self.max_hp
        
        amount_recovered = new_hp - self.hp
        self.hp = new_hp
        
        # Update statistics
        self.engine.stats.hp_gained += amount_recovered

        return amount_recovered
    
    def take_damage(self, amount: int) -> None:
        self.hp -= amount

    def die(self) -> None:
        '''
        This method does the followig:
            - prints out a message, indicating that entity is dead
            - sets the entity's character to '%' - corpse
            - sets blocks_movement to False
            - removes the AI component
            - sets the entity's name to 'Remains of {entity name}'
        '''
        if self.engine.agent is self.parent:
            self.engine.message_log.add_message(
                'You died!'
            )

            '''
            The following two lines renders the screen before agents death.
            They should be uncommented for development process only.
            '''
            # print('') # A simple line break in the console output
            # self.engine.render()

            self.engine.game_over = True
        else:
            self.engine.message_log.add_message(
                f'{self.parent.name} is dead!'
            )
            # Update statistics
            self.engine.stats.enemies_killed += 1
            if self.engine.level == 1:
                self.engine.stats.enemies_killed_lvl_1 += 1
            elif self.engine.level == 2:
                self.engine.stats.enemies_killed_lvl_2 += 1
            elif self.engine.level == 3:
                self.engine.stats.enemies_killed_lvl_3 += 1

        # Checks if there is no entity already at this position
        x, y = self.parent.x, self.parent.y
        # TODO: function looking for two entities on one tile
        if (self.parent.map.check_for_duplicates(x, y)
            or self.parent.map.tiles[y][x].type == TILE_TYPE.EXIT):
            if (not self.parent.map.is_entity_at(x-1, y)
                and not self.parent.map.is_blocked(x-1, y)
                and self.parent.map.tiles[y][x-1].type != TILE_TYPE.EXIT):
                self.parent.x -= 1
            elif (not self.parent.map.is_entity_at(x, y-1)
                and not self.parent.map.is_blocked(x, y-1)
                and self.parent.map.tiles[y-1][x].type != TILE_TYPE.EXIT):
                self.parent.y -= 1
            elif (not self.parent.map.is_entity_at(x+1, y)
                and not self.parent.map.is_blocked(x+1, y)
                and self.parent.map.tiles[y][x+1].type != TILE_TYPE.EXIT):
                self.parent.x += 1
            elif (not self.parent.map.is_entity_at(x, y+1)
                and not self.parent.map.is_blocked(x, y+1)
                and self.parent.map.tiles[y+1][x].type != TILE_TYPE.EXIT):
                self.parent.y += 1
            else:
                self.parent.x = -1
                self.parent.y = -1
            # NOTE: Extend if necessary

        self.parent.char = '%'
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f'Remains of {self.parent.name}'
        self.parent.render_order = RenderOrder.CORPSE