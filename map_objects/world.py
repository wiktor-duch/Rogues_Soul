from __future__ import annotations

from exceptions import InvalidMap

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine

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
        min_rooms: int,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        min_enemies_per_room: int,
        max_enemies_per_room: int,
        min_health_potions_per_room: int,
        max_health_potions_per_room: int,
        min_souls_per_room: int,
        max_souls_per_room: int,
        min_chests_per_room: int,
        max_chests_per_room: int,
        current_level: int = 0
    ) -> None:
        # Engine configuration 
        self.engine = engine

        # Map configuration
        self.width = map_width
        self.height = map_height

        # Room configuration
        self.min_rooms = min_rooms
        self.max_rooms = max_rooms
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size

        # Enemy configuration
        self.min_enemies_per_room = min_enemies_per_room
        self.max_enemies_per_room = max_enemies_per_room

        # Item configuration
        self.min_health_potions_per_room = min_health_potions_per_room
        self.max_health_potions_per_room = max_health_potions_per_room
        self.min_souls_per_room = min_souls_per_room
        self.max_souls_per_room = max_souls_per_room
        self.min_chests_per_room = min_chests_per_room
        self.max_chests_per_room = max_chests_per_room

        # Set current level
        self.current_level = current_level

    def generate_level(self) -> None:
        from map_objects import generate_dungeon

        self.current_level += 1

        try:
            self.engine.map = generate_dungeon(
                min_rooms = self.min_rooms,
                max_rooms = self.max_rooms,
                room_min_size = self.room_min_size,
                room_max_size = self.room_max_size,
                min_enemies_per_room = self.min_enemies_per_room,
                max_enemies_per_room = self.max_enemies_per_room,
                min_health_potions_per_room = self.min_health_potions_per_room,
                max_health_potions_per_room = self.max_health_potions_per_room,
                min_souls_per_room = self.min_souls_per_room,
                max_souls_per_room = self.max_souls_per_room,
                min_chests_per_room = self.min_chests_per_room,
                max_chests_per_room = self.min_chests_per_room,
                map_width = self.width,
                map_height = self.height,
                engine = self.engine
            )
        except InvalidMap as exc:
            raise exc