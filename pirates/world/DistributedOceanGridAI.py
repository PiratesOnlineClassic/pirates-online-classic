from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.directnotify import DirectNotifyGlobal

from pirates.world.OceanGridBase import OceanGridBase
from pirates.world import WorldGlobals


class DistributedOceanGridAI(DistributedCartesianGridAI, OceanGridBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedOceanGridAI')

    def __init__(self, air):
        startingZone = WorldGlobals.OCEAN_GRID_STARTING_ZONE
        gridSize = WorldGlobals.OCEAN_GRID_SIZE
        gridRadius = WorldGlobals.OCEAN_GRID_RADIUS
        cellWidth = WorldGlobals.OCEAN_CELL_SIZE

        DistributedCartesianGridAI.__init__(self, air, startingZone, gridSize, gridRadius, cellWidth)
        OceanGridBase.__init__(self)

    def generateChildWithRequired(self, do, zoneId, optionalFields=[]):
        self.generateChildWithRequiredAndId(do, self.air.allocateChannel(), self.doId, zoneId, optionalFields)

    def generateChildWithRequiredAndId(self, do, doId, parentId, zoneId, optionalFields=[]):
        do.generateWithRequiredAndId(doId, parentId, zoneId, optionalFields)
