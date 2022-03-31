'''
This is a simple version of a rogue-like game called 'Rogue's Soul'. There is
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
exceeding step limit).Additionally, an agent gets NUM_SOULS_COLLECTED x 1 
each time it picks some souls, +1 every time agent discovers new corridor tile
or room (except the starting one).

The game is considered solved once the agent consistently gets 70% of the
maximum reward. This should be equal to collecting the majority of the souls
and completing the level by escaping the dungeon.

The episode finishes if an agent dies, uses the exit, or exceeds steps limit.

The environment can be easily configured by changing values in the respective
variables in the env_setup.py file.

Randomness in the generation process can be controlled by setting the seed.
NOTE: Setting the seed requires calling the reset() function.

To play the game yourself launch: main.py.

Created by Wiktor Duch.
Game based on: http://rogueliketutorials.com/tutorials/tcod/v2/.
'''

import numpy as np
from typing import Any, Tuple
from gym import Env
from gym.spaces import Box, Discrete
from typing import List, Optional
import random

import exp3_env_setup as setup
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
        TILE_TYPE.BACKGROUND: -1,
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
        'Demon' : 11,
        'Crow' : 12,
        'Knight': 13,
        'Rat' : 14,
        'Skeleton' : 15,
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
        'Cursed Rogue\'s Armour' : 35,
        'Bastard Sword' : 36,
        'Greatshield' : 37,
        'Dragon Armour' : 38 # Current max value
    }

    def __init__(
        self,
        max_steps: int = 1000,
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
            low=-1,
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

        # Randomness testing
        self.entry_in_set: int = -1
        self.test: bool = False
        self.eval: bool = False
        self.test_set: List[int] = list()
        self.eval_set: List[int] = list()

    @property
    def unwrapped(self) -> Env:
        return self

    @property
    def map(self) -> Map:
        return self.engine.map

    def step(self, key: np.int64, print_stats:bool = True) -> Tuple[List[List[int]], int, bool, dict]:
        # Set basic return values
        # reward = -0.1 # Punishing wasting time and too much exploration
        reward = 0
        done = False
        info = {
            'Completed' : False,
            'Died' : False,
        }
        # Update state
        self.current_step += 1
        if self.max_steps == self.current_step:
            reward = -100
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
                self.engine.stats.valid_actions += 1
            except:
                self.engine.stats.invalid_actions += 1
                # Do nothing
                pass

            self.engine.handle_enemy_turns()
        
            room_updated, corr_updated = discover_tiles(self.map, self.engine.agent) # Discovers tiles ahead of the agent
            if room_updated or corr_updated:
                reward += 1 # Update reward on discovering new area

            # Update statistics
            if room_updated:
                self.engine.stats.fov_updates += 1
                self.engine.stats.rooms_visted += 1
                if self.engine.level == 1:
                    self.engine.stats.rooms_visited_lvl_1 += 1
                elif self.engine.level == 2:
                    self.engine.stats.rooms_visited_lvl_2 += 1
                elif self.engine.level == 3:
                    self.engine.stats.rooms_visited_lvl_3 += 1
            elif corr_updated:
                self.engine.stats.fov_updates += 1

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
            reward += souls_diff # Update reward based on souls found

        # Check if enemies killed
        if len(list(self.map.actors)) != num_actors_before:
            pass
        
        self.state = self.get_next_observation()

        # Update statistics
        if done:
            self.engine.update_stats()
            if print_stats:
                self.engine.stats.display()

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
        # Get the previous seed
        if len(self.test_set) == 0 and len(self.eval_set) == 0:
            seed = self.get_seed()
        else: # Get next seed in the test or eval set
            self.entry_in_set += 1
            if self.test:
                seed = self.test_set[self.entry_in_set % len(self.test_set)]
            elif self.eval:
                seed = self.eval_set[self.entry_in_set % len(self.eval_set)]

        # Get new Engine instance
        self.engine = setup.new_engine(
            prev_mode=self.get_mode(),
            prev_seed=seed
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

    def change_set(self, mode:int) -> None:
        '''
        Toggles between evaluation and test seed sets.
        0: test
        else: evaluation
        '''
        if mode == 0:
            self.test = True
            self.eval = False
        else:
            self.test = False
            self.eval = True
        self.entry_in_set = -1
        self.reset()

    def set_test_and_eval_sets(self, test_size:int, eval_size:int) -> None:
        self.test = True
        for _ in range(test_size):
            self.test_set.append(random.randint(1, test_size*100))
        for _ in range(eval_size):
            self.eval_set.append(random.randint(test_size*100+1, (test_size+eval_size)*100))

    def get_test_set(self) -> List[int]:
        return self.test_set
    
    def get_eval_set(self) -> List[int]:
        return self.eval_set

    def set_seed(self, seed: int) -> None:
        '''
        Sets seed.
        This seed is not used till the game is reseted.
        - seed(int): seed value for RNG
        '''
        self.engine.set_seed(seed)
        self.reset()

    def get_seed(self) -> Optional[int]:
        return self.engine.seed
    
    def set_mode(self, mode:int) -> None:
        '''
        Sets modes:
        0: Game mode
        1: Developer mode
        '''
        self.engine.set_game_mode(mode)
        self.reset()

    def get_mode(self) -> int:
        return self.engine.game_mode

    '''HELPER FUNCTIONS'''
    def get_valid_actions(self) -> List[int]:
        '''
        Returns a list of all the valid actions for the current agent's position.
        '''
        x = self.engine.agent.x
        y = self.engine.agent.y
        valid_actions: List[int] = []
        if not self.map.tiles[y-1][x].blocked:
            valid_actions.append(0)
        if not self.map.tiles[y+1][x].blocked:
            valid_actions.append(1)
        if not self.map.tiles[y][x-1].blocked:
            valid_actions.append(2)
        if not self.map.tiles[y][x+1].blocked:
            valid_actions.append(3)
        
        return valid_actions

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
        
        # Append valid actions
        val_acts = self.get_valid_actions()
        if 0 in val_acts:
            obs_space[last_y][7] = 0
        else:
            obs_space[last_y][7] = self.tile_type_to_int.get(TILE_TYPE.BACKGROUND)

        if 1 in val_acts:
            obs_space[last_y][8] = 1
        else:
            obs_space[last_y][8] = self.tile_type_to_int.get(TILE_TYPE.BACKGROUND)

        if 2 in val_acts:
            obs_space[last_y][9] = 2
        else:
            obs_space[last_y][9] = self.tile_type_to_int.get(TILE_TYPE.BACKGROUND)
        
        if 3 in val_acts:
            obs_space[last_y][10] = 3
        else:
            obs_space[last_y][10] = self.tile_type_to_int.get(TILE_TYPE.BACKGROUND)

        for x in range(11, self.map.width):
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