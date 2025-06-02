from ..classPassive import Passive


# Allows you to respawn once after death
class Cheese(Passive):
    """
    A passive item that automatically triggers level progression and rewards the player.
    
    The Cheese class represents a special passive item that handles level-up events
    automatically upon initialization. When activated, it increments the player's
    current level and grants an additional life as a reward.
    
    Core functionality:
    - Automatic level progression upon initialization
    - Awards extra life to the player
    - Inherits passive item behavior from the Passive base class
    
    Args:
        Inherits constructor parameters from the Passive base class.
    
    Note:
        This item triggers its effect immediately upon creation via __post_init__.
        The player object must be properly initialized before using this class.
    """
    def __post__init__(self):
        self.on_level_up()

    def on_level_up(self) -> None:
        """
        Handle the level up event for the player.
        
        This method is called when the player successfully completes a level.
        It increments the current level and awards an extra life to the player
        as a reward for progressing through the game.
        """
        self.level += 1
        self.player.lives += 1
