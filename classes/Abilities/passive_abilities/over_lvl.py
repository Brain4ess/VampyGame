from ..class_passive_ability import PassiveAbility


# +1 to max_level to all abilities except self
class OverLvl(PassiveAbility):
    """
    A passive ability that increases the maximum level of other abilities and passives.
    
    The Overlevel class is a special passive that enhances the player's progression by
    increasing the maximum level cap for all abilities and passives. When the player
    levels up, this passive not only increases its own level but also raises the max_level
    for all existing abilities and passives. Additionally, when new abilities or passives
    are added, their max_level is immediately boosted based on the current level of this
    Overlevel passive.
    
    Core functionality:
    - Automatically triggers level-up handling when initialized
    - Increases max_level of all abilities and passives when player levels up
    - Enhances newly added abilities and passives based on current level
    
    Constructor parameters:
        Inherits from Passive class - specific parameters depend on parent implementation.
        
    Note:
        This class assumes the player object has 'abilities' and 'passives' attributes
        that are iterable collections. The class modifies other objects' max_level
        attributes, so ensure all abilities and passives have this attribute available.
    """
    def __post__init__(self):
        self.on_level_up()

    def on_level_up(self) -> None:
        """
        Handle level up event for the player.
        
        This method is called when the player levels up. It increments the current level
        and increases the maximum level for all abilities and passives (excluding self).
        
        The method performs the following actions:
        1. Increments the player's current level by 1
        2. Increases the max_level for all player abilities by 1
        3. Increases the max_level for all player passives by 1 (except for self)
        
        Note:
            This method assumes that self.player exists and has 'abilities' and 'passives'
            attributes that are iterable collections containing objects with 'max_level' attributes.
        """
        self.level += 1
        for i in self.player.abilities:
            i.max_level += 1
        for i in self.player.passives:
            if i is not self:
                i.max_level += 1

    def on_ability_add(self, ability) -> None:
        """
        Handle the event when an ability is added.
        
        This method is called when an ability is added to increase the maximum
        level of the ability by the current level of this object.
        
        Args:
            ability: The ability object that is being added. Must have a 
                    max_level attribute that can be modified.
        
        Side Effects:
            Modifies the max_level attribute of the provided ability object
            by adding the current level value to it.
        """
        ability.max_level += self.level

    def on_passive_add(self, passive) -> None:
        """
        Handle the addition of a passive ability by increasing its maximum level.
        
        This method is called when a passive ability is added to enhance its
        maximum level based on the current level of this object.
        
        Args:
            passive: The passive ability object to be enhanced. Must have a
                    max_level attribute that can be modified.
        
        Note:
            This method modifies the passive object in-place by incrementing
            its max_level attribute by the current level of this object.
        """
        passive.max_level += self.level
