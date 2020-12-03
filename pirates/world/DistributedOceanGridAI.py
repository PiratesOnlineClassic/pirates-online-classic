from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.directnotify import DirectNotifyGlobal

from pirates.world.OceanGridBase import OceanGridBase
from pirates.world import WorldGlobals
from pirates.movement.DistributedMovingObjectAI import DistributedMovingObjectAI


class DistributedOceanGridAI(DistributedCartesianGridAI, OceanGridBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedOceanGridAI')

    def __init__(self, air):
        startingZone = WorldGlobals.OCEAN_GRID_STARTING_ZONE
        gridSize = WorldGlobals.OCEAN_GRID_SIZE
        gridRadius = WorldGlobals.OCEAN_GRID_RADIUS
        cellWidth = WorldGlobals.OCEAN_CELL_SIZE

        DistributedCartesianGridAI.__init__(self, air, startingZone, gridSize, gridRadius, cellWidth)
        OceanGridBase.__init__(self)

    def addObjectToOceanGrid(self, av):
        assert(av is not None)
        self.addObjectToGrid(av)

    def removeObjectFromOceanGrid(self, av):
        assert(av is not None)
        self.removeObjectFromGrid(av)

    #def handleChildArrive(self, childObj, zoneId):
    #    if isinstance(childObj, DistributedMovingObjectAI):
    #        self.addObjectToOceanGrid(childObj)
    #
    #    DistributedNodeAI.handleChildArrive(self, childObj, zoneId)

    def handleChildLeave(self, childObj, zoneId):
        if isinstance(childObj, DistributedMovingObjectAI):
            self.removeObjectFromOceanGrid(childObj)

        DistributedCartesianGridAI.handleChildLeave(self, childObj, zoneId)

    def generateChildWithRequired(self, do, zoneId, optionalFields=[]):
        self.generateChildWithRequiredAndId(do, self.air.allocateChannel(), self.doId, zoneId, optionalFields)

    def generateChildWithRequiredAndId(self, do, doId, parentId, zoneId, optionalFields=[]):
        do.generateWithRequiredAndId(doId, parentId, zoneId, optionalFields)
