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

        # get the cell origin zone relative to the spawn island's spawn position,
        # that was retrieved from the instance world.
        zoneId = island.getZoneFromXYZ((xPos, yPos, zPos))

        # ensure the zoneId we've just calculated is indeed valid,
        # and not some random zone outside the cartesian grid...
        if not island.isValidZone(zoneId):
            self.notify.warning('Cannot finish teleport for avatar %d, invalid spawn zone %d!' % (
                avatar.doId, zoneId))

            return

        # set the avatar's location relative to the spawn point's cell,
        # this way the avatar will be visible within the cartesian grid.
        self.avatar.b_setLocation(island.doId, zoneId)
        self.avatar.reparentTo(island)

    def teleportToInstanceFinal(self, avatarId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        avatar.b_setTeleportFlag(PiratesGlobals.TFIgnore)

        # the avatar has arrived at the location and is now finished
        # teleporting, let's set their game state so they spawn in correctly.
        self.avatar.b_setGameState('Spawn')

        # remove the teleport fsm object from the teleport manager so
        # the avatar can teleport elsewhere in the future.
        self.teleportFsm.request('Stop')
