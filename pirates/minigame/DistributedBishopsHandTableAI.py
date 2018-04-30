from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBishopsHandTableAI(DistributedPokerTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBishopsHandTableAI')

    def __init__(self, air):
        DistributedPokerTableAI.__init__(self, air)