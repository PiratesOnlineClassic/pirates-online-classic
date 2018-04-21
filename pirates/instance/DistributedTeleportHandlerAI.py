from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals

class DistributedTeleportHandlerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportHandlerAI')

    def __init__(self, air, teleportMgr, teleportFsm, avatar):
        DistributedObjectAI.__init__(self, air)

        self.teleportMgr = teleportMgr
        self.teleportFsm = teleportFsm
        self.avatar = avatar

    def startTeleportProcess(self, parentId, zoneId, bandId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        self.sendUpdateToAvatarId(self.avatar.doId, 'waitInTZ', [[], 0])

    def teleportToInstanceReady(self, zoneId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        world = self.teleportFsm.world
        island = self.teleportFsm.island

        self.sendUpdateToAvatarId(self.avatar.doId, 'continueTeleportToInstance', [world.parentId,
            world.zoneId, world.doId, world.getFileName(),
            world.doId, island.zoneId, island.doId, world.getFileName(), world.oceanGrid.doId])

    def readyToFinishTeleport(self, instanceDoId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        world = self.teleportFsm.world
        island = self.teleportFsm.island
        xPos, yPos, zPos, h = self.teleportFsm.spawnPt

        world.d_setSpawnInfo(self.avatar.doId, xPos, yPos, zPos, h, 0, [island.doId,
            island.parentId, island.zoneId])

        self.sendUpdateToAvatarId(self.avatar.doId, 'teleportToInstanceCleanup', [])

        # send the avatar under the island cartesian grid object, then
        # set relative position to that of the island's node...
        self.avatar.reparentTo(island)
        self.avatar.b_setLocation(island.doId, PiratesGlobals.IslandLocalZone)

    def teleportToInstanceFinal(self, avatarId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        self.teleportFsm.request('Stop')
