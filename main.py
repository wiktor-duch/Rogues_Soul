import traceback

import game.setup as setup

'''
Based on:
http://rogueliketutorials.com/tutorials/tcod/v2/
'''

def main():
    engine = setup.new_engine(render_info=True)
    print(engine.get_game_mode())
    if setup.new_map(engine): # Map was correctly generated
        # Game mainloop
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
                print('CONGRATULATIONS!\nYou managed to escape from your nightmare.\n')

if __name__ == '__main__':
    main()