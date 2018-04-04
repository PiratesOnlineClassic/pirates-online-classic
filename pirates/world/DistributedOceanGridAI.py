
from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.directnotify import DirectNotifyGlobal

class DistributedOceanGridAI(DistributedCartesianGridAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedOceanGridAI')

    def __init__(self, air):
        DistributedCartesianGridAI.__init__(self, air)



