from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from pirates.world import WorldGlobals


class DistributedLocationManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLocationManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def getLocationCategories(self, avatar):
        from pirates.world.DistributedOceanGridAI import DistributedOceanGridAI
        from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
        from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
        from pirates.world.DistributedIslandAI import DistributedIslandAI
        from pirates.ship.DistributedShipAI import DistributedShipAI

        parentObj = avatar.getParentObj()
        categories = []
        if isinstance(parentObj, DistributedOceanGridAI):
            categories.append(WorldGlobals.OCEAN)

        if isinstance(parentObj, DistributedShipAI):
            categories.append(WorldGlobals.SHIP)

        if isinstance(parentObj, DistributedGameAreaAI):
            categories.append(WorldGlobals.GAMEAREA)

        if isinstance(parentObj, DistributedIslandAI):
            categories.append(WorldGlobals.ISLAND)

        if isinstance(parentObj, DistributedGAInteriorAI):
            categories.append(WorldGlobals.BUILDING)

        return categories

    def requestLocation(self, category):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        self.d_locationResponse(avatar.doId, int(category in self.getLocationCategories(avatar)))

    def d_locationResponse(self, avatarId, response):
        self.sendUpdateToAvatarId(avatarId, 'locationResponse', [response])
