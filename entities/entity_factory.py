from entities.entity import Entity

agent = Entity(char='@', name='Agent', blocks_movement=True)

# Enemy types
bat = Entity(char='b', name='Bat', blocks_movement=True)
demon = Entity(char='D', name='Demon', blocks_movement=True)