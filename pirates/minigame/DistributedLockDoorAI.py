from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedLockAI import DistributedLockAI


class DistributedLockDoorAI(DistributedLockAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLockDoorAI')

    def __init__(self, air):
        DistributedLockAI.__init__(self, air)
        self._openedBy = 0

    def getOpenedBy(self):
        return self._openedBy

    def handleLockOpened(self, avatar):
        self._openedBy = avatar.doId
        self.notify.debug('Lock door %s opened by %d' % (self.getUniqueId(), avatar.doId))
        DistributedLockAI.handleLockOpened(self, avatar)
