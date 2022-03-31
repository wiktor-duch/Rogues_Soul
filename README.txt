Game configuration:
1. Create a new file with your desired setup name in 'game.setup'.
2. Follow convention from the other setup files to configurate the game in your own way.
3. Change the import in the 'main.py' so that your setup file name follows after '.setup_configs'.

Gym environment configuration:
Either change the existing 'env_setup.py' file ot create a new file follwoing the setup file convention and import it in the 'env.py' file.

Run Game:
Running the game does not required any other external libraries. The version of python on which it was developed is 3.7.4.
To run a game launch 'main.py'.

Create Gym environment:
Initialize the environment to same variable by instantiating 'RoguesSoulsEnv' class, e.g.
env = RoguesSoulsEnv()

Game actions:
'a', '4' - go, attack, pick and use item left
'd', '6' - go, attack, pick and use item right
'w', '2' - go, attack, pick and use item up
's', '8' - go, attack, pick and use item down

Developer actions:
'm', 'M' - discover/cover map (change mode)
'q', 'Q' - quit the game
'p', 'P' - print player's equipment

Env description and important information can be found in the 'env.py' file.

Testing Gym environment:
Run 'test_env.py'.

Testing agent:
Run 'test_model.py'.