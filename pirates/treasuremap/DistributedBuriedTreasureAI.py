from direct.directnotify import DirectNotifyGlobal
from direct.task.TaskManagerGlobal import taskMgr
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI

class DistributedBuriedTreasureAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuriedTreasureAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.startingDepth = 0
        self.currentDepth = 0
        self.currentUser = None
        self.treasureAvailable = None
        self.digging = False

    def delete(self):
        self._removeDigTasks()
        if self.digging and self.currentUser in self.air.doId2do:
            self.d_stopDigging(self.currentUser, 1)
        self.digging = False
        self.treasureAvailable = False
        self.currentUser = None
        DistributedInteractiveAI.delete(self)

    def handleRequestInteraction(self, avatar, interactType, instant):
        if self.currentUser is not None:
            return self.DENY

        self.currentUser = avatar.doId
        return self.ACCEPT

    def handlePostRequestInteraction(self, avatar):
        self.digging = True
        self.d_startDigging(avatar.doId)
        taskMgr.doMethodLater(1, self.performChestDig, self.uniqueName('digTask'))

    def performChestDig(self, task):
        avatarId = self.currentUser
        if not self.digging or avatarId is None:
            return task.done
        if avatarId not in self.air.doId2do:
            self._resetDigSpot()
            return task.done

        self.b_setCurrentDepth(max(self.getCurrentDepth() - 1, 0))
        if self.currentDepth <= 0:
            self.digging = False
            avatar = self.air.doId2do[avatarId]
            try:
                progress = self.air.questMgr.finishBuriedTreasure(avatar, self)
            except Exception:
                self.d_stopDigging(avatarId, 1)
                self._resetDigSpot()
                raise
            self.d_stopDigging(avatarId, progress)
            self.d_showTreasure(avatarId)
            taskMgr.doMethodLater(5, self.resetDigSpot, self.uniqueName('digResetTask'))
            return task.done

        return task.again

    def handleRequestExit(self, avatar):
        if avatar.doId != self.currentUser:
            return self.DENY
        self._resetDigSpot(clearUserId=False)
        return self.ACCEPT

    def demandExit(self):
        avatarId = self.air.getAvatarIdFromSender()
        if self.digging and avatarId == self.currentUser:
            self.d_stopDigging(avatarId, 1)
        self.requestExit()

    def _removeDigTasks(self):
        taskMgr.remove(self.uniqueName('digTask'))
        taskMgr.remove(self.uniqueName('digResetTask'))

    def _resetDigSpot(self, clearUserId=True):
        self._removeDigTasks()
        self.digging = False
        self.currentUser = None
        self.b_setCurrentDepth(self.getStartingDepth())
        if clearUserId and self.userId:
            self.b_setUserId(0)

    def resetDigSpot(self, task):
        self._resetDigSpot()
        return task.done

    def d_startDigging(self, avatarId):
        self.sendUpdateToAvatarId(avatarId, 'startDigging', [])

    def d_stopDigging(self, avatarId, questProgress):
        self.sendUpdateToAvatarId(avatarId, 'stopDigging', [questProgress])

    def d_showTreasure(self, avatarId, goldAmount=0):
        self.sendUpdateToAvatarId(avatarId, 'showTreasure', [goldAmount])

    def setStartingDepth(self, depth):
        self.startingDepth = depth

    def d_setStartingDepth(self, depth):
        self.sendUpdate('setStartingDepth', [depth])

    def b_setStartingDepth(self, depth):
        self.setStartingDepth(depth)
        self.d_setStartingDepth(depth)

    def getStartingDepth(self):
        return self.startingDepth

    def setCurrentDepth(self, depth):
        self.currentDepth = depth

    def d_setCurrentDepth(self, depth):
        self.sendUpdate('setCurrentDepth', [depth])

    def b_setCurrentDepth(self, depth):
        self.setCurrentDepth(depth)
        self.d_setCurrentDepth(depth)

    def getCurrentDepth(self):
        return self.currentDepth
