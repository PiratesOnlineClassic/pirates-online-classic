from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.task import Task

class DistributedBuriedTreasureAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuriedTreasureAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.startingDepth = 0
        self.currentDepth = 0
        self.currentUser = None
        self.treasureAvailable = None

    def delete(self):
        self.treasureAvailable = False
        self.currentUser = None
        DistributedInteractiveAI.delete(self)

    def handleRequestInteraction(self, avatar, interactType, instant):
        if self.currentUser:
            return self.DENY

        applicable = self.air.questMgr.treasureChestOpened(avatar, self, self.questProgressionCallback)
        if applicable:
            return self.ACCEPT
        else:
            return self.DENY

    def questProgressionCallback(self, quest):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        def performChestDig(task):
            self.b_setCurrentDepth(max(self.getCurrentDepth() - 1, 0))
            if not self.currentUser:
                return task.done

            if self.currentDepth <= 0:
                self.d_stopDigging(avatar.doId, quest.getProgress())
                self.d_showTreasure(avatar.doId)
                taskMgr.doMethodLater(5, self.resetChest, '%s-digResetTask' % self.doId)
                return task.done

            return task.again

        self.d_startSearching(avatar.doId)
        taskMgr.doMethodLater(1, performChestDig, self.uniqueName('avatarDiggingTask-%d' % avatar.doId))

    def resetDigSpot(self, task):
        self.currentUser = None
        self.b_setCurrentDepth(self.getStartingDepth())
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
