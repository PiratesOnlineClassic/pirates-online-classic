from direct.directnotify import DirectNotifyGlobal

from pirates.battle.DistributedPCCannonAI import DistributedPCCannonAI
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PiratesGlobals


class DistributedIslandCannonAI(DistributedPCCannonAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedIslandCannonAI')

    def __init__(self, air):
        DistributedPCCannonAI.__init__(self, air)

        self.cannonIndex = 0
        self.islandId = 0
        self.isDestructable = 0
        self.destructState = PiratesGlobals.CANNON_STATE_NORMAL
        self.repairTime = config.GetFloat('island-cannon-repair-time', 60.0)

    def delete(self):
        taskMgr.remove(self.uniqueName('repairCannon'))
        if self.userId:
            self.ignore(self.air.getAvatarExitEvent(self.userId))

        DistributedPCCannonAI.delete(self)

    # =========================================================================
    # DC Fields
    # =========================================================================

    def setCannonIndex(self, cannonIndex):
        self.cannonIndex = cannonIndex

    def d_setCannonIndex(self, cannonIndex):
        self.sendUpdate('setCannonIndex', [cannonIndex])

    def b_setCannonIndex(self, cannonIndex):
        self.setCannonIndex(cannonIndex)
        self.d_setCannonIndex(cannonIndex)

    def getCannonIndex(self):
        return self.cannonIndex

    def setIslandId(self, islandId):
        self.islandId = islandId

    def d_setIslandId(self, islandId):
        self.sendUpdate('setIslandId', [islandId])

    def b_setIslandId(self, islandId):
        self.setIslandId(islandId)
        self.d_setIslandId(islandId)

    def getIslandId(self):
        return self.islandId

    def setIsDestructable(self, isDestructable):
        self.isDestructable = isDestructable

    def d_setIsDestructable(self, isDestructable):
        self.sendUpdate('setIsDestructable', [isDestructable])

    def b_setIsDestructable(self, isDestructable):
        self.setIsDestructable(isDestructable)
        self.d_setIsDestructable(isDestructable)

    def getIsDestructable(self):
        return self.isDestructable

    def setDestructState(self, destructState):
        self.destructState = destructState

    def d_setDestructState(self, destructState):
        self.sendUpdate('setDestructState', [destructState])

    def b_setDestructState(self, destructState):
        self.setDestructState(destructState)
        self.d_setDestructState(destructState)

    def getDestructState(self):
        return self.destructState

    def isDestroyed(self):
        return self.destructState == PiratesGlobals.CANNON_STATE_DESTRUCT

    # =========================================================================
    # Interaction
    # =========================================================================

    def handleRequestInteraction(self, avatar, interactType, instant):
        if self.isDestroyed():
            return self.DENY

        if self.userId and self.userId != avatar.doId:
            return self.DENY

        self.acceptOnce(self.air.getAvatarExitEvent(avatar.doId), self._handleUserExit, extraArgs=[avatar.doId])
        self.startWeapon(avatar.doId)
        return self.ACCEPT

    def handleRequestExit(self, avatar):
        if avatar.doId != self.userId:
            return self.DENY

        self.ignore(self.air.getAvatarExitEvent(avatar.doId))
        self.stopWeapon(avatar.doId)
        return self.ACCEPT

    def demandExit(self):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId and avatarId == self.userId:
            self.ignore(self.air.getAvatarExitEvent(avatarId))
            self.stopWeapon(avatarId)

        DistributedPCCannonAI.demandExit(self)

    def _handleUserExit(self, avatarId):
        if avatarId != self.userId:
            return

        # the avatar left the district while using the cannon, free it up for the next pirate:
        self.setMovie(WeaponGlobals.WEAPON_MOVIE_CLEAR, 0)
        self.b_setUserId(0)

    def ejectUser(self):
        if not self.userId:
            return

        avatarId = self.userId
        self.ignore(self.air.getAvatarExitEvent(avatarId))
        self.stopWeapon(avatarId)
        self.b_setUserId(0)

    # =========================================================================
    # Destruction
    # =========================================================================

    def hitByProjectile(self):
        avatarId = self.air.getAvatarIdFromSender()
        if not self.air.doId2do.get(avatarId):
            return

        if not self.isDestructable:
            self.air.logPotentialHacker(
                message='Received hitByProjectile for an indestructable island cannon',
                targetAvId=avatarId,
                cannonId=self.doId)

            return

        if self.isDestroyed():
            return

        self.destroyCannon()

    def destroyCannon(self, repair=True):
        self.notify.debug('Cannon %d on island %d destroyed' % (self.doId, self.islandId))
        self.ejectUser()
        self.b_setDestructState(PiratesGlobals.CANNON_STATE_DESTRUCT)

        taskMgr.remove(self.uniqueName('repairCannon'))
        if repair and self.repairTime > 0:
            taskMgr.doMethodLater(self.repairTime, self._repairCannonTask, self.uniqueName('repairCannon'))

    def _repairCannonTask(self, task):
        self.repairCannon()
        return task.done

    def repairCannon(self):
        taskMgr.remove(self.uniqueName('repairCannon'))
        if not self.isDestroyed():
            return

        self.notify.debug('Cannon %d on island %d repaired' % (self.doId, self.islandId))
        self.b_setDestructState(PiratesGlobals.CANNON_STATE_NORMAL)
