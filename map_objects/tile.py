from enum import Enum

class TILE_TYPE(Enum):
    '''
    Contains all the possible types of tiles.
    '''
    
    BACKGROUND = 0
    FLOOR = 1
    V_WALL = 2
    H_WALL = 3
    CORRIDOR = 4
    ENTRANCE = 5

class Tile:
    def __init__(self):
        '''
        A tile on a map. Can block movement and sight if not discovered.
        '''
        
        self.blocked = True
        self.discovered = False

        self.type = TILE_TYPE.BACKGROUND