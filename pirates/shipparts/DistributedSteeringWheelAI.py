
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.shipparts.DistributedShippartAI import DistributedShippartAI
from direct.directnotify import DirectNotifyGlobal

class DistributedSteeringWheelAI(DistributedInteractiveAI, DistributedShippartAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSteeringWheelAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        DistributedShippartAI.__init__(self, air)



