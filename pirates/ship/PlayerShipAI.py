from pirates.ship.DistributedShipAI import DistributedShipAI
from direct.directnotify import DirectNotifyGlobal

class PlayerShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayerShipAI')

    def __init__(self, air):
        DistributedShipAI.__init__(self, air)
