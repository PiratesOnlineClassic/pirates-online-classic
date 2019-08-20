from pirates.ship.DistributedShipUD import DistributedShipUD
from direct.directnotify import DirectNotifyGlobal

class PlayerShipUD(DistributedShipUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayerShipUD')

    def __init__(self, air):
        DistributedShipUD.__init__(self, air)
