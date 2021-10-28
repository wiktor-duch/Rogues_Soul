from actions.action_with_direction import ActionWithDirection
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.item_action import ItemAction
class BumpAction(ActionWithDirection):
    def perform(self) -> None:

        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        elif self.target_item:
            return ItemAction(self.entity, self.target_item).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()