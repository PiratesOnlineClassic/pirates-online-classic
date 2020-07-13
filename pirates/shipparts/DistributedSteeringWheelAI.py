from direct.directnotify import DirectNotifyGlobal

from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.shipparts.DistributedShippartAI import DistributedShippartAI


class DistributedSteeringWheelAI(DistributedInteractiveAI, DistributedShippartAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSteeringWheelAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        DistributedShippartAI.__init__(self, air)
        self.ship = None

    def generate(self):
        DistributedInteractiveAI.generate(self)
        DistributedShippartAI.generate(self)

        self.ship = self.getShip()
        assert(self.ship is not None)

    def handleRequestInteraction(self, avatar, interactType, instant):
        if avatar.doId != self.ship.captainId and self.userId > 0:
            return self.DENY

        # reject the user that was previously steering (if one is present)
        if self.userId > 0:
            self.d_rejectExit(self.userId)

        # if the user who is trying to interact is not the captain,
        # we need to give them "special permission" to update fields
        if avatar.doId != self.ship.captainId:
            fieldList = [
                'setComponentL',
                'setComponentX',
                'setComponentY',
                'setComponentZ',
                'setComponentH',
                'setComponentP',
                'setComponentR',
                'setComponentT',
                'setSmStop',
                'setSmH',
                'setSmZ',
                'setSmXY',
                'setSmXZ',
                'setSmPos',
                'setSmHpr',
                'setSmXYH',
                'setSmXYZH',
                'setSmPosHpr',
                'setSmPosHprL',
                'clearSmoothing',
                'suggestResync',
                'returnResync'
            ]

            self.air.setAllowClientSend(avatar.doId, self.ship, fieldList)

        return self.ACCEPT

    def handlePostRequestInteraction(self, avatar):
        self.ship.b_setClientController(avatar.doId)
        self.ship.b_setGameState('ClientSteering', avatar.doId)

    def handleRequestExit(self, avatar):
        return self.ACCEPT

    def handlePostRequestExit(self, avatar):
        self.ship.b_setClientController(0)
        self.ship.b_setGameState('Adrift', 0)
