'''
Based on:
http://rogueliketutorials.com/tutorials/tcod/v2/
'''
from enum import auto, Enum

class RenderOrder(Enum):
    '''
    Sets rendering order.
    '''
    ACTOR = auto()
    ITEM = auto()
    CORPSE = auto()