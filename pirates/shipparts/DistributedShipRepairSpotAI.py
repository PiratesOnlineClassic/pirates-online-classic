
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedShipRepairSpotAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipRepairSpotAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.shipId = 0
        self.index = 0


    # setShipId(DoId) required broadcast ram
    
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

    # setIndex(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setIndex(self, index):
        self.index = index

    def d_setIndex(self, index):
        self.sendUpdate('setIndex', [index])

    def b_setIndex(self, index):
        self.setIndex(index)
        self.d_setIndex(index)

    def getIndex(self):
        return self.index


