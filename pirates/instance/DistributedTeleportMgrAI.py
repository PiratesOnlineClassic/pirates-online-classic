from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from otp.ai.MagicWordGlobal import *

from pirates.quest.QuestConstants import LocationIds
from pirates.piratesbase import PiratesGlobals
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from pirates.instance.DistributedTeleportZoneAI import DistributedTeleportZoneAI
from pirates.instance.DistributedTeleportHandlerAI import DistributedTeleportHandlerAI
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI


class TeleportFSM(FSM):

    def __init__(self, air, avatar, world, gameArea, spawnPt):
        FSM.__init__(self, 'TeleportFSM')

        self.air = air
        self.avatar = avatar
        self.world = world
        self.gameArea = gameArea
        self.spawnPt = spawnPt

        self.teleportZone = None
        self.teleportHandler = None

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterStart(self):
        self.acceptOnce(self.avatar.getDeleteEvent(), self.__avatarExited)

        self.teleportZone = DistributedTeleportZoneAI(self.air)
        self.teleportZone.generateWithRequired(self.air.allocateZone())

        teleportHandlerDoId = self.air.allocateChannel()
        self.acceptOnce('generate-%d' % teleportHandlerDoId, self.__teleportHandlerCreatedCallback)

        self.teleportHandler = DistributedTeleportHandlerAI(self.air, self.air.teleportMgr, self, self.avatar)
        self.teleportHandler.generateWithRequiredAndId(teleportHandlerDoId, self.air.districtId, self.teleportZone.zoneId)

    def __teleportHandlerCreatedCallback(self, teleportHandler):
        if not teleportHandler:
            self.notify.warning('Failed to generate teleportHandler for avatar %d, while trying to teleport!' % (
                self.avatar.doId))

            self.cleanup()
            return

        self.avatar.d_forceTeleportStart(self.world.getFileName(), self.teleportZone.doId,
            self.teleportHandler.doId, 0, self.teleportZone.parentId, self.teleportZone.zoneId)

    def __avatarExited(self):
        self.cleanup()

    def exitStart(self):
        pass

    def enterStop(self):
        if self.teleportZone:
            self.teleportZone.requestDelete()

        if self.teleportHandler:
            self.teleportHandler.requestDelete()

        del self.air.teleportMgr.avatar2fsm[self.avatar.doId]
        self.ignoreAll()
        self.demand('Off')

    def exitStop(self):
        pass

    def cleanup(self):
        self.demand('Stop')

class DistributedTeleportMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportMgrAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.avatar2fsm = {}

    def getWorld(self, instanceType, instanceName):
        for object in self.air.doId2do.values():
            if not object or not isinstance(object, DistributedInstanceBaseAI):
                continue

            if object.getType() == instanceType and object.getFileName() == instanceName:
                return object

        return None

    def d_initiateTeleport(self, avatar, instanceType=None, instanceName=None, locationUid=None, spawnPt=None):
        if avatar.doId in self.avatar2fsm:
            self.notify.warning('Cannot initiate teleport for avatar %d, already teleporting!' % (
                avatar.doId))

            return

        returnLocation = avatar.getReturnLocation()
        currentIsland = avatar.getCurrentIsland()

        # check to see which island the avatar exited last at,
        # then ensure this is their login teleport; not a normal teleport request...
        if returnLocation and not currentIsland:
            locationUid = returnLocation

        gameArea = avatar.getParentObj()
        if isinstance(gameArea, DistributedGameAreaAI) and gameArea.getUniqueId() == locationUid:
            self.notify.warning('Cannot initiate teleport for %d, already there, locationUid=%s!' % (
                avatar.doId, locationUid))

            return

        if not instanceType and not instanceName:
            world = gameArea.getParentObj()
        else:
            world = self.getWorld(instanceType, instanceName)

        if not world:
            self.notify.warning('Cannot initiate teleport for unknown world: instanceType=%r instanceName=%r' % (
                instanceType, instanceName))

            return

        gameArea = self.air.uidMgr.justGetMeMeObject(locationUid)
        if not gameArea:
            self.notify.warning('Cannot initiate teleport for unknown gameArea: locationUid=%r' % (
                locationUid))

            return

        if not spawnPt:
            spawnPt = world.getSpawnPt(gameArea.getUniqueId())

        if not spawnPt:
            self.notify.warning('Cannot initiate teleport for avatar %d, no available spawn points for gameArea, '
                'locationUid=%r!' % (avatar.doId, locationUid))

            return

        self.avatar2fsm[avatar.doId] = TeleportFSM(self.air, avatar, world, gameArea, spawnPt)
        self.avatar2fsm[avatar.doId].request('Start')

    def initiateTeleport(self, instanceType, fromInstanceType, shardId, locationUid, instanceDoId, instanceName, gameType, friendDoId, friendAreaDoId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        if shardId and shardId != self.air.districtId:
            self.air.travelAgent.d_requestTeleportToShardAItoUD(avatar.doId, shardId, instanceType,
                instanceName, locationUid)

            return

        self.d_initiateTeleport(avatar, instanceType, instanceName, locationUid)

    def requestTeleportToIsland(self, locationUid):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        self.d_initiateTeleport(avatar, locationUid=locationUid)

    def d_teleportHasBegun(self, avatarId, instanceType, fromInstanceType, instanceName, gameType):
        self.sendUpdateToAvatarId(avatarId, 'teleportHasBegun', [instanceType, fromInstanceType,
            instanceName, gameType])

    def d_localTeleportToIdResponse(self, avatarId, parentId, zoneId):
        self.sendUpdateToAvatarId(avatarId, '_localTeleportToIdResponse', [parentId, zoneId])

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def areaTeleport(areaUid):
    simbase.air.teleportMgr.d_initiateTeleport(spellbook.getTarget(),
        locationUid=areaUid)

    return "Teleporting to area: %s." % areaUid
