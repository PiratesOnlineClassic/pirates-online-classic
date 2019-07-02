from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta

from pirates.world.DistributedDoorBaseAI import DistributedDoorBaseAI
from pirates.piratesbase import PiratesGlobals


class DistributedBuildingDoorAI(DistributedDoorBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuildingDoorAI')

    def __init__(self, air):
        DistributedDoorBaseAI.__init__(self, air)

        self.interiorDoId = 0
        self.interiorUid = ''
        self.interiorWorldParentId = 0
        self.interiorWorldZoneId = 0

    def setInteriorId(self, interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId):
        self.interiorDoId = interiorDoId
        self.interiorUid = interiorUid
        self.interiorWorldParentId = interiorWorldParentId
        self.interiorWorldZoneId = interiorWorldZoneId

    def d_setInteriorId(self, interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId):
        self.sendUpdate('setInteriorId', [interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId])

    def b_setInteriorId(self, interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId):
        self.setInteriorId(interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId)
        self.d_setInteriorId(interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId)

    def getInteriorId(self):
        return [self.interiorDoId, self.interiorUid, self.interiorWorldParentId, self.interiorWorldZoneId]

    def handleRequestInteraction(self, avatar, interactType, instant):
        result = DistributedDoorBaseAI.handleRequestInteraction(self, avatar, interactType, instant)
        if not result:
            return self.DENY

        interior = self.air.doId2do.get(self.interiorDoId)
        if not interior:
            self.notify.warning('Cannot handle avatar %d interact for door %d, '
                'interior %d not found!' % (avatar.doId, self.doId, self.interiorDoId))

            return self.DENY

        if not self.otherDoor:
            self.notify.warning('Cannot handle avatar %d interact for door %d, '
                'interior door not found!' % (avatar.doId, self.doId))

            return self.DENY

        return self.ACCEPT

    def requestPrivateInteriorInstance(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        interior = self.air.doId2do.get(self.interiorDoId)
        if not interior:
            self.notify.warning('Cannot set interior instance %d interact for door %d, '
                'interior %d not found!' % (avatar.doId, self.doId, self.interiorDoId))

            return

        interiorDoor = interior.getInteriorFrontDoor()
        if not interiorDoor:
            self.notify.warning('Cannot set interior instance %d interact for door %d, '
                'interior door not found!' % (avatar.doId, self.doId))

            return

        self.d_setPrivateInteriorInstance(avatar.doId, interior.parentId, interior.zoneId, interior.doId)

    def d_setPrivateInteriorInstance(self, avatarId, worldId, worldZoneId, interiorId, autoFadeIn=True):
        self.sendUpdateToAvatarId(avatarId, 'setPrivateInteriorInstance', [worldId, worldZoneId, interiorId, autoFadeIn])
