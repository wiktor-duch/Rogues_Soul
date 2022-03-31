from env import RoguesSoulsEnv

env = RoguesSoulsEnv(max_steps=500)
env.set_seed(4)
env.set_mode(1)
state = env.reset() # Needs resetting to apply above changes
# env.render(mode='human')

# Flatten obs
from gym.wrappers import FlattenObservation
env = FlattenObservation(env)
state = env.reset()
# print(state)
print(type(state))

# Load Model
from stable_baselines3 import DQN
model = DQN.load('./models/colab-exp-1/custom_rew_fun_6_75_')

import time
episodes = 2
print(f'TESTING MODEL ON {episodes} EPISODES\n')
for e in range(1, episodes+1):
    obs = env.reset()
    done = False
    score = 0

  
    while not done:
        env.render()
        # input('[ENTER]')
        time.sleep(2)
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(int(action))
        score += reward
    
    completed = info.get('Completed')
    print(f'Episode: {e}, Score: {score}, Completed: {completed}')