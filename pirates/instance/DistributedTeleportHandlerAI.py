from panda3d.core import *
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
            self.teleportFsm.cleanup()
            return

        self.sendUpdateToAvatarId(self.avatar.doId, 'waitInTZ', [[], 0])

    def teleportToInstanceReady(self, zoneId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.teleportFsm.cleanup()
            return

        world = self.teleportFsm.world
        island = self.teleportFsm.island

        self.sendUpdateToAvatarId(self.avatar.doId, 'continueTeleportToInstance', [world.parentId,
            world.zoneId, world.doId, world.getFileName(), world.doId, island.zoneId,
            island.doId, world.getFileName(), world.oceanGrid.doId])

    def readyToFinishTeleport(self, instanceDoId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.teleportFsm.cleanup()
            return

        world = self.teleportFsm.world
        island = self.teleportFsm.island
        xPos, yPos, zPos, h = self.teleportFsm.spawnPt

        # get the cell origin zone relative to the spawn island's spawn position,
        # that was retrieved from the instance world.
        zoneId = island.getZoneFromXYZ((xPos, yPos, zPos))

        # ensure the zoneId we've just calculated is indeed valid,
        # and not some random zone outside the cartesian grid...
        if not island.isValidZone(zoneId):
            self.notify.warning('Cannot finish teleport for avatar %d, invalid spawn zone %d!' % (
                avatar.doId, zoneId))

            self.teleportFsm.cleanup()
            return

        world.d_setSpawnInfo(self.avatar.doId, xPos, yPos, zPos, h, 0, [island.doId,
            island.parentId, island.zoneId])

        self.sendUpdateToAvatarId(self.avatar.doId, 'teleportToInstanceCleanup', [])

    def teleportToInstanceFinal(self, avatarId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.teleportFsm.cleanup()
            return

        self.avatar.b_setGameState('Spawn')
        messenger.send('teleportDone-%d' % self.avatar.doId)
        self.teleportFsm.cleanup()
