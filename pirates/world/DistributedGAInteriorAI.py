from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.directnotify import DirectNotifyGlobal

from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.world import WorldGlobals
from pirates.world.InteriorAreaBuilderAI import InteriorAreaBuilderAI


class DistributedGAInteriorAI(DistributedCartesianGridAI, DistributedGameAreaAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGAInteriorAI')

    def __init__(self, air, isBuilding=False):
        startingZone = WorldGlobals.GAME_AREA_INTERIOR_STARTING_ZONE if isBuilding else WorldGlobals.GAME_AREA_STARTING_ZONE
        cellWidth = WorldGlobals.GAME_AREA_INTERIOR_CELL_SIZE if isBuilding else WorldGlobals.GAME_AREA_CELL_SIZE
        gridRadius = WorldGlobals.GAME_AREA_INTERIOR_GRID_RADIUS if isBuilding else WorldGlobals.GAME_AREA_GRID_RADIUS
        gridSize = WorldGlobals.GAME_AREA_INTERIOR_GRID_SIZE if isBuilding else WorldGlobals.GAME_AREA_GRID_SIZE

        DistributedCartesianGridAI.__init__(self, air, startingZone, gridSize, gridRadius, cellWidth)
        DistributedGameAreaAI.__init__(self, air)

        self.connectorId = 0

        self.isBuilding = isBuilding
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

    def setIsBuilding(self, isBuilding):
        self.isBuilding = isBuilding

    def getIsBuilding(self):
        return self.isBuilding

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
