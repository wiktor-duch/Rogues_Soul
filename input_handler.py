from typing import Tuple as tuple, Dict as dict

def handle_keys(key: str) -> (dict[str, tuple[int, int]] or dict[str, bool]):
    if key == '1': # LEFT
        return {'move': (-1,0)}
    elif key == '2': # UP
        return {'move': (0,-1)}
    elif key == '3': # RIGHT
        return {'move': (1,0)}
    elif key == '4': #DOWN
        return {'move': (0,1)}
    
    elif key == 'q' or key == 'Q': # EXIT
        return {'exit': True}

    else:
        return {}