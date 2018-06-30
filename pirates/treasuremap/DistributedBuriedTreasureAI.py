from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.task import Task


class DistributedBuriedTreasureAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedBuriedTreasureAI')

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
        if self.treasureAvailable == None:
            self.treasureAvailable = config.GetBool(
                'always-allow-digging', False)  #TODO: input from questing
        if self.treasureAvailable and self.currentUser is None:
            self.currentUser = avatar
            taskMgr.doMethodLater(
                1, self.__digTask,
                '%s-avatarDigTask-%s' % (self.doId, avatar.doId))

            self.sendUpdateToAvatarId(avatar.doId, 'startDigging', [])
            return self.ACCEPT

        return self.DENY

    def handleRequestExit(self, avatar):
        if not self.currentUser:
            # We'll log this if the config variable is true. This will help clear up clutter.
            if config.GetBool('want-treasurechest-inactive-log', False):
                self.notify.debug(
                    "Failed to request handle exist; Currently \"Digging\" Avatar is not present or was deleted..?"
                )
                self.air.logPotentialHacker(
                    message=
                    'Received handleRequestExist from a avatar while buried treasure was inactive!',
                    currentAvatarId=0,
                    requestedAvatarId=avatar.doId)
            return
        elif avatar != self.currentUser:
            self.notify.warning(
                'Failed to request handle exist; Avatar is not current interactor'
            )

            self.air.logPotentialHacker(
                message=
                'Received handleRequestExist from a different avatar then is currently digging!',
                currentAvatarId=self.currentUser.doId,
                requestedAvatarId=avatar.doId)
            return

        self.currentUser = None

    def __digTask(self, task):
        self.b_setCurrentDepth(max(self.getCurrentDepth() - 1, 0))

        if not self.currentUser:
            return task.done

        if self.currentDepth <= 0:

            questProgress = 1
            goldAmount = 0  # Appears to be deprecated code

            avatarId = self.currentUser.doId
            self.sendUpdateToAvatarId(avatarId, 'stopDigging', [questProgress])
            self.sendUpdateToAvatarId(avatarId, 'showTreasure', [goldAmount])

            taskMgr.doMethodLater(5, self.__resetTask,
                                  '%s-digResetTask' % self.doId)
            return task.done

        return task.again

    def __resetTask(self, task):
        if self.currentUser:
            self.currentUser = None
        self.b_setCurrentDepth(self.getStartingDepth())
        return task.done

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

    def d_startDigging(self):
        self.sendUpdate('startDigging', [])

    def d_stopDigging(self, questProgress):
        self.sendUpdate('stopDigging', [questProgress])
