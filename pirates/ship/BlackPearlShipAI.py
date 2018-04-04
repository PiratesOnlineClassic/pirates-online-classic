
from pirates.ship.DistributedShipAI import DistributedShipAI
from direct.directnotify import DirectNotifyGlobal

class BlackPearlShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('BlackPearlShipAI')

    def __init__(self, air):
        DistributedShipAI.__init__(self, air)



