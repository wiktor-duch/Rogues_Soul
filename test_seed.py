from env import RoguesSoulsEnv

if __name__ == '__main__':
    print('Loading the env: Rogue\'s Soul')
    env = RoguesSoulsEnv(100)
    env.set_mode(1)
    env.choose_set_random = True

    print('Checking if fixed seed works')
    print('Set seed to 2')
    env.set_seed(2)
    
    env.set_test_and_eval_sets(test_size=5, eval_size=3)
    print(env.get_test_set())
    for _ in range(10):
        print(env.get_seed())
        env.reset()
    print('Change set')
    env.change_set(1)

    print(env.get_eval_set())
    for _ in range(5):
        print(env.get_seed())
        env.reset()
    

    # print('Seed: ' + str(env.get_seed()))
    # env.render()
    # input('[ENTER]')

    # env.reset()
    # print('Seed: ' + str(env.get_seed()))
    # env.render()
    # input('[ENTER]')

    # env.reset()
    # print('Seed: ' + str(env.get_seed()))

    # print('Set seed to None')
    # env.set_seed(None)
    # env.reset()
    # print('Seed: ' + str(env.get_seed()))
    # env.render()
    # input('[ENTER]')
    # env.reset()
    # print('Seed: ' + str(env.get_seed()))
    # env.render()
