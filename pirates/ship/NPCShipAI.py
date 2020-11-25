from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship import ShipGlobals


class NPCShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NPCShipAI')

    def __init__(self, air):
        DistributedShipAI.__init__(self, air)
