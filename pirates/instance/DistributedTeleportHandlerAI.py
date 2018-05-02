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

        # set the avatar's location under the island object so the island
        # will load and the avatar will be present on the cartesian grid.
        self.avatar.b_setLocation(island.doId, PiratesGlobals.IslandLocalZone)

    def teleportToInstanceFinal(self, avatarId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        # the avatar has arrived at the location and is now finished
        # teleporting, let's set their game state so they spawn in correctly.
        self.avatar.b_setGameState('Spawn')

        # remove the teleport fsm object from the teleport manager so
        # the avatar can teleport elsewhere in the future.
        self.teleportFsm.request('Stop')
