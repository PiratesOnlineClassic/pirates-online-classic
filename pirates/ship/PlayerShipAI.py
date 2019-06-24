from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.world.DistributedOceanGridAI import DistributedOceanGridAI
from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI


class PlayerShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayerShipAI')

    def __init__(self, air):
        DistributedShipAI.__init__(self, air)

        self.allowCrewState = False
        self.allowFriendState = False
        self.allowGuildState = False
        self.allowPublicState = False

    def setLocation(self, parentId, zoneId):
        parentObj = self.air.doId2do.get(parentId)
        if parentObj is not None and isinstance(parentObj, DistributedOceanGridAI):
            for avatarId in self.crew:
                avatar = self.air.doId2do.get(avatarId)
                if avatar is not None:
                    self.air.worldGridManager.handleLocationChanged(parentObj, avatar, zoneId)

        DistributedShipAI.setLocation(self, parentId, zoneId)

    def handleChildLeave(self, childObj, zoneId):
        if isinstance(childObj, DistributedPlayerPirateAI):
            self.air.worldGridManager.clearAvatarInterest(self.getParentObj(), childObj)

        DistributedShipAI.handleChildLeave(self, childObj, zoneId)

    def setAllowCrewState(self, allowCrewState):
        self.allowCrewState = allowCrewState

    def d_setAllowCrewState(self, allowCrewState):
        self.sendUpdate('setAllowCrewState', [allowCrewState])

    def b_setAllowCrewState(self, allowCrewState):
        self.setAllowCrewState(allowCrewState)
        self.d_setAllowCrewState(allowCrewState)

    def getAllowCrewState(self):
        return self.allowCrewState

    def setAllowFriendState(self, allowFriendState):
        self.allowFriendState = allowFriendState

    def d_setAllowFriendState(self, allowFriendState):
        self.sendUpdate('setAllowFriendState', [allowFriendState])

    def b_setAllowFriendState(self, allowFriendState):
        self.setAllowFriendState(allowFriendState)
        self.d_setAllowFriendState(allowFriendState)

    def getAllowFriendState(self):
        return self.allowFriendState

    def setAllowGuildState(self, allowGuildState):
        self.allowGuildState = allowGuildState

    def d_setAllowGuildState(self, allowGuildState):
        self.sendUpdate('setAllowGuildState', [allowGuildState])

    def b_setAllowGuildState(self, allowGuildState):
        self.setAllowGuildState(allowGuildState)
        self.d_setAllowGuildState(allowGuildState)

    def getAllowGuildState(self):
        return self.allowGuildState

    def setAllowPublicState(self, allowPublicState):
        self.allowPublicState = allowPublicState

    def d_setAllowPublicState(self, allowPublicState):
        self.sendUpdate('setAllowPublicState', [allowPublicState])

    def b_setAllowPublicState(self, allowPublicState):
        self.setAllowPublicState(allowPublicState)
        self.d_setAllowPublicState(allowPublicState)

    def getAllowPublicState(self):
        return self.allowPublicState
