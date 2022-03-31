'''
Running this file allows to check if the custom env works as intended.
'''

from env import RoguesSoulsEnv
from stable_baselines3.common.env_checker import check_env

if __name__ == '__main__':
    print('Loading the env: Rogue\'s Soul')
    env = RoguesSoulsEnv(100)

    # Check spaces
    print('\nACTION SPACE\n')
    print(f'The actions space has shape: {env.action_space.n}\n')
    print(f'Sample observation space look:')
    print(f' (1) {env.action_space.sample()}')
    # print(f' (2) {env.action_space.sample()}')
    # print(f' (3) {env.action_space.sample()}\n')

    input('Press [ENTER] to continue.')

    print('\nOBSERVATION SPACE\n')
    print(f'The observation space has shape: {env.observation_space.shape}\n')
    print(f'Sample observation space look: ')
    print(f' (1) \n{env.observation_space.sample()}\n')
    # print(f' (2) \n{env.observation_space.sample()}\n')
    # print(f' (3) \n{env.observation_space.sample()}\n')

    input('Press [ENTER] to continue.')

    # Testing on random actions
    episodes = 10
    print(f'TESTING ENV ON {episodes} EPISODES\n')
    for e in range(1, episodes+1):
        env.reset()
        done = False
        score = 0

        while not done:
            # env.render()
            action = env.action_space.sample()
            _, reward, done, _ = env.step(action)
            score += reward
        
        print(f'Episode: {e}, Score: {score}')

    input('Press [ENTER] to continue.')

    # Testing on random actions (2)
    steps = 10
    print(f'\nVIZUALIZATION OF {steps} RANDOM STEPS\n')
    state = env.reset()
    done = False
    score = 0

    for step in range(steps):
        print('OBSERVATION SPACE:')
        env.render()
        action = env.action_space.sample()
        print(f'Action selected: {action}')
        n_state, reward, done, info = env.step(action)
        print(f'Reward: {reward}')
        score += reward
        if done:
            print(f'Score: {score}')
            break
        input('Press [ENTER] to continue.\n')

    # RENDERING COMPARISON
    print('\nHUMAN RENDERING vs AI RENDERING\n')
    
    print('Human sees as follows.')
    env.reset()
    env.set_mode(1)
    env.reset()
    env.render(mode='human')

    input('Press [ENTER] to continue.')

    print('AI sees as follows.')
    env.render(mode='ai')

    input('Press [ENTER] to continue.')

    # Check if compatible with stable-baselines-3
    print('CHECK WITH STABLE BASELINES 3')
    try:
        from gym.wrappers import FlattenObservation
        env = FlattenObservation(env)
        check_env(env, warn=True, skip_render_check=False)
        print('All fine!')
    except Exception as exc:
        print('Something went wrong!')
        print(exc)