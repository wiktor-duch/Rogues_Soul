from actions.action_with_direction import ActionWithDirection
from actions.equip_action import EquipAction
from actions.item_action import ItemAction
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction
from actions.use_exit_action import UseExitAction

class BumpAction(ActionWithDirection):
    def perform(self) -> None:

        if self.target_actor: # There is an enemy as destination
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        elif self.destination_is_exit: # There is an exit tile
            return UseExitAction(self.entity).perform()

        elif self.target_item: # There is an item there
            return ItemAction(self.entity, self.target_item).perform()
        
        elif self.target_equipment: # There is a piece of equipment
            return EquipAction(self.entity, self.target_equipment).perform()

        else: # Try moving 
            return MovementAction(self.entity, self.dx, self.dy).perform()