from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship import ShipGlobals


class NPCShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NPCShipAI')

    def __init__(self, air):
        DistributedShipAI.__init__(self, air)

    def generate(self):
        self.air.shipManager.addShip(self)
        DistributedShipAI.generate(self)

    def delete(self):
        self.air.shipManager.removeShip(self)
        DistributedShipAI.delete(self)
