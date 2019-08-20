from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class DistributedCharterableObjectAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCharterableObjectAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.ownerId = 0

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def d_setOwnerId(self, ownerId):
        self.sendUpdate('setOwnerId', [ownerId])

    def b_setOwnerId(self, ownerId):
        self.setOwnerId(ownerId)
        self.d_setOwnerId(ownerId)

    def getOwnerId(self):
        return self.ownerId
