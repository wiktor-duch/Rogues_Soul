import traceback
import time
from game.setup_configs.demo_setup import new_engine, new_map

'''
Based on:
http://rogueliketutorials.com/tutorials/tcod/v2/
'''

def main():
    engine = new_engine(render_info=True)
    
    if new_map(engine): # Map was correctly generated
        # Game mainloop
        start_time = time.time()
        while not engine.game_over and not engine.game_completed:
            engine.render(print_title=True)
            
            try:
                engine.event_handler.handle_player_events()
            except Exception:
                engine.message_log.add_message(traceback.format_exc())
            
            print('\n') # Adds a line break beetween terminal outputs

            if engine.game_over is True:
                print('YOU DIED!')
            
            if engine.game_completed is True:
                engine.stats.levels_completed += 1
                print('CONGRATULATIONS!\nYou managed to escape from your nightmare.\n')
        end_time = time.time()
        # Update and print stats
        engine.stats.time_elapsed = (int(end_time-start_time))
        engine.stats.hp = engine.agent.fighter.max_hp
        engine.stats.defense = engine.agent.fighter.defense
        engine.stats.power = engine.agent.fighter.power
        engine.stats.souls = engine.agent.souls
        # Display statistics
        engine.stats.display()
if __name__ == '__main__':
    main()