from operator import mod
from re import M
from env import RoguesSoulsEnv

if __name__ == '__main__':
    print('Loading the env: Rogue\'s Soul')
    env = RoguesSoulsEnv()

    env.set_mode(1)
    env.set_seed(6)

    # Doing 20 random actions
    steps = 20
    state = env.reset()
    done = False
    score = 0

    for step in range(steps):
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score += reward
        if done:
            break
    
    # RENDERING COMPARISON
    print('\nHUMAN RENDERING vs AI RENDERING\n')
    
    env.render(mode='human')
    
    input('Press [ENTER] to continue.')

    env.render(mode='ai')
