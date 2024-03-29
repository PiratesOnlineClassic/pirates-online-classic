from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class DistributedChatManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedChatManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
