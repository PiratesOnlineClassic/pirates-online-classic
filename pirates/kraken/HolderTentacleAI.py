from direct.directnotify import DirectNotifyGlobal
from pirates.kraken.KrakenPartAI import KrakenPartAI
from pirates.kraken.HolderGameFSMAI import HolderGameFSMAI


class HolderTentacleAI(KrakenPartAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('HolderTentacleAI')

    HpScale = 2.0

    def __init__(self, air):
        KrakenPartAI.__init__(self, air)

    def createGameFSM(self):
        return HolderGameFSMAI(self.air, self)

    def d_emerge(self, emerge):
        self.sendUpdate('emerge', [emerge])

    def emerge(self, emerge):
        self.d_emerge(emerge)
