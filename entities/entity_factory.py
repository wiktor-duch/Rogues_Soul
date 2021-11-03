from components.consumable_components import (
    ConsumableHealing,
    ConsumableReward,
    ConsumableSoul
)
from components.equippable_components import (
    ShortSword,
    LongSword,
    LightChainMail,
    CursedRoguesArmour,
    SoldiersShield,
    KiteShield
)
from components import (
    ActorsEquipment,
    Fighter,
    HostileEnemy,
    Inventory
)
from entities.actor import Actor
from entities.item import Item
from entities.equipment import Equipment

agent = Actor(
    char='@',
    name='Agent',
    ai_cls=HostileEnemy,
    actor_equipment=ActorsEquipment(),
    fighter=Fighter(base_hp=16, base_defense=2, base_power=4),
    inventory=Inventory(capacity=6)
)

# Enemy types
bat = Actor(
    char='b',
    name='Bat',
    ai_cls=HostileEnemy,
    actor_equipment=ActorsEquipment(),
    fighter=Fighter(base_hp=6, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0)
)

crow = Actor(
    char='c',
    name='Crow',
    ai_cls=HostileEnemy,
    actor_equipment=ActorsEquipment(),
    fighter=Fighter(base_hp=8, base_defense=0, base_power=4),
    inventory=Inventory(capacity=0)
)

demon = Actor(
    char='D',
    name='Demon',
    ai_cls=HostileEnemy,
    actor_equipment=ActorsEquipment(),
    fighter=Fighter(base_hp=8, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0)
)

lost_knight = Actor(
    char='K',
    name='Knight',
    ai_cls=HostileEnemy,
    actor_equipment=ActorsEquipment(),
    fighter=Fighter(base_hp=8, base_defense=2, base_power=4),
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

chest = Item(
    char='?',
    name='Chest',
    consumable=ConsumableReward(
        pct=0.5,
        num_souls=25,
        amount_hp=1
    )
)

# Equipment
# Sords
short_sword = Equipment(
    char='/',
    name='Short Sword',
    equippable=ShortSword()
)

long_sword = Equipment(
    char='/',
    name='Long Sword',
    equippable=LongSword()
)

# Shields
soldiers_shield = Equipment(
    char='(',
    name='Soldier\'s Shield',
    equippable=SoldiersShield()
)

kite_shield = Equipment(
    char='(',
    name='Kite Shield',
    equippable=KiteShield()
)

# Armours
light_chain_mail = Equipment(
    char='[',
    name='Light Chain Mail',
    equippable=LightChainMail()
)

cursed_rogues_armour = Equipment(
    char='[',
    name='Cursed Rogue\'s Armour',
    equippable=CursedRoguesArmour()
)