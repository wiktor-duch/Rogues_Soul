# Experiment 1 Setup

# - Environemt is fixed with seed 4
# - Map is undiscovered

# General env_setup:
# - Num rooms: 3
# - Items: Souls (2), Health Potion (0-1), Enemies (Level 1, 1-2)

from env import RoguesSoulsEnv

env = RoguesSoulsEnv(max_steps=500)
env.set_seed(4)
env.set_game_mode(1)
# Needs resetting to apply above changes
state = env.reset()
env.render(mode='human')

# Flatten obs
from gym.wrappers import FlattenObservation
env_flat = FlattenObservation(env)
state = env_flat.reset()
# print(state)
print(type(state))

# Create Model
from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy

model = DQN('MlpPolicy', env, verbose=1)

# Train model
model.learn(total_timesteps=2000)