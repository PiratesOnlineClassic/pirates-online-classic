from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.directnotify import DirectNotifyGlobal
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.world.WorldGlobals import *
from pirates.world.InteriorAreaBuilderAI import InteriorAreaBuilderAI

class DistributedGAInteriorAI(DistributedGameAreaAI, DistributedCartesianGridAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGAInteriorAI')

    def __init__(self, air):
        DistributedGameAreaAI.__init__(self, air)
        DistributedCartesianGridAI.__init__(self, air, GAME_AREA_INTERIOR_STARTING_ZONE, GAME_AREA_INTERIOR_GRID_SIZE,
            GAME_AREA_INTERIOR_GRID_RADIUS, GAME_AREA_INTERIOR_CELL_SIZE)

        self.connectorId = 0

        self.exteriorFrontDoor = None
        self.exteriorBackDoor = None
        self.interiorFrontDoor = None
        self.interiorBackDoor = None

        self.builder = InteriorAreaBuilderAI(air, self)

    def setConnectorId(self, connectorId):
        self.connectorId = connectorId

    def d_setConnectorId(self, connectorId):
        self.sendUpdate('setConnectorId', [connectorId])

    def b_setConnectorId(self, connectorId):
        self.setConnectorId(connectorId)
        self.d_setConnectorId(connectorId)

    def getConnectorId(self):
        return self.connectorId

    def setExteriorFrontDoor(self, exteriorFrontDoor):
        self.exteriorFrontDoor = exteriorFrontDoor

    def getExteriorFrontDoor(self):
        return self.exteriorFrontDoor

    def setExteriorBackDoor(self, exteriorBackDoor):
        self.exteriorBackDoor = exteriorBackDoor

    def getExteriorBackDoor(self):
        return self.exteriorBackDoor

    def setInteriorFrontDoor(self, interiorFrontDoor):
        self.interiorFrontDoor = interiorFrontDoor

    def getInteriorFrontDoor(self):
        return self.interiorFrontDoor

    def setInteriorBackDoor(self, interiorBackDoor):
        self.interiorBackDoor = interiorBackDoor

    def getInteriorBackDoor(self):
        return self.interiorBackDoor

    def delete(self):
        self.air.deallocateZone(self.zoneId)

        DistributedCartesianGridAI.delete(self)
        DistributedGameAreaAI.delete(self)
