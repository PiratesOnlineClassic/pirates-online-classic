from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedLockAI import DistributedLockAI


class DistributedLockDoorAI(DistributedLockAI):
    """
    A locked (jail) door.  Picking the lock swings the door open on every
    client, which stashes the door's collisions so pirates can walk through.
    """

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
