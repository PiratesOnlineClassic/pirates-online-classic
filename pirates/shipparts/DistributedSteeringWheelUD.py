
from pirates.distributed.DistributedInteractiveUD import DistributedInteractiveUD
from pirates.shipparts.DistributedShippartUD import DistributedShippartUD
from direct.directnotify import DirectNotifyGlobal

class DistributedSteeringWheelUD(DistributedInteractiveUD, DistributedShippartUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSteeringWheelUD')

    def __init__(self, air):
        DistributedInteractiveUD.__init__(self, air)
        DistributedShippartUD.__init__(self, air)



