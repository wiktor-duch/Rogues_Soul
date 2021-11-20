from game.actions.action_with_direction import Action
from game.exceptions import ImpossibleAction, InvalidMap


class UseExitAction(Action):
    def perform(self) -> None:
        '''
        Handles using the exit.
        '''
        if self.engine.world.current_level == self.engine.num_levels:
            # Game is completed
            self.engine.game_completed = True
        else: # New level should be generated
            try:
                self.engine.world.generate_level()
                self.engine.message_log.add_message(
                    'Welcome to the next level.'
                )
            except InvalidMap as exc:
                raise ImpossibleAction(exc.args[0])