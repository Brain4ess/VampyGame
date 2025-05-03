from ..classPassive import Passive

class Cheese(Passive):
    def __post__init__(self):
        self.onlevelup()
    
    def onlevelup(self):
        self.level += 1
        self.player.lives += 1