from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.directnotify import DirectNotifyGlobal

from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.world import WorldGlobals


class DistributedTownAI(DistributedCartesianGridAI, DistributedGameAreaAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTownAI')

    def __init__(self, air):
        DistributedCartesianGridAI.__init__(self, air, WorldGlobals.GAME_AREA_STARTING_ZONE,
            WorldGlobals.GAME_AREA_GRID_SIZE, WorldGlobals.GAME_AREA_GRID_RADIUS,
            WorldGlobals.GAME_AREA_CELL_SIZE)

        DistributedGameAreaAI.__init__(self, air)

    def delete(self):
        DistributedCartesianGridAI.delete(self)
        DistributedGameAreaAI.delete(self)
