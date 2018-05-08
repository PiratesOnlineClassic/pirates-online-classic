from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from direct.directnotify import DirectNotifyGlobal

class DistributedDiceGameAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDiceGameAI')

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)
