from ..classPassive import Passive
from random import choice

class Mirror(Passive): 
    def __post__init__(self):
        cloning = choice(self.player.abilities)
        import classes.Abilities as clab
        self.clone = getattr(clab, cloning.ability['class'])
        self.clone = self.clone(self.screen, cloning.ability, cloning.player, cloning.group, cloning.enemy_group, cloning.timer)
        self.clone.name += ' mirrored'
        self.player.abilities.append(self.clone)

    def onlevelup(self):
        self.level += 1
        self.clone.level += 1