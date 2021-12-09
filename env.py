'''
This is a simple version of a rogue-like game called 'Rogue's Soul. There is
no shop, spells, inventory, etc. A player can only go up, down, left, right
and whenever they 'step' on an item, they use it. To view, configure or add
more entities view the 'entities' package and 'entity_factory.py'.

The ACTION SPACE is discrete. It consists of only four actions: up, down, left,
right.

The SATE consists of a 2D array with integer values. Its shape is MAP_WIDTH x
MAP_HEIGHT+1.The additional row at the bottom shows some statistics such as
player's health and souls gathered. To see the meaning of each integer value,
view the dictionaries below.

The reward is 100 for escaping (using door) and -100 for losing (i.e. ding or
exceeding step limit).Additionally, an agent gets NUM_SOULS_COLLECTED x 0.1 
each time it picks some souls and -0.05 each time it tries invalid actions, 
i.e. 'bumping' into a wall.

The game is considered solved once the agent consistently gets 190+ points.
This is equal to 100 for winning and 2x50 for collecting (all) souls decreased
by some number of invalid moves.

The episode finishes if an agent dies, uses the exit, or exceeds steps limit.

The environment can be easily configured by changing values in the respective
values in the env_setup.py file.

Randomness in the generation process can be controlled by setting the seed.
NOTE: Setting the seed requires calling the reset() function.

To play the game yourself launch: main.py.

Created by Wiktor Duch.
Based on: http://rogueliketutorials.com/tutorials/tcod/v2/.
'''

import numpy as np
from typing import Any, Tuple
from gym import Env
from gym.spaces import Box, Discrete
from typing import List, Optional

import env_setup as setup
from game.actions import BumpAction
from game.entities import Item, Equipment, Actor
from game.vizualization import discover_tiles
from game.map_objects import Map, TILE_TYPE

class RoguesSoulsEnv(Env):
    metadata = {
        'render.modes' : ['human', 'ai']
    }

    MOVE_ACTIONS = {
        0: (0,-1), # UP
        1: (0,1), # DOWN
        2: (-1,0), # LEFT
        3: (1,0) # RIGHT
    }

    ACTIONS_LEN = len(MOVE_ACTIONS) 

    # Tiles have values 0 to 9
    tile_type_to_int = {
        TILE_TYPE.BACKGROUND: 0,
        TILE_TYPE.FLOOR : 1,
        TILE_TYPE.V_WALL : 2,
        TILE_TYPE.H_WALL : 2,
        TILE_TYPE.ENTRANCE : 3,
        TILE_TYPE.CORRIDOR : 4,
        TILE_TYPE.EXIT : 5
    }

    # Enemies have values 10 to 19
    enemy_to_int = {
        'Bat' : 10,
        'Crow' : 11,
        'Demon' : 12,
        'Knight': 13,
        'Agent' : 19
    }

    # Items have values 20 to 29
    item_to_int = {
        'Health Potion' : 20,
        'Soul' : 21,
        'Chest' : 22
    }

    # Pieces of equipment have values 30-39
    equipment_to_int = {
        'Short Sword' : 30,
        'Soldier\'s Shield' : 31,
        'Light Chain Mail' : 32,
        'Long Sword' : 33,
        'Kite Shield' : 34,
        'Cursed Rogue\'s Armour' : 35 # Current max value
    }

    def __init__(
        self,
        max_steps: int = 2000,
    ) -> None:

        # Game settings
        self.engine = setup.new_engine()
        
        is_correctly_generated = False
        while not is_correctly_generated:
            if setup.new_map(self.engine):
                is_correctly_generated = True
            else:
                print('Trying to generate map again.')

        # Spaces
        self.action_space = Discrete(n=self.ACTIONS_LEN)
        self.observation_space = Box(
            low=0,
            high=40,
            shape=(
                self.engine.world.height+1,
                self.engine.world.width,
            ),
            dtype=np.int8
        )
        self.state = self.get_next_observation()

        # Set maximum number of steps
        self.max_steps = max_steps
        self.current_step = 0

    @property
    def unwrapped(self) -> Env:
        return self

    @property
    def map(self) -> Map:
        return self.engine.map

    def step(self, key: np.int64) -> Tuple[List[List[int]], int, bool, dict]:
        # Set basic return values
        reward = 0
        done = False
        info = {
            'Completed' : False,
            'Died' : False,
            'Souls collected': 0,
            'Enemies killed' : 0,
        }
        # Update state
        self.current_step += 1
        if self.max_steps == self.current_step:
            reward -= 100
            done = True

        # Gathering statistics
        souls_before = self.engine.agent.souls
        num_actors_before = len(list(self.map.actors))

        # Apply action
        if key in self.MOVE_ACTIONS:
            dx, dy = self.MOVE_ACTIONS[key]
            try:
                action = BumpAction(self.engine.agent, dx, dy)
                action.perform()
            except:
                # Punish for invalid action
                # reward -= 0.05
                pass

            self.engine.handle_enemy_turns()
        
            discover_tiles(self.map, self.engine.agent) # Discovers tiles ahead of the agent

        # Calculate reward
        if self.engine.game_over is True:
            done = True # Update done
            info['Died'] = True # Update info
            reward = -100
        elif self.engine.game_completed is True:
            done = True # Update done
            info['Completed'] = True # Update info
            reward = 100
        else:
            souls_diff = self.engine.agent.souls - souls_before
            info['Souls collected'] += 1
            reward += souls_diff/10

        # Check if enemies killed
        if len(list(self.map.actors)) != num_actors_before:
            info['Enemies killed'] += 1
        
        self.state = self.get_next_observation()

        return self.state, reward, done, info

    def render(self, mode: str = 'human', close: bool = False) -> None:
        '''
        STUB
        '''
        if mode == 'human':
            return self.engine.render()
        elif mode == 'ai':
            print(self.state)
        return
    
    def reset(self) -> Any:
        '''
        Resets the game state.

        Returns the initial observation.
        '''
        # Get the previous mode
        prev_mode = self.get_mode()
        # Get the previous seed
        prev_seed = self.get_seed()

        # Get new Engine instance
        self.engine = setup.new_engine(
            prev_mode=prev_mode,
            prev_seed=prev_seed
        )
        
        # Create new map
        is_correctly_generated = False
        while not is_correctly_generated:
            if setup.new_map(self.engine):
                is_correctly_generated = True
            else:
                print('Trying to generate map again.')
        
        # Reset steps
        self.current_step = 0
        
        self.state = self.get_next_observation()

        return self.state

    def set_seed(self, seed: int) -> None:
        '''
        Sets seed.
        This seed is not used till the game is reseted.
        - seed(int): seed value for RNG
        '''
        self.engine.set_seed(seed)

    def get_seed(self) -> Optional[int]:
        return self.engine.seed
    
    def set_mode(self, mode:int) -> None:
        self.engine.set_game_mode(mode)

    def get_mode(self) -> int:
        return self.engine.game_mode

    '''HELPER FUNCTIONS'''
    def get_next_observation(self) -> Any:
        obs_space = [[-1 for x in range(self.map.width)] for y in range(self.map.height+1)]

        for y in range(self.map.height):
            for x in range(self.map.width):
                if self.engine.get_game_mode() == 0:
                    
                    if not self.map.tiles[y][x].discovered: # Sets undiscovered tiles to background
                        obs_space[y][x] = self.tile_type_to_int.get(TILE_TYPE.BACKGROUND)
                    else:
                        entity_added = self.add_entity(x, y, obs_space)
                        if entity_added is False:
                            obs_space[y][x] = self.tile_type_to_int.get(self.map.tiles[y][x].type)
        
                elif self.engine.get_game_mode() == 1:
                    
                    entity_added = self.add_entity(x, y, obs_space)
                    if entity_added is False:
                        obs_space[y][x] = self.tile_type_to_int.get(self.map.tiles[y][x].type)

        # Last row contains agents statistics
        last_y = self.map.height

        # Set Level
        obs_space[last_y][0] = self.engine.level
        obs_space[last_y][1] = self.engine.num_levels
        # Set Souls
        obs_space[last_y][2] = self.engine.agent.souls
        # Set HP
        obs_space[last_y][3] = self.engine.agent.fighter.hp
        obs_space[last_y][4] = self.engine.agent.fighter.max_hp
        # Set Power
        obs_space[last_y][5] = self.engine.agent.fighter.power
        # Set Defense
        obs_space[last_y][6] = self.engine.agent.fighter.defense

        for x in range(7, self.map.width):
            obs_space[last_y][x] = self.tile_type_to_int.get(TILE_TYPE.BACKGROUND)

        return np.array(obs_space)

    def add_entity(self, x: int, y: int, arr: List[List[int]]) -> bool:
        '''
        Checks if there is an entity at the given coordinates to 
        be added to observation space.
        
        Returns True if there is one and False otherwise.
        '''
        entities = self.map.entities

        entities_sorted_for_rendering = sorted(
            entities, key=lambda x: x.render_order.value
        )

        if len(entities_sorted_for_rendering) != 0:
            for entity in entities_sorted_for_rendering:
                if x == entity.x and y == entity.y:
                    if isinstance(entity, Item):
                        arr[y][x] = self.item_to_int.get(entity.name)
                    elif isinstance(entity, Actor):
                        if entity.is_alive():
                            arr[y][x] = self.enemy_to_int.get(entity.name)
                        else:
                            return False
                    elif isinstance(entity, Equipment):
                        arr[y][x] = self.equipment_to_int.get(entity.name)
                    else:
                        print('No such entity type defiend in helper functions.')
                        return False
                    
                    return True
        
        return False