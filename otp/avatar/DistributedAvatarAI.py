from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from direct.directnotify import DirectNotifyGlobal

class DistributedAvatarAI(DistributedSmoothNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAvatarAI')

    def __init__(self, air):
        DistributedSmoothNodeAI.__init__(self, air)

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name
