from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class AccountAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('AccountAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
