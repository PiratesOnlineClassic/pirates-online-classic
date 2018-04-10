from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.distributed.DistributedTargetableObjectAI import DistributedTargetableObjectAI

class DistributedInteractivePropAI(DistributedInteractiveAI, DistributedTargetableObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractivePropAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        DistributedTargetableObjectAI.__init__(self, air)