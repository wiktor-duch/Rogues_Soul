from game.actions.action import Action

class SwitchModeAction(Action):
    def perform(self):
        if self.engine.game_mode == 0:
            self.engine.game_mode = 1
        else:
            self.engine.game_mode = 0