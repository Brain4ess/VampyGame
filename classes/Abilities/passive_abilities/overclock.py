from ..class_passive_ability import PassiveAbility


# Reduces the cooldowns of all abilities
class Overclock(PassiveAbility):
    """
    A passive ability that provides cooldown reduction benefits for player abilities.
    
    This class enhances gameplay by reducing ability cooldowns both when the player
    levels up and when new abilities are acquired. The cooldown reduction scales
    with the player's level, providing progressive improvement.
    
    Core Functionality:
        - Automatic cooldown reduction on level up (0.25s per level)
        - Retroactive cooldown reduction for newly acquired abilities
        - Passive enhancement that activates automatically during gameplay
    
    Constructor Parameters:
        Inherits from Passive class - refer to parent class documentation for
        specific parameter requirements (typically includes player reference).
    
    Note:
        This passive ability modifies ability cooldowns permanently. The effects
        are cumulative and irreversible during a game session.
    """
    def __post__init__(self):
        self.on_level_up()

    def on_level_up(self) -> None:
        """
        Handle the level up event for the player.
        
        This method increases the player's level by 1 and reduces the cooldown
        of all player abilities by 0.25 seconds as a level up bonus.
        
        Side Effects:
            - Increments self.level by 1
            - Reduces cooldown of all abilities in self.player.abilities by 0.25
        """
        self.level +=1
        for i in self.player.abilities:
            i.cooldown -= 0.25

    def on_ability_add(self, ability) -> None:
        """
        Callback function triggered when an ability is added.
        
        Reduces the cooldown of the newly added ability based on the current level.
        The cooldown reduction follows the formula: cooldown -= level * 0.25
        
        Args:
            ability: The ability object that was added. Must have a 'cooldown' attribute
                    that can be modified.
        
        Note:
            This method modifies the ability's cooldown property directly.
            Higher levels result in greater cooldown reduction.
        """
        ability.cooldown -= self.level * 0.25
