from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal
from pirates.shipparts.DistributedShippartAI import DistributedShippartAI


class DistributedSteeringWheelAI(DistributedInteractiveAI,
                                 DistributedShippartAI):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedSteeringWheelAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        DistributedShippartAI.__init__(self, air)
