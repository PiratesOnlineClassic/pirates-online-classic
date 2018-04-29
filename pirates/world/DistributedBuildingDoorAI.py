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

    def handleRequestInteraction(self, avatar, interactType, instant):
        result = DistributedDoorBaseAI.handleRequestInteraction(self, avatar,
            interactType, instant)

        if not result:
            return self.DENY

        interior = self.air.doId2do.get(self.interiorDoId)

        if not interior:
            self.notify.warning('Cannot handle avatar %d interact for door %d, interior %d not found!' % (
                avatar.doId, self.doId, self.interiorDoId))

            return self.DENY

        interiorDoor = interior.getInteriorFrontDoor()

        if not interiorDoor:
            self.notify.warning('Cannot handle avatar %d interact for door %d, interior door not found!' % (
                avatar.doId, self.doId))

            return self.DENY

        avatar.b_setLocation(interior.doId, interiorDoor.zoneId)
        return self.ACCEPT

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

    def requestPrivateInteriorInstance(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        self.sendUpdateToAvatarId(avatar.doId, 'setPrivateInteriorInstance', [self.interiorWorldParentId,
            self.interiorWorldZoneId, self.interiorDoId, True])
