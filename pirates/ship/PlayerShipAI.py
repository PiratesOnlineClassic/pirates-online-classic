
from pirates.ship.DistributedShipAI import DistributedShipAI
from direct.directnotify import DirectNotifyGlobal

class PlayerShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayerShipAI')

    def __init__(self, air):
        DistributedShipAI.__init__(self, air)
        self.allowCrewState = False
        self.allowFriendState = False
        self.allowGuildState = False
        self.allowPublicState = False


    # attacked() broadcast

    def attacked(self, attacked):
        self.sendUpdate('attacked', [attacked])

    # setSiegeBounty(uint16) broadcast ram

    def setSiegeBounty(self, siegeBounty):
        self.sendUpdate('setSiegeBounty', [siegeBounty])

    # setAllowCrewState(bool) airecv required broadcast ram ownsend
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAllowCrewState(self, allowCrewState):
        self.allowCrewState = allowCrewState

    def d_setAllowCrewState(self, allowCrewState):
        self.sendUpdate('setAllowCrewState', [allowCrewState])

    def b_setAllowCrewState(self, allowCrewState):
        self.setAllowCrewState(allowCrewState)
        self.d_setAllowCrewState(allowCrewState)

    def getAllowCrewState(self):
        return self.allowCrewState

    # setAllowFriendState(bool) airecv required broadcast ram ownsend
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAllowFriendState(self, allowFriendState):
        self.allowFriendState = allowFriendState

    def d_setAllowFriendState(self, allowFriendState):
        self.sendUpdate('setAllowFriendState', [allowFriendState])

    def b_setAllowFriendState(self, allowFriendState):
        self.setAllowFriendState(allowFriendState)
        self.d_setAllowFriendState(allowFriendState)

    def getAllowFriendState(self):
        return self.allowFriendState

    # setAllowGuildState(bool) airecv required broadcast ram ownsend
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAllowGuildState(self, allowGuildState):
        self.allowGuildState = allowGuildState

    def d_setAllowGuildState(self, allowGuildState):
        self.sendUpdate('setAllowGuildState', [allowGuildState])

    def b_setAllowGuildState(self, allowGuildState):
        self.setAllowGuildState(allowGuildState)
        self.d_setAllowGuildState(allowGuildState)

    def getAllowGuildState(self):
        return self.allowGuildState

    # setAllowPublicState(bool) airecv required broadcast ram ownsend
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAllowPublicState(self, allowPublicState):
        self.allowPublicState = allowPublicState

    def d_setAllowPublicState(self, allowPublicState):
        self.sendUpdate('setAllowPublicState', [allowPublicState])

    def b_setAllowPublicState(self, allowPublicState):
        self.setAllowPublicState(allowPublicState)
        self.d_setAllowPublicState(allowPublicState)

    def getAllowPublicState(self):
        return self.allowPublicState


