from typing import Tuple as tuple

class Rectangle:
    def __init__(self, x_coord: int, y_coord: int, width: int, height: int):
        '''
        Helper class that makes room generation easier
        '''

        self.x1 = x_coord
        self.y1 = y_coord
        self.x2 = x_coord + width
        self.y2 = y_coord + height
    
    def center(self) -> tuple[int]:
        '''
        Returns the center coordinates of a rectangle
        '''

        center_x = int((self.x1 + self.x2)/2)
        center_y = int((self.y1 + self.y2)/2)

        return (center_x, center_y)

    def intersect_room(self, other) -> bool:
        '''
        Returns true if a room intersects another room.
        '''
        
        # +/- 1 allows to leave a 1 tile break background break between the rooms
        return (self.x1-1 <= other.x2 and self.x2+1 >= other.x1 and
            self.y1-1 <= other.y2 and self.y2+1 >= other.y1)
    
    def intersect_tile_at(self, x, y) -> bool:
        '''
        Returns true if a tile intersects a room.
        '''

        return (self.x1 <= x and self.x2 >= x and
            self.y1 <= y and self.y2 >= y)