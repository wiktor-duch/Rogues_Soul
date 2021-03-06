'''
Based on:
http://rogueliketutorials.com/tutorials/tcod/v2/
'''
from __future__ import annotations

from game.actions import Action

from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from game.entities import Actor

class BaseAI(Action):
    entity: Actor

    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int, additinal_check:bool = False) -> List[Tuple[int]]:
        '''
        Computes and returns the path as xy-coordinates to the target position.
        
        Target can be an agent, souls or items.
        
        Returns an empty list if there is no valid path.
        '''

        # We alredy check this is hostile enemy class so there is no need to do it again 
        if additinal_check:
            room = None
            for r in self.entity.map.rooms:
                if r.intersects_tile_at(dest_x, dest_y):
                    # NOTE: Standing at the entrance does not trigger the enemy
                    break
            
            if room is None:
                return [] # Returns empty list as there is no valid path

        path: List[Tuple[int]] = []

        # Gets current coordinates
        curr_x = self.entity.x
        curr_y = self.entity.y

        # Gets both distances
        dist_x = abs(dest_x - curr_x)
        dist_y = abs(dest_y - curr_y)
        
        # Checks if the enemy is already next to the player
        if (dist_x == 0 and dist_y == 1) or (dist_x == 1 and dist_y == 0):
            return path # Returns empty path as target is next to the entity
        else:
            is_adjacent = False

        while not is_adjacent:
            # Appends a tile in x direction
            if dist_x >= dist_y:
                # Checks the direction
                if (dest_x - curr_x) < 0: # Target is on the left
                    curr_x -= 1
                    path.append((curr_x, curr_y))
                else: # Target is on the right
                    curr_x += 1
                    path.append((curr_x, curr_y))

                # Recalculates the distance
                dist_x = abs(dest_x - curr_x)
                
            # Appends a tile in y direction
            else: # dist_x < dist_y
                # Checks the direction
                if (dest_y - curr_y) < 0: # Target is on the left
                    curr_y -= 1
                    path.append((curr_x, curr_y))
                else: # Target is on the right
                    curr_y += 1
                    path.append((curr_x, curr_y))
                
                # Recalculates the distance
                dist_y = abs(dest_y - curr_y)

            # Checks if the last tile in the path is adjacent to the destination tile
            if (dist_x == 0 and dist_y == 1) or (dist_x == 1 and dist_y == 0):
                is_adjacent = True
        
        return path

    def get_next_move(self, dest_x: int, dest_y: int) -> Tuple[int]:
        '''
        Returns the next dx and dy values that can be passed to MovementAction.
        '''

        next_move: Tuple[int] = (0, 0)

        # Gets current coordinates
        curr_x = self.entity.x
        curr_y = self.entity.y

        # Gets both distances
        dx = dest_x - curr_x
        dy = dest_y - curr_y
        
        # (Additionally) Checks if the enemy is already next to the player
        if (abs(dx) == 0 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 0):
            return next_move # Returns (0,0) as target is next to the entity
        
        if abs(dx) > abs(dy): # Try moving horizontally
            if (dx >= 0 # Go right
            and not self.engine.map.is_actor_at(curr_x+1, curr_y)
            and not self.engine.map.is_blocked(curr_x+1, curr_y)):
                next_move = (1, 0)

            elif (dx < 0 # Go left
            and not self.engine.map.is_actor_at(curr_x-1, curr_y)
            and not self.engine.map.is_blocked(curr_x-1, curr_y)):
                next_move = (-1, 0)

            else: # Avoid the other actor
                if dy > 0: # Target is below
                    next_move = (0, 1)
                elif dy < 0: # Target is above
                    next_move = (0, -1)
                else: # Target is at the same level
                    if self.engine.map.is_blocked(curr_x, curr_y+1):
                        next_move = (0,-1)
                    else:
                        next_move = (0, 1)
        
        else: # Try moving vertically
            if (dy >= 0 # Go down
            and not self.engine.map.is_actor_at(curr_x, curr_y+1)
            and not self.engine.map.is_blocked(curr_x, curr_y+1)):
                next_move = (0, 1)

            elif (dy < 0 # Go up
            and not self.engine.map.is_actor_at(curr_x, curr_y-1)
            and not self.engine.map.is_blocked(curr_x, curr_y-1)):
                next_move = (0, -1)

            else: # Avoid the other actor
                if dx > 0: # Target is on the right
                    next_move = (1, 0)
                elif dx < 0: # Target is on the left
                    next_move = (-1, 0)
                else: # Target is at the same level
                    if self.engine.map.is_blocked(curr_x+1, curr_y):
                        next_move = (-1,0)
                    else:
                        next_move = (1, 0)

        return next_move