class Entity:
    def __init__(self, x_coord: int, y_coord: int, char: str):
        """
        A generic object to represent player, enemies, items, etc.
        """

        self.x = x_coord
        self.y = y_coord
        self.char = char

    def move(self, dx: int, dy: int) -> None:
        '''
        Changes the x and y coordinates of the entity.
        '''

        self.x += dx
        self.y += dy