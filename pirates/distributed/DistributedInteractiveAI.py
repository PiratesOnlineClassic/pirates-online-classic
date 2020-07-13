from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal


class DistributedInteractiveAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractiveAI')

    ACCEPT = 1
    DENY = 0
    MULTIUSE = False

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)

        self.userId = 0
        self.uniqueId = ''

    def requestInteraction(self, doId, interactType, instant):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            self.air.logPotentialHacker(
                message='Received requestInteraction from non-existant avatar',
                targetAvId=avatar.doId,
                doId=doId,
                interactType=interactType,
                instant=instant)

            return

        handle = self.handleRequestInteraction(avatar, interactType, instant)
        if not handle:
            self.d_rejectInteraction(avatar.doId)
            return

        if not self.MULTIUSE:
            self.b_setUserId(avatar.doId)
        else:
            self.sendUpdateToAvatarId(avatar.doId, 'setUserId', [avatar.doId])

        self.sendUpdateToAvatarId(avatar.doId, 'acceptInteraction', [])
        self.handlePostRequestInteraction(avatar)
        messenger.send(avatar.uniqueName('interact-accepted'))

    def handleRequestInteraction(self, avatar, interactType, instant):
        self.notify.debug('handleRequestInteraction not overriden by %s, '
            'defaulting to DENY' % self.__class__.__name__)

        return self.DENY

    def handlePostRequestInteraction(self, avatar):
        pass

    def requestExit(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            self.air.logPotentialHacker(
                message='Received requestExit from non-existant avatar',
                targetAvId=avatar.doId,
                doId=doId,
                interactType=interactType,
                instant=instant)

            return

        handle = self.handleRequestExit(avatar)
        if not handle:
            self.d_rejectExit(avatar.doId)
            return

        if not self.MULTIUSE:
            self.b_setUserId(0)
        else:
            self.sendUpdateToAvatarId(avatar.doId, 'setUserId', [0])

        self.handlePostRequestExit(avatar)
        messenger.send(avatar.uniqueName('interact-canceled'))

    def demandExit(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            self.notify.warning('Failed to demand exit for non-existant avatar!')
            return

        self.b_setUserId(0)

    def handleRequestExit(self, avatar):
        return self.DENY

    def handlePostRequestExit(self, avatar):
        pass

    def d_rejectInteraction(self, avatarId):
        self.sendUpdateToAvatarId(avatarId, 'rejectInteraction', [])

    def d_rejectExit(self, avatarId):
        self.sendUpdateToAvatarId(avatarId, 'rejectExit', [])

    def d_offerOptions(self, avatarId, optionIds, statusCodes):
        self.sendUpdateToAvatarId(avatarId, 'offerOptions', [optionIds, statusCodes])

    def selectOption(self, optionId):
        pass

    def setUserId(self, userId):
        self.userId = userId

    def d_setUserId(self, userId):
        self.sendUpdate('setUserId', [userId])

    def b_setUserId(self, userId):
        self.setUserId(userId)
        self.d_setUserId(userId)

    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def d_setUniqueId(self, uniqueId):
        self.sendUpdate('setUniqueId', [uniqueId])

    def b_setUniqueId(self, uniqueId):
        self.setUniqueId(uniqueId)
        self.d_setUniqueId(uniqueId)

    def getUniqueId(self):
        return self.uniqueId
