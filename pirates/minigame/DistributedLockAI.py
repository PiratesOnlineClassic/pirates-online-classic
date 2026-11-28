from direct.directnotify import DirectNotifyGlobal
from direct.task.TaskManagerGlobal import *
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.uberdog.UberDogGlobals import InventoryType


class DistributedLockAI(DistributedInteractiveAI):
    """
    A lock (treasure chest by default) that is opened by solving the lockpick
    minigame.  Only one pirate may work on the lock at a time; the client
    plays the minigame and tells us when every layer has been picked.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLockAI')
    MULTIUSE = False

    # LockGUI uses difficulty / 10 layers, between 1 and 6 of them.
    MaxDifficulty = 60
    # The quickest a single layer of the lock can realistically be picked.
    MinLayerTime = 0.5
    # Reputation awarded for every layer of a lock that is picked.
    RepPerLayer = 10
    # How long the solver sees the 'Unlocked by' message before getting up.
    SolvedExitDelay = 3.0

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self._open = 0
        self._difficulty = 1
        self._currentUser = None
        self._startTime = 0

    def delete(self):
        taskMgr.remove(self.uniqueName('lock-solved-exit'))
        self._releaseUser()
        DistributedInteractiveAI.delete(self)

    def setDifficulty(self, difficulty):
        # The client only ever opens the lock when the number of layers
        # it calculates (difficulty / 10) is a whole number.
        difficulty = max(1, min(int(difficulty), self.MaxDifficulty))
        if difficulty >= 10:
            difficulty -= difficulty % 10

        self._difficulty = difficulty

    def getDifficulty(self):
        return self._difficulty

    def getNumLayers(self):
        return max(1, self._difficulty // 10)

    def setOpen(self, open):
        self._open = open

    def d_setOpen(self, open):
        self.sendUpdate('setOpen', [open])

    def b_setOpen(self, open):
        self.setOpen(open)
        self.d_setOpen(open)

    def getOpen(self):
        return self._open

    def isOpen(self):
        return bool(self._open)

    def announceGenerate(self):
        DistributedInteractiveAI.announceGenerate(self)
        self.d_setOpen(self._open)

    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------

    def handleRequestInteraction(self, avatar, interactType, instant):
        if self._open or self._currentUser is not None:
            return self.DENY

        return self.ACCEPT

    def handlePostRequestInteraction(self, avatar):
        self._currentUser = avatar
        self._startTime = globalClock.getRealTime()
        self.acceptOnce(avatar.getDeleteEvent(), self._releaseUser)

        # The client builds the lockpick gui with the lock's difficulty;
        # requestSeatResponse(1) would call localAvatarSatDown without it.
        self.d_localAvatarSatDown(avatar.doId)

    def handleRequestExit(self, avatar):
        if self._currentUser != avatar:
            return self.DENY

        taskMgr.remove(self.uniqueName('lock-solved-exit'))
        self._releaseUser()
        self.d_requestSeatResponse(avatar.doId, 2)
        return self.ACCEPT

    def _releaseUser(self):
        if self._currentUser is not None:
            self.ignore(self._currentUser.getDeleteEvent())

        self._currentUser = None
        if self.userId:
            self.b_setUserId(0)

    def d_localAvatarSatDown(self, avatarId):
        self.sendUpdateToAvatarId(avatarId, 'localAvatarSatDown', [avatarId, self._difficulty])

    def d_localAvatarGotUp(self, avatarId):
        self.sendUpdateToAvatarId(avatarId, 'localAvatarGotUp', [])

    def d_requestSeatResponse(self, avatarId, answer):
        self.sendUpdateToAvatarId(avatarId, 'requestSeatResponse', [answer])

    def d_lockSolved(self, avatarId, name):
        # lockSolved is broadcast in the dc, but only the solver has the
        # lockpick gui to show it on.
        self.sendUpdateToAvatarId(avatarId, 'lockSolved', [name])

    # ------------------------------------------------------------------
    # Solving
    # ------------------------------------------------------------------

    def d_openLock(self, name, avId):
        # Client sends this when it solves the lock
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if self._open or avatar != self._currentUser:
            self.air.logPotentialHacker(
                message='Received d_openLock from avatar not picking the lock',
                targetAvId=avatar.doId,
                doId=self.doId)

            return

        elapsed = globalClock.getRealTime() - self._startTime
        if elapsed < self.getNumLayers() * self.MinLayerTime:
            self.air.logPotentialHacker(
                message='Received d_openLock too quickly',
                targetAvId=avatar.doId,
                elapsed=elapsed)

            return

        self.d_lockSolved(avatar.doId, avatar.getName())
        self.b_setOpen(1)
        self.rewardSolver(avatar)
        self.handleLockOpened(avatar)

        taskMgr.doMethodLater(self.SolvedExitDelay, self._solvedExitTask,
            self.uniqueName('lock-solved-exit'), extraArgs=[avatar], appendTask=True)

    def _solvedExitTask(self, avatar, task=None):
        if self._currentUser == avatar:
            self._releaseUser()
            self.d_requestSeatResponse(avatar.doId, 2)

        return task.done if task else None

    def rewardSolver(self, avatar):
        inventory = self.air.inventoryManager.getInventory(avatar.doId)
        if not inventory:
            return

        reputation = inventory.getReputation(InventoryType.LockpickRep)
        inventory.setReputation(InventoryType.LockpickRep,
            reputation + self.RepPerLayer * self.getNumLayers())

    def handleLockOpened(self, avatar):
        messenger.send(self.uniqueName('lockOpened'), [avatar])
