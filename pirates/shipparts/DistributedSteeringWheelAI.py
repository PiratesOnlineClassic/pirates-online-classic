from direct.directnotify import DirectNotifyGlobal

from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.shipparts.DistributedShippartAI import DistributedShippartAI


class DistributedSteeringWheelAI(DistributedInteractiveAI, DistributedShippartAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSteeringWheelAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        DistributedShippartAI.__init__(self, air)

    def handleRequestInteraction(self, avatar, interactType, instant):
        ship = self.getShip()
        assert(ship is not None)
        ship.b_setGameState('ClientSteering', avatar.doId)
        return self.ACCEPT

    def handleRequestExit(self, avatar):
        ship = self.getShip()
        assert(ship is not None)
        ship.b_setGameState('Adrift', 0)
        return self.ACCEPT
