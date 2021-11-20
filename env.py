import numpy as np
from typing import Tuple
from gym import Env
from gym.spaces import Box, Discrete
from typing import List, Optional

import env_setup as setup
import helper_functions as hel_fun
from game.actions import BumpAction
from game.vizualization import discover_tiles
from game.map_objects.map import Map

# https://github.com/kngwyu/rogue-gym/blob/master/python/rogue_gym/envs/rogue_env.py

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
            low=hel_fun.get_min_value_in_obs_space(),
            high=hel_fun.get_max_value_in_obs_space(),
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
        return hel_fun.get_next_observation(self.map)

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