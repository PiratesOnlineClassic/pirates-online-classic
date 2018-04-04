
from direct.distributed.DistributedNodeUD import DistributedNodeUD
from direct.directnotify import DirectNotifyGlobal

class DistributedShippartUD(DistributedNodeUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShippartUD')

    def __init__(self, air):
        DistributedNodeUD.__init__(self, air)
        self.ownerId = 0
        self.shipId = 0
        self.geomParentId = 0


    # setOwnerId(uint32) required db
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def d_setOwnerId(self, ownerId):
        self.sendUpdate('setOwnerId', [ownerId])

    def b_setOwnerId(self, ownerId):
        self.setOwnerId(ownerId)
        self.d_setOwnerId(ownerId)

    def getOwnerId(self):
        return self.ownerId

    # setShipId(uint32) required broadcast ram db ownrecv
    
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

    # setGeomParentId(uint32) required broadcast ram db
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setGeomParentId(self, geomParentId):
        self.geomParentId = geomParentId

    def d_setGeomParentId(self, geomParentId):
        self.sendUpdate('setGeomParentId', [geomParentId])

    def b_setGeomParentId(self, geomParentId):
        self.setGeomParentId(geomParentId)
        self.d_setGeomParentId(geomParentId)

    def getGeomParentId(self):
        return self.geomParentId


