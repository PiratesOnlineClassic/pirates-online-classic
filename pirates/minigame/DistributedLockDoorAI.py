from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedLockAI import DistributedLockAI


class DistributedLockDoorAI(DistributedLockAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLockDoorAI')

    def __init__(self, air):
        DistributedLockAI.__init__(self, air)
