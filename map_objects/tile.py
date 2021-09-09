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
    def __init__(self, blocked: bool, block_sight: bool = None):
        """
        A tile on a map. Can block movement and sight.
        """
        
        self.blocked = blocked
        
        # By default, if a tile is blocked/undiscovered, it also blocks the sight
        if block_sight is None:
            block_sight = blocked
        
        self.block_sight = block_sight

        self.type = TILE_TYPE.BACKGROUND