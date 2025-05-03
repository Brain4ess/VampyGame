from ..classPassive import Passive

class Overclock(Passive):
    def __post__init__(self):
        self.onlevelup()

    def onlevelup(self):
        self.level +=1
        for i in self.player.abilities:
            i.cooldown -= 0.25
    
    def onAbilityAdd(self, ability):
        ability.cooldown -= self.level * 0.25