from direct.directnotify import DirectNotifyGlobal

from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.piratesbase import PiratesGlobals


class DistributedDinghyAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDinghyAI')
    MULTIUSE = True

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)

        self.interactRadius = 0
        self.locationId = 0
        self.siegeTeam = 0

    def getPublicShipInfo(self, shipDoId):
        ship = self.air.doId2do.get(shipDoId)
        assert(ship is not None)

        captain = self.air.doId2do.get(ship.getCaptainId())
        assert(captain is not None)

        shipInfo = [
            captain.doId,
            ship.doId,
            ship.getHp(),
            ship.getSp(),
            len(ship.getCargo()),
            len(ship.getCrew()),
            1, # TODO!
            ship.getShipClass(),
            ship.getName(),
            ship.getSiegeTeam(),
            captain.getName()
        ]

        return shipInfo

    def getOfferPublicOptions(self):
        publicOptions = []
        for ship in self.air.shipManager.getPlayerShips():
            if not ship.getAllowPublicState():
                continue

            publicOptions.append(self.getPublicShipInfo(ship.doId))

        return publicOptions

    def d_offerPublicOptions(self, avatarId, publicOptions):
        self.sendUpdateToAvatarId(avatarId, 'offerPublicOptions', [publicOptions])

    def handleRequestInteraction(self, avatar, interactType, instant):
        return self.ACCEPT

    def handlePostRequestInteraction(self, avatar):
        self.d_offerPublicOptions(avatar.doId, self.getOfferPublicOptions())

    def handleRequestExit(self, avatar):
        return self.ACCEPT

    def canSelectShip(self, ship):
        if not self.air.shipManager.hasActiveShip(ship.doId):
            return False

        # check to see if the ship is full
        if len(ship.getCrew()) >= ship.getMaxCrew():
            return False

        return True

    def selectPublicShip(self, shipDoId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        ship = self.air.doId2do.get(shipDoId)
        if not ship:
            self.d_sendAvatarToShip(avatar.doId, 0)
            return

        if not self.canSelectShip(ship):
            self.d_sendAvatarToShip(avatar.doId, 0)
            return

        if not ship.getAllowPublicState():
            self.d_sendAvatarToShip(avatar.doId, 0)
            return

        self.sendAvatarToShip(avatar, ship)

    def setInteractRadius(self, interactRadius):
        self.interactRadius = interactRadius

    def d_setInteractRadius(self, interactRadius):
        self.sendUpdate('setInteractRadius', [interactRadius])

    def b_setInteractRadius(self, interactRadius):
        self.setInteractRadius(interactRadius)
        self.d_setInteractRadius(interactRadius)

    def getInteractRadius(self):
        return self.interactRadius

    def setLocationId(self, locationId):
        self.locationId = locationId

    def d_setLocationId(self, locationId):
        self.sendUpdate('setLocationId', [locationId])

    def b_setLocationId(self, locationId):
        self.setLocationId(locationId)
        self.d_setLocationId(locationId)

    def getLocationId(self):
        return self.locationId

    def setSiegeTeam(self, siegeTeam):
        self.siegeTeam = siegeTeam

    def d_setSiegeTeam(self, siegeTeam):
        self.sendUpdate('setSiegeTeam', [siegeTeam])

    def b_setSiegeTeam(self, siegeTeam):
        self.setSiegeTeam(siegeTeam)
        self.d_setSiegeTeam(siegeTeam)

    def getSiegeTeam(self):
        return self.siegeTeam

    def selectOwnShip(self, shipId, teamSpec):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        inventory = avatar.getInventory()
        if not inventory:
            self.notify.warning('Failed to select ship %d, '
                'avatar %d has no inventory!' % (shipId, avatar.doId))

            self.d_sendAvatarToShip(avatar.doId, 0)
            return

        parentObj = avatar.getParentObj()
        if not isinstance(parentObj, DistributedGameAreaAI):
            self.notify.warning('Failed to select avatar ship %d, '
                'avatar %d has invalid parent object %r!' % (shipId, avatar.doId, parentObj))

            self.d_sendAvatarToShip(avatar.doId, 0)
            return

        shipDoIdList = inventory.getShipDoIdList()
        if shipId not in shipDoIdList:
            self.notify.warning('Failed to select avatar ship %d, '
                'avatar %d does not own that ship!' % (shipId, avatar.doId))

            self.d_sendAvatarToShip(avatar.doId, 0)
            return

        def deployShipCallback(success):
            if not success:
                self.d_sendAvatarToShip(avatar.doId, 0)
                return

            ship = self.air.doId2do.get(shipId)
            if not ship:
                self.notify.warning('Failed to select avatar %d ship to deploy %d, '
                    'ship never deployed!' % (avatar.doId, shipId))

                self.d_sendAvatarToShip(avatar.doId, 0)
                return

            self.sendAvatarToShip(avatar, ship)

        self.air.questMgr.deployedShip(avatar)
        parentObj.shipDeployer.deployShip(avatar, shipId, deployShipCallback)

    def sendAvatarToShip(self, avatar, ship):
        assert(avatar is not None)
        assert(ship is not None)

        def _interestDoneCallback():
            self.d_sendAvatarToShip(avatar.doId, ship.doId)

        self.air.worldGridManager.handleLocationChanged(ship.getParentObj(), avatar, ship.zoneId,
            callback=_interestDoneCallback)

    def d_sendAvatarToShip(self, avatarId, shipId):
        self.sendUpdateToAvatarId(avatarId, 'sendAvatarToShip', [shipId])
