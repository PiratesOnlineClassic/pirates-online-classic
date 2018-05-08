from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from direct.directnotify import DirectNotifyGlobal

class DistributedLiarsDiceAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLiarsDiceAI')

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)
