from enum import auto, Enum

class RenderOrder(Enum):
    '''
    Sets rendering order.
    '''
    ACTOR = auto()
    ITEM = auto()
    CORPSE = auto()