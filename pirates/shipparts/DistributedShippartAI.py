from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class DistributedShippartAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShippartAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.ownerId = 0
        self.shipId = 0
        self.geomParentId = 0

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def d_setOwnerId(self, ownerId):
        self.sendUpdate('setOwnerId', [ownerId])

    def b_setOwnerId(self, ownerId):
        self.setOwnerId(ownerId)
        self.d_setOwnerId(ownerId)

    def getOwnerId(self):
        return self.ownerId

    def getOwner(self):
        return self.air.doId2do.get(self.ownerId)

    def setShipId(self, shipId):
        self.shipId = shipId

    def d_setShipId(self, shipId):
        self.sendUpdate('setShipId', [shipId])

    def b_setShipId(self, shipId):
        self.setShipId(shipId)
        self.d_setShipId(shipId)

    def getShipId(self):
        return self.shipId

    def getShip(self):
        return self.air.doId2do.get(self.shipId)

    def setGeomParentId(self, geomParentId):
        self.geomParentId = geomParentId

    def d_setGeomParentId(self, geomParentId):
        self.sendUpdate('setGeomParentId', [geomParentId])

    def b_setGeomParentId(self, geomParentId):
        self.setGeomParentId(geomParentId)
        self.d_setGeomParentId(geomParentId)

    def getGeomParentId(self):
        return self.geomParentId
