from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal


class DistributedSteeringWheelUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSteeringWheelUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
