'''

To play the game yourself, launch: main.py
'''

import numpy as np
from typing import Tuple
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
            dtype=np.int16
        )

        # Set maximum number of steps
        self.max_steps = max_steps
        self.current_step = 0

    @property
    def unwrapped(self) -> Env:
        return self

    @property
    def map(self) -> Map:
        return self.engine.map

    @property
    def next_obs(self) -> List[List[int]]:
        return self.get_next_observation()

    def step(self, key: int) -> Tuple[List[List[int]], int, bool, dict]:
        # Set basic return values
        reward = 0
        done = False
        info = {} # Placeholder for info

        self.current_step += 1
        if self.max_steps == self.current_step:
            done = True

        souls_before = self.engine.agent.souls

        # Apply action
        if key in self.MOVE_ACTIONS:
            info['action'] = key
            dx, dy = self.MOVE_ACTIONS[key]
            try:
                action = BumpAction(self.engine.agent, dx, dy)
                action.perform()
            except:
                # Punish for invalid action
                reward -= 5

            self.engine.handle_enemy_turns()
        
            discover_tiles(self.map, self.engine.agent) # Discovers tiles ahead of the agent

        # Calculate reward
        if self.engine.game_over is True:
            done = True # Update done
            reward = -100
        elif self.engine.game_completed is True:
            done = True # Update done
            reward = 100
        else:
            souls_diff = self.engine.agent.souls - souls_before
            reward += souls_diff

        return self.next_obs, reward, done, info

    def render(self, mode: str = 'human', close: bool = False) -> None:
        '''
        STUB
        '''
        if mode == 'human':
            return self.engine.render()
        elif mode == 'ai':
            print(self.next_obs)
        return
    
    def reset(self) -> List[List[int]]:
        '''
        Resets the game state.

        Returns the initial observation.
        '''

        # Get new Engine instance
        self.engine = setup.new_engine()
        
        # Create new map
        is_correctly_generated = False
        while not is_correctly_generated:
            if setup.new_map(self.engine):
                is_correctly_generated = True
            else:
                print('Trying to generate map again.')
        
        # Reset steps
        self.current_step = 0

        return self.next_obs

    def set_seed(self, seed: int) -> None:
        '''
        Sets seed.
        This seed is not used till the game is reseted.
        - seed(int): seed value for RNG
        '''
        self.engine.set_seed(seed)

    def get_seed(self) -> Optional[int]:
        return self.engine.seed
    
    def set_game_mode(self, mode:int) -> None:
        self.engine.set_game_mode(mode)

    def get_mode(self) -> int:
        return self.engine.game_mode

    '''HELPER FUNCTIONS'''
    def get_next_observation(self) -> List[List[int]]:
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

        obs_space = np.array(obs_space)

        return obs_space   

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
                            arr[y][x] = self.tile_type_to_int.get(entity.name)
                    elif isinstance(entity, Equipment):
                        arr[y][x] = self.equipment_to_int.get(entity.name)
                    else:
                        print('No such entity type defiend in helper functions.')
                        return False
                    
                    return True
        
        return False