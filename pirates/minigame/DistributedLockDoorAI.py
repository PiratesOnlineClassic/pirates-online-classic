
from pirates.minigame.DistributedLockAI import DistributedLockAI
from direct.directnotify import DirectNotifyGlobal

class DistributedLockDoorAI(DistributedLockAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLockDoorAI')

    def __init__(self, air):
        DistributedLockAI.__init__(self, air)



