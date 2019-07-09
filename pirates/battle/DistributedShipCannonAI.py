from direct.directnotify import DirectNotifyGlobal

from pirates.battle.DistributedPCCannonAI import DistributedPCCannonAI
from pirates.shipparts.DistributedShippartAI import DistributedShippartAI
from pirates.shipparts.CannonDNA import CannonDNA


class DistributedCannonDNA(CannonDNA):
    pass


class DistributedShipCannonAI(DistributedPCCannonAI, DistributedShippartAI, DistributedCannonDNA):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipCannonAI')

    def __init__(self, air):
        DistributedPCCannonAI.__init__(self, air)
        DistributedShippartAI.__init__(self, air)
        DistributedCannonDNA.__init__(self)

    def setCannonIndex(self, cannonIndex):
        self.cannonIndex = cannonIndex

    def d_setCannonIndex(self, cannonIndex):
        self.sendUpdate('setCannonIndex', [cannonIndex])

    def b_setCannonIndex(self, cannonIndex):
        self.setCannonIndex(cannonIndex)
        self.d_setCannonIndex(cannonIndex)

    def getCannonIndex(self):
        return self.cannonIndex

    def handleRequestInteraction(self, avatar, interactType, instant):
        self.startWeapon(avatar.doId)
        return self.ACCEPT

    def handleRequestExit(self, avatar):
        self.stopWeapon(avatar.doId)
        return self.ACCEPT
