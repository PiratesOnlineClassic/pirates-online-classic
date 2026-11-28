from direct.directnotify import DirectNotifyGlobal

from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.shipparts.DistributedShippartAI import DistributedShippartAI


class DistributedSteeringWheelAI(DistributedInteractiveAI, DistributedShippartAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSteeringWheelAI')

    # the fields a helmsman who isn't the ship's owner needs to be able to
    # send in order to steer the ship, the owner may already send them (ownsend)...
    SteeringFields = [
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
        # only the ship's crew may take the wheel, and never while the
        # ship is going down (see DistributedShip.canTakeWheel)...
        if not self.ship.hasCrewMember(avatar.doId):
            self.air.writeServerEvent('suspicious', avId=avatar.doId,
                issue='Tried to take the wheel of ship %d they are not crew of!' % self.ship.doId)

            return self.DENY

        if not self.ship.isSailable() or self.ship.getCurrentGameState() == 'Pinned':
            return self.DENY

        if not self.ship.canTakeWheel(avatar):
            return self.DENY

        # the captain may always take the wheel back from whoever is steering:
        if avatar.doId != self.ship.captainId and self.userId > 0 and self.userId != avatar.doId:
            return self.DENY

        # reject the user that was previously steering (if one is present)
        if self.userId > 0 and self.userId != avatar.doId:
            self.d_rejectExit(self.userId)
            self.revokeSteering(self.userId)

        # if the user who is trying to interact is not the captain,
        # we need to give them "special permission" to update fields
        if avatar.doId != self.ship.captainId:
            self.air.setAllowClientSend(avatar.doId, self.ship, self.SteeringFields)

        return self.ACCEPT

    def revokeSteering(self, avatarId):
        # the captain owns the ship's position fields, everyone else
        # loses the permission to move the ship once they let go of the wheel...
        if avatarId and avatarId != self.ship.captainId:
            self.air.setAllowClientSend(avatarId, self.ship, [])

    def handlePostRequestInteraction(self, avatar):
        self.ship.b_setClientController(avatar.doId)
        self.ship.b_setGameState('ClientSteering', avatar.doId)

    def handleRequestExit(self, avatar):
        # a helmsman that had the wheel taken from them by the captain lets go of
        # the wheel afterwards, that must not release the captain's controls...
        if avatar.doId != self.userId:
            return self.DENY

        return self.ACCEPT

    def handlePostRequestExit(self, avatar):
        self.revokeSteering(avatar.doId)
        self.ship.releaseWheel(avatar.doId)
