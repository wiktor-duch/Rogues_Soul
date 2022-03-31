'''
Inspired by:
http://rogueliketutorials.com/tutorials/tcod/v2/
'''
from game.entities import Entity, Actor
from game.map_objects import Map,TILE_TYPE

from typing import Set

tile_type_to_char = {
    TILE_TYPE.V_WALL : '|',
    TILE_TYPE.H_WALL : '-',
    TILE_TYPE.FLOOR : '.',
    TILE_TYPE.CORRIDOR : '#',
    TILE_TYPE.ENTRANCE : '+',
    TILE_TYPE.EXIT : '>'
}

def render_map(map: Map, game_mode_on: bool) -> None:
    '''
    Renders the entire map.
    '''
    
    for y in range(map.height):
        for x in range(map.width):
            # If tile is undiscovered is rendered as a space
            if game_mode_on:
                if not map.tiles[y][x].discovered:
                    print(' ', end='')
                else:
                    entity_drawn = draw_entity(map.entities, x, y)
                    if entity_drawn is False:
                        print(tile_type_to_char.get(map.tiles[y][x].type), end='')
            
            # Activates development mode
            else:
                if map.tiles[y][x].type == TILE_TYPE.BACKGROUND:
                    print(' ', end='')
                else:
                    entity_drawn = draw_entity(map.entities, x, y)
                    if entity_drawn is False:
                        print(tile_type_to_char.get(map.tiles[y][x].type), end='')
        print('')

def draw_entity(entities: Set[Entity], x_coord: int, y_coord: int) -> bool:
    '''
    Checks if there is an entity at the given coordinates to be drawn.
    Returns true if there is one.
    '''

    entities_sorted_for_rendering = sorted(
        entities, key=lambda x: x.render_order.value
    )

    for entity in entities_sorted_for_rendering:
        if x_coord == entity.x and y_coord == entity.y:
            print(entity.char, end='')
            return True
    return False

def render_game_intro() -> None:
    '''
    Prints big game's title with the description before launching the game.
    '''

    title = ('\n\t\t╔══╗ ╔══╗ ╔══ ╔  ╗ ╔══ ║ ╔══╗\n'
             + '\t\t╠═╦╝ ║  ║ ║ ╗ ║  ║ ╠═    ╚══╗\n'
             + '\t\t║ ║  ╚══╝ ╚═╝ ╚══╝ ╚══   ╚══╝\n\n'
             + '\t\t    ╔══╗ ╔══╗ ╔  ╗ ╔\n'
             + '\t\t    ╚══╗ ║  ║ ║  ║ ║\n'
             + '\t\t    ╚══╝ ╚══╝ ╚══╝ ╚══\n')
    
    print(title)
    input('Press [enter] to start.\n')

def render_break_line(width: int) -> None:
    '''
    Prints a line of the provided width.
    '''

    if width < 1:
        return # Invalid width provided
    
    for _ in range(width):
        print('-', end='')

def render_bottom_bar(
    curr_level: int,
    num_levels: int,
    agent: Actor
    ) -> None:
    '''
    This function renders the following game info at the bottom:
        - Current level
        - Agent's hp
        - Souls collected so far
    '''
    hp = agent.fighter.hp
    max_hp = agent.fighter.max_hp
    souls = agent.souls
    defense = agent.fighter.defense
    power = agent.fighter.power

    print(f'\t\tLEVEL: {curr_level}/{num_levels}\t  HP: {hp} \tSOULS: {souls}')
    print(f'\t\tDEFENSE: {defense}\tMAX HP: {max_hp} \tPOWER: {power}')