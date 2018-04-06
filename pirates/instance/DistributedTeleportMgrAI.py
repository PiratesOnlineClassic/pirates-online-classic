from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.quest.QuestConstants import LocationIds
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from direct.fsm.FSM import FSM
from pirates.instance.DistributedTeleportZoneAI import DistributedTeleportZoneAI
from pirates.instance.DistributedTeleportHandlerAI import DistributedTeleportHandlerAI

class TeleportFSM(FSM):

    def __init__(self, teleportMgr, avatar, world, island, spawnPt):
        FSM.__init__(self, 'TeleportFSM')

        self.teleportMgr = teleportMgr
        self.avatar = avatar
        self.world = world
        self.island = island
        self.spawnPt = spawnPt

        self.teleportZone = None
        self.teleportHandler = None

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterStart(self):
        self.acceptOnce(self.avatar.getDeleteEvent(), lambda: self.demand('Stop'))

        self.teleportZone = DistributedTeleportZoneAI(self.teleportMgr.air)
        self.teleportZone.generateWithRequired(self.teleportMgr.air.allocateZone())

        def teleportHandlerReady(teleportHandler):
            if not teleportHandler:
                self.notify.warning('Failed to generate teleportHandler %d, for avatar %d, while trying to teleport!' % (
                    self.teleportHandler.doId, self.avatar.doId))

                self.demand('Stop')
                return

            self.avatar.d_forceTeleportStart(self.world.getFileName(), self.teleportZone.doId, self.teleportHandler.doId, 0,
                self.teleportZone.parentId, self.teleportZone.zoneId)

        teleportHandlerDoId = self.teleportMgr.air.allocateChannel()
        self.acceptOnce('generate-%d' % teleportHandlerDoId, teleportHandlerReady)

        self.teleportHandler = DistributedTeleportHandlerAI(self.teleportMgr.air, self.teleportMgr, self, self.avatar)
        self.teleportHandler.generateWithRequiredAndId(teleportHandlerDoId, self.teleportMgr.air.districtId, self.teleportZone.zoneId)

    def exitStart(self):
        pass

    def enterStop(self):
        self.teleportZone.requestDelete()
        self.teleportHandler.requestDelete()

        del self.teleportMgr.avatar2fsm[self.avatar.doId]

        self.ignoreAll()
        self.demand('Off')

    def exitStop(self):
        pass

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

    def d_initiateTeleport(self, avatar, instanceType=None, instanceName=None, locationUid=LocationIds.PORT_ROYAL_ISLAND, spawnPt=None):
        if avatar.doId in self.avatar2fsm:
            self.notify.warning('Cannot initiate teleport for avatar %d, already teleporting!' % (
                avatar.doId))

            return

        island = avatar.getParentObj()

        if island is not None and island.getUniqueId() == locationUid:
            self.notify.debug('Cannot initiate teleport for %d, already there, locationUid=%s!' % (
                avatar.doId, locationUid))

            return

        if not instanceType and not instanceName:
            world = island.getParentObj()
        else:
            world = self.getWorld(instanceType, instanceName)

        if not world:
            self.notify.warning('Cannot initiate teleport for unknown world: instanceType=%d instanceName=%s' % (
                instanceType, instanceName))

            return

        island = world.uidMgr.justGetMeMeObject(locationUid)

        if not island:
            self.notify.warning('Cannot initiate teleport for unknown island: locationUid=%s' % (
                locationUid))

            return

        if not spawnPt:
            spawnPt = world.getSpawnPt(island.getUniqueId())

        if not spawnPt:
            self.notify.warning('Cannot initiate teleport for avatar %d, no available spawn points for island, locationUid=%s!' % \
                avatar.doId, locationUid)

            return

        self.avatar2fsm[avatar.doId] = TeleportFSM(self, avatar, world, island, spawnPt)
        self.avatar2fsm[avatar.doId].request('Start')

    def initiateTeleport(self, instanceType, fromInstanceType, shardId, locationUid, instanceDoId, instanceName, gameType, friendDoId, friendAreaDoId):
        if simbase.config.GetBool('force-teleport-pr', True):
            locationUid = LocationIds.PORT_ROYAL_ISLAND

        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.notify.warning('Cannot initiate teleport for unknown avatar!')
            return

        self.d_initiateTeleport(avatar, instanceType, instanceName, locationUid)

    def requestTeleportToIsland(self, locationUid):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.notify.warning('Cannot initiate teleport for unknown avatar!')
            return

        self.d_initiateTeleport(avatar, locationUid=locationUid)

    def d_teleportHasBegun(self, avatarId, instanceType, fromInstanceType, instanceName, gameType):
        self.sendUpdateToAvatarId(avatarId, 'teleportHasBegun', [instanceType, fromInstanceType, instanceName, gameType])
