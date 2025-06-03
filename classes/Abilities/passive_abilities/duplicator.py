from ..class_passive_ability import PassiveAbility


# +1 to projectiles per level for each ability a player has
class Duplicator(PassiveAbility):
    """
    A passive ability that duplicates projectiles for all player abilities.
    
    The Duplicator class enhances the player's combat effectiveness by increasing
    the number of projectiles fired by all abilities. It automatically upgrades
    existing abilities when leveling up and enhances new abilities when they are
    acquired.
    
    Core functionality:
    - Increases projectile count for all existing abilities when leveling up
    - Automatically enhances new abilities with additional projectiles
    - Scales with level to provide progressive power increases
    
    Constructor parameters:
        Inherits from Passive class - specific parameters depend on parent class
        implementation.
    
    Notes:
        - Modifies abilities permanently by increasing their projectile_addition
        - Effects are cumulative and persist for the duration of the game session
        - All abilities must have a projectile_addition attribute to work properly
    """
    def __post__init__(self):
        self.on_level_up()

    def on_level_up(self) -> None:
        """
        Handle the level up event for the player.
        
        This method increments the player's level by 1 and enhances all of the player's
        abilities by increasing their projectile addition count by 1.
        
        Side Effects:
            - Increments self.level by 1
            - Increases projectile_addition by 1 for each ability in self.player.abilities
        """
        self.level += 1
        for i in self.player.abilities:
            i.projectile_addition += 1

    def on_ability_add(self, ability) -> None:
        """
        Called when an ability is added to modify its projectile properties.
        
        This method increases the projectile count of the given ability based on 
        the current level of this modifier.
        
        Args:
            ability: The ability object to be modified. Must have a 
                    projectile_addition attribute that can be incremented.
        """
        ability.projectile_addition += self.level
