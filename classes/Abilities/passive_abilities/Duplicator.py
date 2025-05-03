from ..classPassive import Passive
class Duplicator(Passive):
    def __post__init__(self):
        self.onlevelup()
    
    def onlevelup(self):
        self.level += 1
        for i in self.player.abilities:
            i.projectile_addition += 1
    
    def onAbilityAdd(self, ability):
        ability.projectile_addition += self.level