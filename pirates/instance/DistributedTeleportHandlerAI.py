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
        self.sendUpdateToAvatarId(self.avatar.doId, 'waitInTZ', [[], 0])

    def _getDestinationInstance(self):
        gameArea = self.teleportFsm.gameArea
        instance = gameArea.getParentObj()
        if not instance:
            self.notify.warning('Cannot teleport avatar %d: destination area %d has no instance' %
                (self.avatar.doId, gameArea.doId))
            self.d_abortTeleport()
            self.teleportFsm.cleanup()
        return instance

    def teleportToInstanceReady(self, zoneId):
        world = self.teleportFsm.world
        gameArea = self.teleportFsm.gameArea
        destination = self._getDestinationInstance()
        if not destination:
            return

        self.sendUpdateToAvatarId(self.avatar.doId, 'continueTeleportToInstance', [world.doId,
            world.oceanGrid.zoneId, world.doId, world.getFileName(), gameArea.parentId, gameArea.zoneId,
            destination.doId, destination.getFileName(), world.oceanGrid.doId])

    def readyToFinishTeleport(self, instanceDoId):
        gameArea = self.teleportFsm.gameArea
        destination = self._getDestinationInstance()
        if not destination:
            return
        xPos, yPos, zPos, h = self.teleportFsm.spawnPt

        # ensure the zoneId we've just calculated is indeed valid,
        # and not some random zone outside the cartesian grid...
        zoneId = gameArea.getZoneFromXYZ((xPos, yPos, zPos))
        if not gameArea.isValidZone(zoneId):
            self.notify.warning('Cannot finish teleport for avatar %d, '
                'invalid spawn zone %d!' % (self.avatar.doId, zoneId))

            self.d_abortTeleport()
            self.teleportFsm.cleanup()
            return

        destination.d_setSpawnInfo(self.avatar.doId, xPos, yPos, zPos, h, 0, [gameArea.doId,
            gameArea.zoneId, gameArea.parentId])

        self.sendUpdateToAvatarId(self.avatar.doId, 'teleportToInstanceCleanup', [])

    def teleportToInstanceFinal(self, avatarId):
        self.avatar.b_setGameState('Spawn')
        self.teleportFsm.cleanup()
        messenger.send('teleportDone-%d' % self.avatar.doId)

    def continueTeleportToTZ(self):
        """
        Called by the client to continue the teleport process after entering the teleport zone.
        The client may call this if it needs to signal readiness to proceed.
        """
        # The teleport process is already ongoing, this is just an acknowledgment
        # that the client is ready in the TZ. In most cases, the flow continues
        # automatically via waitInTZ, so this is a no-op unless we need to handle
        # specific timing issues.
        pass

    def avatarLeft(self):
        """
        Called by the client when the avatar leaves during teleport (e.g., teleport aborted).
        This should clean up the teleport FSM and associated objects.
        """
        self.notify.debug('Avatar %d left during teleport, cleaning up...' % self.avatar.doId)
        self.teleportFsm.cleanup()

    def d_abortTeleport(self):
        """
        Send abort teleport message to the client. Called when the AI needs to cancel
        the teleport process due to an error or invalid state.
        """
        self.sendUpdateToAvatarId(self.avatar.doId, 'abortTeleport', [])
