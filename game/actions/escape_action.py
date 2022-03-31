from game.actions.action import Action

class EscapeAction(Action):
    def perform(self):
        self.engine.game_over = True