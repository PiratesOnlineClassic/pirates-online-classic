from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal

from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI


class DistributedGAConnectorAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGAConnectorAI')

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)

        self.modelPath = ''
        self.links = [False, '', []]
        self.uniqueId = ''
        self.name = ''
        self.nodeName = ''
        self.otherLinkUid = ''

    def getParentingRules(self):
        return ['', '']

    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def d_setModelPath(self, modelPath):
        self.sendUpdate('setModelPath', [modelPath])

    def b_setModelPath(self, modelPath):
        self.setModelPath(modelPath)
        self.d_setModelPath(modelPath)

    def getModelPath(self):
        return self.modelPath

    def setLinks(self, isExterior, exteriorUid, links):
        self.links = [isExterior, exteriorUid, links]

    def d_setLinks(self, isExterior, exteriorUid, links):
        self.sendUpdate('setLinks', [isExterior, exteriorUid, links])

    def b_setLinks(self, isExterior, exteriorUid, links):
        self.setLinks(isExterior, exteriorUid, links)
        self.d_setLinks(isExterior, exteriorUid, links)

    def getLinks(self):
        return self.links

    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def d_setUniqueId(self, uniqueId):
        self.sendUpdate('setUniqueId', [uniqueId])

    def b_setUniqueId(self, uniqueId):
        self.setUniqueId(uniqueId)
        self.d_setUniqueId(uniqueId)

    def getUniqueId(self):
        return self.uniqueId

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setNodeName(self, nodeName):
        self.nodeName = nodeName

    def getNodeName(self):
        return self.nodeName

    def setOtherLinkUid(self, otherLinkUid):
        self.otherLinkUid = otherLinkUid

    def getOtherLinkUid(self):
        return self.otherLinkUid

    def requestPrivateArea(self, areaDoId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        area = self.air.doId2do.get(areaDoId)
        if not area:
            self.notify.warning('Cannot handle request private area for avatar: %d, '
                'unknown area with doId: %d!' % (avatar.doId, areaDoId))

            return

        if not isinstance(area, DistributedGameAreaAI):
            return

        # only the game areas this connector links together may be requested
        linkedAreaIds = [link[1] for link in self.links[2]]
        if area.doId not in linkedAreaIds:
            self.air.logPotentialHacker(message='Requested a private area the connector does not link to!',
                targetAvId=avatar.doId, connectorId=self.doId, areaDoId=areaDoId)

            return

        areaWorld = area.getParentObj()
        if not areaWorld:
            return

        if not isinstance(areaWorld, DistributedInstanceBaseAI):
            return

        # the avatar arrives in the requested area at the connector that lays within it,
        # which is usually the connector on the other side of the tunnel, unless the avatar
        # turned around and is heading back into the area it came from...
        if area is self.getParentObj():
            areaConnector = self
        else:
            areaConnector = self.air.uidMgr.justGetMeMeObject(self.otherLinkUid)

        if not areaConnector:
            self.notify.warning('Cannot handle request private area for avatar: %d, '
                'unknown other side connector with uid: %s' % (avatar.doId, self.otherLinkUid))

            return

        def _connectorInterestCallback():
            self.d_setPrivateArea(avatar.doId, areaWorld.doId, area.zoneId, area.doId, True)

        self.air.worldGridManager.handleLocationChanged(areaConnector.getParentObj(), avatar,
            areaConnector.zoneId, _connectorInterestCallback)

    def setPrivateArea(self, worldId, worldZoneId, areaDoId, autoFadeIn):
        # the private area is only ever assigned by the AI in response to requestPrivateArea,
        # a client should never be sending this field to us...
        self.air.logPotentialHacker(message='Received setPrivateArea from a client!',
            connectorId=self.doId)

    def d_setPrivateArea(self, avatarId, worldId, worldZoneId, areaDoId, autoFadeIn):
        self.sendUpdateToAvatarId(avatarId, 'setPrivateArea', [worldId, worldZoneId, areaDoId, autoFadeIn])
