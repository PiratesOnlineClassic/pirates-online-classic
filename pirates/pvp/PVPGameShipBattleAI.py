
from pirates.pvp.PVPGameBaseAI import PVPGameBaseAI
from direct.directnotify import DirectNotifyGlobal

class PVPGameShipBattleAI(PVPGameBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameShipBattleAI')

    def __init__(self, air):
        PVPGameBaseAI.__init__(self, air)


    # setShipDoId(DoId)

    def setShipDoId(self, shipDoId):
        self.sendUpdate('setShipDoId', [shipDoId])

    # setBoarded() airecv clsend

    def setBoarded(self, boarded):
        pass


