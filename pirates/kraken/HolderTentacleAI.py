from direct.directnotify import DirectNotifyGlobal
from pirates.kraken.KrakenPartAI import KrakenPartAI
from pirates.kraken.HolderGameFSMAI import HolderGameFSMAI


class HolderTentacleAI(KrakenPartAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('HolderTentacleAI')

    HpScale = 2.0

    def __init__(self, air):
        KrakenPartAI.__init__(self, air)
        self.emerged = 0

    def createGameFSM(self):
        self.gameFSM = HolderGameFSMAI(self.air, self)

    def d_emerge(self, emerge):
        self.sendUpdate('emerge', [emerge])

    def emerge(self, emerge):
        self.emerged = emerge
        self.d_emerge(emerge)

    def getEmerged(self):
        return self.emerged
