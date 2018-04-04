
from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI
from direct.directnotify import DirectNotifyGlobal

class DistributedHoldemTableAI(DistributedPokerTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHoldemTableAI')

    def __init__(self, air):
        DistributedPokerTableAI.__init__(self, air)



