from random import choice

from ..classPassive import Passive


# Clones random active ability
class Mirror(Passive):
    """
    A passive ability that creates a mirrored copy of another random ability.
    
    The Mirror class extends the Passive base class and provides functionality to
    clone an existing ability from the player's ability collection. When initialized,
    it randomly selects one of the player's abilities and creates a duplicate with
    the same properties but marked as "mirrored".
    
    Core functionality:
    - Randomly selects an ability from the player's current abilities
    - Creates a mirrored clone of the selected ability
    - Adds the cloned ability to the player's ability collection
    - Synchronizes level progression between the original Mirror and its clone
    
    Constructor parameters are inherited from the Passive base class:
    - screen: Display surface for rendering
    - ability: Dictionary containing ability configuration data
    - player: Player object that owns this ability
    - group: Sprite group for ability management
    - enemy_group: Group of enemy sprites for interaction
    - timer: Game timer for ability timing
    
    Note: This ability requires the player to have at least one existing ability
    to clone. The cloned ability will have " mirrored" appended to its name.
    """
    def __post__init__(self):
        cloning = choice(self.player.abilities)
        import classes.Abilities
        self.clone = getattr(classes.Abilities, cloning.ability['class'])
        self.clone = self.clone(self.screen, cloning.ability, cloning.player, cloning.group, cloning.enemy_group, cloning.timer)
        self.clone.name += ' mirrored'
        self.player.abilities.append(self.clone)

    def on_level_up(self) -> None:
        """
        Handle level up event by incrementing the level for both the current object and its clone.
        
        This method is called when a level up event occurs. It increases the level
        attribute by 1 for both the current instance and its associated clone object.
        
        Returns:
            None
        """
        self.level += 1
        self.clone.level += 1
