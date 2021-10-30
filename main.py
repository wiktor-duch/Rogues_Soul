import traceback

import setup

'''
Based on:
http://rogueliketutorials.com/tutorials/tcod/v2/
https://www.youtube.com/watch?v=zAVEsKPq8x0
'''

def main():
    engine = setup.new_engine(render_info=True)
    
    if setup.new_map(engine): # Map was correctly generated
    
        # Game mainloop
        while not engine.game_over:
            engine.render()
            
            try:
                engine.event_handler.handle_events()
            except Exception:
                engine.message_log.add_message(traceback.format_exc())
            
            print('\n') # Adds a line break beetween terminal outputs

            if engine.game_over == True:
                print('GAME OVER!')

if __name__ == '__main__':
    main()