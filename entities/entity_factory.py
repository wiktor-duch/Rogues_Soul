from components.hostile_enemy import HostileEnemy
from components.fighter import Fighter
from entities.actor import Actor

agent = Actor(
    char='@',
    name='Agent',
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=2, power=2)
)

# Enemy types
bat = Actor(
    char='b',
    name='Bat',
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=6, defense=0, power=1)
)
demon = Actor(
    char='D',
    name='Demon',
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=8, defense=1, power=2)
)
lost_knight = Actor(
    char='K',
    name='Knight',
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=2, power=2)
)