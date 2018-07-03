from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.directnotify import DirectNotifyGlobal
from pirates.world.OceanGridBase import OceanGridBase
from pirates.world.WorldGlobals import *
from pirates.piratesbase.UniqueIdManager import UniqueIdManager

class DistributedOceanGridAI(DistributedCartesianGridAI, OceanGridBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedOceanGridAI')

    def __init__(self, air):
        DistributedCartesianGridAI.__init__(self, air, OCEAN_GRID_STARTING_ZONE, OCEAN_GRID_SIZE,
            OCEAN_GRID_RADIUS, OCEAN_CELL_SIZE)

        OceanGridBase.__init__(self)

        self.uidMgr = UniqueIdManager(self.air)

    def generateChildWithRequired(self, do, zoneId, optionalFields=[]):
        self.generateChildWithRequiredAndId(do, self.air.allocateChannel(), self.doId, zoneId, optionalFields)

    def generateChildWithRequiredAndId(self, do, doId, parentId, zoneId, optionalFields=[]):
        do.generateWithRequiredAndId(doId, parentId, zoneId, optionalFields)
