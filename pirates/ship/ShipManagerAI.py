from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship.PlayerShipAI import PlayerShipAI


class ShipManagerAI(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipManagerAI')

    def __init__(self, air):
        self.air = air

        self.activeShips = {}

    def hasActiveShip(self, shipId):
        return shipId in self.activeShips

    def addActiveShip(self, ship):
        if ship.doId in self.activeShips:
            return

        assert(ship.getDeploy())
        self.activeShips[ship.doId] = ship

    def removeActiveShip(self, ship):
        if ship.doId not in self.activeShips:
            return

        del self.activeShips[ship.doId]

    def getActiveShip(self, shipId):
        return self.activeShips.get(shipId)

    def getActivePlayerShips(self):
        activePlayerShips = []
        for shipId, ship in list(self.activeShips.items()):
            if not isinstance(ship, PlayerShipAI):
                continue

            activePlayerShips.append(ship)

        return activePlayerShips
