from ..class_passive_ability import PassiveAbility


# Gives you more experience from killing enemies
class MoreExp(PassiveAbility):
    """
    A passive ability that enhances experience gain for the player.
    
    This class represents a passive skill that automatically triggers upon level up,
    providing a permanent increase to the player's experience gain rate. Each time
    the player levels up, their experience gain multiplier is increased by 60%.
    
    Core Functionality:
        - Automatically triggers on level up events
        - Increases experience gain multiplier by 60% per level
        - Tracks its own level progression
    
    Constructor Parameters:
        Inherits parameters from the Passive base class.
    
    Note:
        This passive has a compounding effect - each level up multiplies the current
        experience gain rate, potentially leading to exponential growth in experience
        acquisition over multiple levels.
    """
    def __post__init__(self):
        self.on_level_up()

    def on_level_up(self) -> None:
        """
        Handle the level up event for the player.
        
        This method is called when the player levels up. It increments the player's
        level by 1 and increases the experience gain multiplier by 60% (multiplied by 1.6).
        
        Side Effects:
            - Increments self.level by 1
            - Multiplies self.player.exp_gain by 1.6
        """
        self.level += 1
        self.player.exp_gain *= 1.6
