
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedDinghyAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDinghyAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.interactRadius = 0
        self.locationId = 0
        self.siegeTeam = 0


    # setInteractRadius(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setInteractRadius(self, interactRadius):
        self.interactRadius = interactRadius

    def d_setInteractRadius(self, interactRadius):
        self.sendUpdate('setInteractRadius', [interactRadius])

    def b_setInteractRadius(self, interactRadius):
        self.setInteractRadius(interactRadius)
        self.d_setInteractRadius(interactRadius)

    def getInteractRadius(self):
        return self.interactRadius

    # setLocationId(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setLocationId(self, locationId):
        self.locationId = locationId

    def d_setLocationId(self, locationId):
        self.sendUpdate('setLocationId', [locationId])

    def b_setLocationId(self, locationId):
        self.setLocationId(locationId)
        self.d_setLocationId(locationId)

    def getLocationId(self):
        return self.locationId

    # setSiegeTeam(int8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setSiegeTeam(self, siegeTeam):
        self.siegeTeam = siegeTeam

    def d_setSiegeTeam(self, siegeTeam):
        self.sendUpdate('setSiegeTeam', [siegeTeam])

    def b_setSiegeTeam(self, siegeTeam):
        self.setSiegeTeam(siegeTeam)
        self.d_setSiegeTeam(siegeTeam)

    def getSiegeTeam(self):
        return self.siegeTeam

    # offerOptions()

    def offerOptions(self, offerOptions):
        self.sendUpdate('offerOptions', [offerOptions])

    # offerBandOptions(BandShipInfo [])

    def offerBandOptions(self, offerBandOptions):
        self.sendUpdate('offerBandOptions', [offerBandOptions])

    # offerFriendOptions(FriendShipInfo [])

    def offerFriendOptions(self, offerFriendOptions):
        self.sendUpdate('offerFriendOptions', [offerFriendOptions])

    # offerGuildOptions(GuildShipInfo [])

    def offerGuildOptions(self, offerGuildOptions):
        self.sendUpdate('offerGuildOptions', [offerGuildOptions])

    # offerPublicOptions(PublicShipInfo [])

    def offerPublicOptions(self, offerPublicOptions):
        self.sendUpdate('offerPublicOptions', [offerPublicOptions])

    # sendAvatarToShip(uint32)

    def sendAvatarToShip(self, sendAvatarToShip):
        self.sendUpdate('sendAvatarToShip', [sendAvatarToShip])

    # denyAccess(int8)

    def denyAccess(self, denyAccess):
        self.sendUpdate('denyAccess', [denyAccess])

    # selectOwnShip(uint32, int8) clsend airecv

    def selectOwnShip(self, selectOwnShip, todo_int8_1):
        pass

    # selectFriendShip(uint32) clsend airecv

    def selectFriendShip(self, selectFriendShip):
        pass

    # selectBandShip(uint32) clsend airecv

    def selectBandShip(self, selectBandShip):
        pass

    # selectGuildShip(uint32) clsend airecv

    def selectGuildShip(self, selectGuildShip):
        pass

    # selectPublicShip(uint32) clsend airecv

    def selectPublicShip(self, selectPublicShip):
        pass

    # responseFriendsList(uint32, uint32array)

    def responseFriendsList(self, responseFriendsList, todo_uint32array_1):
        self.sendUpdate('responseFriendsList', [responseFriendsList, todo_uint32array_1])

    # responseGuildMatesList(uint32, uint32array)

    def responseGuildMatesList(self, responseGuildMatesList, todo_uint32array_1):
        self.sendUpdate('responseGuildMatesList', [responseGuildMatesList, todo_uint32array_1])


