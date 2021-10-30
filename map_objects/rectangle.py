from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from map_objects.rectangle import Rectangle as Rect

class Rectangle:
    def __init__(self, x: int, y: int, width: int, height: int):
        '''
        Helper class that makes room generation easier
        '''

        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height
    
    @property
    def center(self) -> Tuple[int]:
        '''
        Returns the center coordinates of a rectangle
        '''

        center_x = int((self.x1 + self.x2)/2)
        center_y = int((self.y1 + self.y2)/2)

        return (center_x, center_y)

    def intersects_room(self, other: Rect) -> bool:
        '''
        Returns true if a room intersects another room.
        '''
        
        # +/- 1 allows to leave a 1 tile break background break between the rooms
        return (self.x1-1 <= other.x2 and self.x2+1 >= other.x1 and
            self.y1-1 <= other.y2 and self.y2+1 >= other.y1)
    
    def intersects_tile_at(self, x, y) -> bool:
        '''
        Returns true if a tile intersects a room.
        '''

        return (self.x1 <= x and self.x2 >= x 
            and self.y1 <= y and self.y2 >= y)