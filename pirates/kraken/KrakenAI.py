
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class KrakenAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('KrakenAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.shipId = 0


    # setShipId(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setShipId(self, shipId):
        self.shipId = shipId

    def d_setShipId(self, shipId):
        self.sendUpdate('setShipId', [shipId])

    def b_setShipId(self, shipId):
        self.setShipId(shipId)
        self.d_setShipId(shipId)

    def getShipId(self):
        return self.shipId


