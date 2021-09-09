from entity import Entity
from map_objects.tile import Tile, TILE_TYPE
from map_objects.rectangle import Rectangle as Rect
from random import randint
from typing import List

class Map:
    def __init__(self, width: int, height: int):
        '''
        Generates a new game map.
        '''

        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self) -> List[List[Tile]]:
        '''
        Initialize the 2D array of Tiles.
        '''
        
        tiles = [[Tile(True) for x in range(self.width)] for y in range(self.height)]
        return tiles
    
    def is_blocked(self, x_coord: int, y_coord: int) -> bool:
        '''
        Returns true if a tile is blocked.
        '''

        if self.tiles[y_coord][x_coord].blocked:
            return True
        
        return False
    
    def create_vert_tunnel(self, y1: int, y2: int, x: int, rooms: list) -> None:
        '''
        Creates a vertical tunnel between y1 and y2 at x.
        Requires list of rooms to set the tiles type.
        '''

        for y in range(min(y1, y2), max(y1,y2)+1):
            intersection = False
            entrance = False
            corner_detected = False
            
            # Checks if a tile intersects a room
            for room in rooms:
                if room.intersect_tile(x, y):
                    intersection = True
                    # Corner detection
                    if ((x == room.x1 and y == room.y1) or (x == room.x1 and y == room.y2) or
                        (x == room.x2 and y == room.y1) or (x == room.x2 and y == room.y2)):
                        
                        corner_detected = True

                        # Check for right corner (from room perspective)
                        if room.intersect_tile(x-1, y):
                            x -= 1
                            # Check if there is no entrance on the left already
                            if not self.tiles[y][x-1].type == TILE_TYPE.ENTRANCE:
                                entrance = True
                            # If NOT a right bottom corner and the first tunnel tile
                            if self.tiles[y-1][x].type == TILE_TYPE.BACKGROUND and y > min(y1, y2):
                                self.tiles[y-1][x].type = TILE_TYPE.CORRIDOR
                                self.tiles[y-1][x].blocked = False
                                self.tiles[y-1][x].block_sight = False
                            
                        # Left corner (from room perspective)
                        else:
                            x += 1
                            # Check if there is no entrance on the right already
                            if not self.tiles[y][x+1].type == TILE_TYPE.ENTRANCE:
                                entrance = True
                            # If NOT a left bottom corner and the first tunnel tile
                            if self.tiles[y-1][x].type == TILE_TYPE.BACKGROUND and y > min(y1, y2):
                                self.tiles[y-1][x].type = TILE_TYPE.CORRIDOR
                                self.tiles[y-1][x].blocked = False
                                self.tiles[y-1][x].block_sight = False
                            
                    # Wall detection
                    if ((y == room.y1 or y == room.y2) and 
                        not (self.tiles[y][x-1].type == TILE_TYPE.ENTRANCE or self.tiles[y][x+1].type == TILE_TYPE.ENTRANCE)):
                        entrance = True
                    
                    break # Intersection found
            
            # The last tile
            if y == max(y1, y2):
                # Tunnel goes through the room and ends at the bottom wall
                if self.tiles[y-1][x].type == TILE_TYPE.FLOOR and entrance is True:
                    return None # Don't go to the next if statement and end the method
            # The first tile
            elif y == min(y1, y2) and entrance is True:
                entrance = False
            
            # All tiles
            if entrance is True: # Entrance detected
                self.tiles[y][x].type = TILE_TYPE.ENTRANCE
                self.tiles[y][x].blocked = False
                self.tiles[y][x].block_sight = False
            elif intersection is False and corner_detected is False: # Corridor detected
                self.tiles[y][x].type = TILE_TYPE.CORRIDOR
                self.tiles[y][x].blocked = False
                self.tiles[y][x].block_sight = False

    def create_horiz_tunnel(self, x1: int, x2: int, y: int, rooms: list) -> None:
        '''
        Creates a horizontal tunnel between x1 and x2 at y.
        Requires list of rooms to set the Tile type.
        '''

        for x in range(min(x1, x2), max(x1,x2)+1):
            intersection = False
            entrance = False
            corner_detected = False

            # Checks if a tile intersects a room
            for room in rooms:
                if room.intersect_tile(x, y):
                    intersection = True
                    # Corner detection
                    if ((x == room.x1 and y == room.y1) or (x == room.x1 and y == room.y2) or
                        (x == room.x2 and y == room.y1) or (x == room.x2 and y == room.y2)):
                        
                        corner_detected = True

                        # Check for bottom corner (from room perspective)
                        if room.intersect_tile(x, y-1):
                            y -= 1
                            # Check if there is no entrance above already
                            if not self.tiles[y-1][x].type == TILE_TYPE.ENTRANCE:
                                entrance = True
                            # If NOT a right bottom corner and the first tunnel tile
                            if self.tiles[y][x-1].type == TILE_TYPE.BACKGROUND and x > min(x1, x2):
                                self.tiles[y][x-1].type = TILE_TYPE.CORRIDOR
                                self.tiles[y][x-1].blocked = False
                                self.tiles[y][x-1].block_sight = False
                            
                        # Top corner (from room perspective)
                        else:
                            y += 1
                            # Check if there is no entrance below already
                            if not self.tiles[y+1][x].type == TILE_TYPE.ENTRANCE:
                                entrance = True
                            # If NOT a right top corner and the first tunnel tile
                            if self.tiles[y][x-1].type == TILE_TYPE.BACKGROUND and x > min(x1, x2):
                                self.tiles[y][x-1].type = TILE_TYPE.CORRIDOR
                                self.tiles[y][x-1].blocked = False
                                self.tiles[y][x-1].block_sight = False
                            
                    # Wall detection
                    if ((x == room.x1 or x == room.x2) and 
                        not (self.tiles[y-1][x].type == TILE_TYPE.ENTRANCE or self.tiles[y+1][x].type == TILE_TYPE.ENTRANCE)):
                        entrance = True
                    
                    break # Intersection found
            
            # The last tile
            if x == max(x1, x2):
                # Tunnel goes through the room and ends at the right wall
                if self.tiles[y][x-1].type == TILE_TYPE.FLOOR and entrance is True:
                    return None # Don't go to the next if statement and end the method
            # The first tile
            elif x == min(x1, x2) and entrance is True:
                entrance = False
            
            # All tiles
            if entrance is True: # Entrance detected
                self.tiles[y][x].type = TILE_TYPE.ENTRANCE
                self.tiles[y][x].blocked = False
                self.tiles[y][x].block_sight = False
            elif intersection is False and corner_detected is False: # Corridor detected
                self.tiles[y][x].type = TILE_TYPE.CORRIDOR
                self.tiles[y][x].blocked = False
                self.tiles[y][x].block_sight = False
    
    def create_room(self, room: Rect) -> None:
        '''
        Creates a new room on the map.
        '''

        for y in range(room.y1, room.y2+1):
            for x in range(room.x1, room.x2+1):
                if x == room.x1 or x == room.x2:
                    self.tiles[y][x].type = TILE_TYPE.V_WALL
                    self.tiles[y][x].blocked = True
                elif y == room.y1 or y == room.y2:
                    self.tiles[y][x].type = TILE_TYPE.H_WALL
                    self.tiles[y][x].blocked = True
                else:
                    self.tiles[y][x].type = TILE_TYPE.FLOOR
                    self.tiles[y][x].blocked = False
                self.tiles[y][x].block_sight = False
    
    def generate_new_room(
        self,
        room_min_size: int,
        room_max_size: int,
        map_width, map_height: int
        ) -> Rect:
        '''
        Generates random dimensions for the room and returns the new room with this dimensions
        '''

        # Random width and height. We add 1 to account for walls
        w = randint(room_min_size, room_max_size) +1
        h = randint(room_min_size, room_max_size) +1
        # Random position without going out of the boundaries of our map
        x = randint(1, map_width-w-1)
        y = randint(1, map_height-h-1)

        return Rect(x, y, w, h)

    def generate_dungeon(
        self,
        min_rooms: int,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int, 
        agent: Entity
        ) -> None:
        '''
        Generates a new dungeon with random room layout.
        '''

        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            new_room = self.generate_new_room(room_min_size, room_max_size, map_width, map_height)

            # Run through the other rooms and check if they intersect
            intersection = False
            for other_room in rooms:
                if new_room.intersect_room(other_room):
                    intersection = True
                    break
            if not intersection:
                # There are no intersections, so this room is valid
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # Agent starts at this room
                    agent.x = new_x
                    agent.y = new_y

                rooms.append(new_room)
                num_rooms += 1
        
        # Last thing is to assure that we have at least min_rooms generated
        if num_rooms < min_rooms:
            num_loops = 0 # Ensures while loop breaks after a certain number of loops
            while num_rooms < min_rooms:
                num_loops += 1
                
                new_room = self.generate_new_room(room_min_size, room_max_size, map_width, map_height)

                # Run through the other rooms and check if they intersect
                intersection = False
                for other_room in rooms:
                    if new_room.intersect_room(other_room):
                        intersection = True
                        break
                if not intersection:
                    # There are no intersections, so this room is valid
                    self.create_room(new_room)
                    rooms.append(new_room)
                    num_rooms += 1
                
                if num_loops > 100:
                    print("ERROR: Could not generate the minimum number of rooms specified!")
                    break
        
        # Connecting all rooms
        for i in range(1, len(rooms)):
            # Getting the center of a current room
            (curr_x, curr_y) = rooms[i].center()

            # Getting the center of a current room
            (prev_x, prev_y) = rooms[i-1].center()

            # Connecting the current room to the previous one
            # Flip a coin to check if we go horziontally and then vertically or the other way 
            if randint(0,1) == 1:
                # First go horizontally and then vertically
                self.create_horiz_tunnel(prev_x, curr_x, prev_y, rooms)
                self.create_vert_tunnel(prev_y, curr_y, curr_x, rooms)
            else:
                self.create_vert_tunnel(prev_y, curr_y, prev_x, rooms)
                self.create_horiz_tunnel(prev_x, curr_x, curr_y, rooms)