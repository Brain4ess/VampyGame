from abc import ABC, abstractmethod

import pygame as pg


class PassiveAbility(ABC):
    """
    Abstract base class for passive abilities in a game system.
    
    This class represents passive abilities that can be applied to a player character.
    Passive abilities are ongoing effects that don't require active use and typically
    provide permanent or semi-permanent bonuses, modifications, or special behaviors.
    
    Core functionality:
    - Manages passive ability properties (name, level, max level)
    - Handles visual representation through sprites
    - Provides callbacks for ability and passive addition events
    - Supports leveling system for passive abilities
    
    Args:
        screen (pg.Surface): The pygame surface for rendering the passive's visual elements
        passive (dict): Dictionary containing passive ability configuration with keys:
                       - 'name': Name of the passive ability
                       - 'max_level': Maximum level this passive can reach
                       - 'icon': File path to the passive's icon image
        player: The player object that owns this passive ability
        timer: Game timer object for time-based passive effects
    
    Note:
        - This is an abstract class and cannot be instantiated directly
        - Subclasses must implement the __post__init__ method
        - Icon images are automatically scaled to 64x64 pixels
        - Level starts at 0 and can be increased up to max_level
    """
    def __init__(self, screen: pg.Surface, passive: dict, player, timer):
        self.screen = screen
        self.player = player
        self.timer = timer
        self.passive = passive
        self.name = passive['name']
        self.level = 0
        self.max_level = passive['max_level']
        self.sprite = pg.transform.scale(pg.image.load(passive['icon']), (64, 64))
        self.__post__init__()

    @abstractmethod
    def __post__init__(self):
        pass

    def on_ability_add(self, ability) -> None:
        """
        Called when an ability is added to this entity.
        
        This method serves as a callback that is triggered whenever a new ability
        is added to the current entity. Subclasses should override this method
        to implement specific behavior when abilities are added.
        
        Args:
            ability: The ability object that was added to this entity.
                    The type and structure of this parameter depends on the
                    specific ability system implementation.
        
        Note:
            This is a placeholder method that does nothing by default.
            Subclasses should override this method to provide specific
            functionality when abilities are added.
        """
        pass

    def on_passive_add(self, passive) -> None:
        """
        Called when a passive ability is added to the entity.
        
        This method is triggered whenever a passive ability is applied to or 
        added to the current entity. It serves as a hook for handling passive 
        ability addition events.
        
        Args:
            passive: The passive ability being added to the entity. The type
                    and structure of this parameter depends on the passive
                    ability system implementation.
        
        Note:
            This is a placeholder method that should be overridden in subclasses
            to implement specific behavior when passive abilities are added.
        """
        pass
