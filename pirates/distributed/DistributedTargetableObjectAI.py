
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTargetableObjectAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTargetableObjectAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # requestTarget() airecv clsend

    def requestTarget(self, requestTarget):
        pass

    # removeTarget() airecv clsend

    def removeTarget(self, removeTarget):
        pass


