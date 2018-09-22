from direct.directnotify import DirectNotifyGlobal

from pirates.treasuremap.DistributedTreasureMapInstanceAI import DistributedTreasureMapInstanceAI


class TreasureMapBlackPearlAI(DistributedTreasureMapInstanceAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TreasureMapBlackPearlAI')

    def __init__(self, air):
        DistributedTreasureMapInstanceAI.__init__(self, air)

        self.fileName = 'BlackpearlWorld'
