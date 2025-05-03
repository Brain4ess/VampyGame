from ..classPassive import Passive

class Overlevel(Passive):
    def __post__init__(self):
        self.onlevelup()

    def onlevelup(self):
        self.level += 1
        for i in self.player.abilities:
            i.max_level += 1
        for i in self.player.passives:
            if not (i is self):
                i.max_level += 1
    
    def onAbilityAdd(self, ability):
        ability.max_level += self.level
    
    def onPassiveAdd(self, passive):
        passive.max_level += self.level