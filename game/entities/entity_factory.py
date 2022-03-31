'''
Inspired by:
http://rogueliketutorials.com/tutorials/tcod/v2/
'''
from game.components.consumable_components import (
    ConsumableHealing,
    ConsumableReward,
    ConsumableSoul
)
from game.components.equippable_components import (
    ShortSword,
    LongSword,
    BastardSword,
    LightChainMail,
    CursedRoguesArmour,
    DragonArmour,
    SoldiersShield,
    KiteShield,
    Greatshield
)
from game.components import (
    ActorsEquipment,
    Fighter,
    HostileEnemy,
    Inventory
)
from game.entities.actor import Actor
from game.entities.item import Item
from game.entities.equipment import Equipment

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

rat = Actor(
    char='r',
    name='Rat',
    ai_cls=HostileEnemy,
    actor_equipment=ActorsEquipment(),
    fighter=Fighter(base_hp=10, base_defense=0, base_power=5),
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

skeleton = Actor(
    char='S',
    name='Skeleton',
    ai_cls=HostileEnemy,
    actor_equipment=ActorsEquipment(),
    fighter=Fighter(base_hp=10, base_defense=2, base_power=5),
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
    name='Soul',
    consumable=ConsumableSoul(amount=50)
)

chest = Item(
    char='?',
    name='Chest',
    consumable=ConsumableReward(
        pct=0.5,
        num_souls=25,
        amount_hp=2
    )
)

# Equipment
# Sords
short_sword = Equipment(
    char='/',
    name='Short Sword',
    type='SWORD',
    equippable=ShortSword()
)

long_sword = Equipment(
    char='/',
    name='Long Sword',
    type='SWORD',
    equippable=LongSword()
)

bastard_sword = Equipment(
    char='/',
    name='Bastard Sword',
    type='SWORD',
    equippable=BastardSword()
)

# Shields
soldiers_shield = Equipment(
    char='(',
    name='Soldier\'s Shield',
    type='SHIELD',
    equippable=SoldiersShield()
)

kite_shield = Equipment(
    char='(',
    name='Kite Shield',
    type='SHIELD',
    equippable=KiteShield()
)

greatshield = Equipment(
    char='(',
    name='Greatshield',
    type='SHIELD',
    equippable=Greatshield()
)

# Armours
light_chain_mail = Equipment(
    char='[',
    name='Light Chain Mail',
    type='ARMOUR',
    equippable=LightChainMail()
)

cursed_rogues_armour = Equipment(
    char='[',
    name='Cursed Rogue\'s Armour',
    type='ARMOUR',
    equippable=CursedRoguesArmour()
)

dragon_armour = Equipment(
    char='[',
    name='Dragon Armour',
    type='ARMOUR',
    equippable=DragonArmour()
)