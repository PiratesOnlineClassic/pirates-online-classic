from direct.directnotify import DirectNotifyGlobal
from pirates.kraken.KrakenPartAI import KrakenPartAI
from pirates.kraken.BodyGameFSMAI import BodyGameFSMAI


class KrakenBodyAI(KrakenPartAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('KrakenBodyAI')

    HpScale = 5.0

    def createGameFSM(self):
        self.gameFSM = BodyGameFSMAI(self.air, self)
