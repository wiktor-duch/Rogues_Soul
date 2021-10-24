from components import (
    ConsumableHealing,
    ConsumableSoul,
    Fighter,
    HostileEnemy,
    Inventory
)
from entities.actor import Actor
from entities.item import Item

agent = Actor(
    char='@',
    name='Agent',
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=2, power=4),
    inventory=Inventory(capacity=6)
)

# Enemy types
bat = Actor(
    char='b',
    name='Bat',
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=6, defense=0, power=3),
    inventory=Inventory(capacity=0)
)

crow = Actor(
    char='c',
    name='Crow',
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=8, defense=0, power=4),
    inventory=Inventory(capacity=0)
)

demon = Actor(
    char='D',
    name='Demon',
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=8, defense=1, power=4),
    inventory=Inventory(capacity=0)
)

lost_knight = Actor(
    char='K',
    name='Knight',
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=2, power=2),
    inventory=Inventory(capacity=0)
)

# Items
health_potion = Item(
    char='*',
    name='Health Potion',
    consumable=ConsumableHealing(amount=6)
)

soul = Item(
    char='$',
    name='Souls',
    consumable=ConsumableSoul(amount=50)
)

# chest = Item(
#     char='?',
#     name='Chest',
#     consumable=None
# )