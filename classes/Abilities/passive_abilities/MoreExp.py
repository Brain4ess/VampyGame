from ..classPassive import Passive


# Gives you more experience from killing enemies
class MoreExp(Passive):
    def __post__init__(self):
        self.onlevelup()

    def onlevelup(self):
        self.level += 1
        self.player.exp_gain *= 1.6
