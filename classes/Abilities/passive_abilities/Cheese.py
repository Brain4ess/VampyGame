from ..classPassive import Passive


# Allows you to respawn once after death
class Cheese(Passive):
    def __post__init__(self):
        self.onlevelup()
    
    def onlevelup(self):
        self.level += 1
        self.player.lives += 1
