from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI


class DistributedLockAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLockAI')
    MULTIUSE = False

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self._open = 0
        self._difficulty = 1
        self._currentUser = None

    def setDifficulty(self, difficulty):
        self._difficulty = difficulty

    def getDifficulty(self):
        return self._difficulty

    def announceGenerate(self):
        DistributedInteractiveAI.announceGenerate(self)
        self.sendUpdate('setOpen', [self._open])

    def handleRequestInteraction(self, avatar, interactType, instant):
        if self._open:
            return self.DENY

        self._currentUser = avatar
        # Tell the client it sat down with the difficulty level
        self.sendUpdateToAvatarId(avatar.doId, 'localAvatarSatDown',
            [avatar.doId, self._difficulty])
        self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [1])
        return self.ACCEPT

    def handleRequestExit(self, avatar):
        if self._currentUser == avatar:
            self._currentUser = None

        self.sendUpdateToAvatarId(avatar.doId, 'requestSeatResponse', [2])
        return self.ACCEPT

    def d_openLock(self, name, avId):
        # Client sends this when it solves the lock
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        self.sendUpdate('lockSolved', [name])
        self._open = 1
        self.sendUpdate('setOpen', [1])

        if self._currentUser:
            self.sendUpdateToAvatarId(self._currentUser.doId,
                'localAvatarGotUp', [])
            self._currentUser = None

    def setOpen(self, open):
        self._open = open

    def getOpen(self):
        return self._open
