from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI
from direct.directnotify import DirectNotifyGlobal

class Distributed7StudTableAI(DistributedPokerTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('Distributed7StudTableAI')

    def __init__(self, air):
        DistributedPokerTableAI.__init__(self, air)