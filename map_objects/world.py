from __future__ import annotations

from exceptions import InvalidMap

from typing import TYPE_CHECKING, Dict, List, Tuple

if TYPE_CHECKING:
    from engine import Engine
    from entities import Entity

class World:
    '''
    Holds the settings for Map objects and allows to generate new levels.
    '''

    def __init__(
        self,
        *,
        engine: Engine,
        map_width: int,
        map_height: int,
        room_min_size: int,
        room_max_size: int,
        num_rooms_per_level: List[Tuple[int, int, int]],
        num_enemies_per_level: List[Tuple[int, int, int]],
        enemy_types_per_level: Dict[int, List[Tuple[Entity, int]]],
        num_health_potions_per_level: List[Tuple[int, int, int]],
        num_souls_per_level: List[Tuple[int, int, int]],
        num_chests_per_level: List[Tuple[int, int, int]], 
        current_level: int = 0
    ) -> None:
        # Engine configuration 
        self.engine = engine

        # Map configuration
        self.width = map_width
        self.height = map_height

        # Room configuration
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.num_rooms_per_level = num_rooms_per_level

        # Enemy configuration
        self.num_enemies_per_level = num_enemies_per_level
        self.enemy_types_per_level = enemy_types_per_level

        # Item configuration
        self.num_health_potions_per_level = num_health_potions_per_level
        self.num_souls_per_level = num_souls_per_level
        self.num_chests_per_level = num_chests_per_level

        # Set current level
        self.current_level = current_level

    def generate_level(self) -> None:
        from map_objects import generate_dungeon

        self.current_level += 1

        try:
            self.engine.map = generate_dungeon(
                room_min_size = self.room_min_size,
                room_max_size = self.room_max_size,
                num_rooms_per_level = self.num_rooms_per_level,
                num_enemies_per_level = self.num_enemies_per_level,
                enemy_types_per_level=self.enemy_types_per_level,
                num_health_potions_per_level = self.num_health_potions_per_level,
                num_souls_per_level = self.num_souls_per_level,
                num_chests_per_level= self.num_chests_per_level,  
                map_width = self.width,
                map_height = self.height, 
                engine=self.engine
            )
        except InvalidMap as exc:
            raise exc