from typing import Tuple

class Rectangle:
    def __init__(self, x_coord: int, y_coord: int, width: int, height: int):
        '''
        Helper class that makes room generation easier
        '''

        self.x1 = x_coord
        self.y1 = y_coord
        self.x2 = x_coord + width
        self.y2 = y_coord + height
    
    @property
    def center(self) -> Tuple[int]:
        '''
        Returns the center coordinates of a rectangle
        '''

        center_x = int((self.x1 + self.x2)/2)
        center_y = int((self.y1 + self.y2)/2)

        return (center_x, center_y)

    def intersects_room(self, other) -> bool:
        '''
        Returns true if a room intersects another room.
        '''
        
        # +/- 1 allows to leave a 1 tile break background break between the rooms
        return (self.x1-1 <= other.x2 and self.x2+1 >= other.x1 and
            self.y1-1 <= other.y2 and self.y2+1 >= other.y1)
    
    def intersects_tile_at(self, x_coord, y_coord) -> bool:
        '''
        Returns true if a tile intersects a room.
        '''

        return (self.x1 <= x_coord and self.x2 >= x_coord and
            self.y1 <= y_coord and self.y2 >= y_coord)