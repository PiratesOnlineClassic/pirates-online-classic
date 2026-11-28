from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *

from pirates.battle.DistributedPCCannonAI import DistributedPCCannonAI
from pirates.shipparts.DistributedShippartAI import DistributedShippartAI
from pirates.shipparts.CannonDNA import CannonDNA
from pirates.uberdog.UberDogGlobals import InventoryType


class DistributedCannonDNA(CannonDNA):
    pass


class DistributedShipCannonAI(DistributedPCCannonAI, DistributedShippartAI, DistributedCannonDNA):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipCannonAI')

    def __init__(self, air):
        DistributedPCCannonAI.__init__(self, air)
        DistributedShippartAI.__init__(self, air)
        DistributedCannonDNA.__init__(self)
        self.cannonIndex = 0

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
        if self.userId and self.userId != avatar.doId and self.userId in self.air.doId2do:
            return self.DENY

        ship = self.getShip()
        if ship is not None and not ship.isSailable():
            return self.DENY

        self.startWeapon(avatar.doId)
        return self.ACCEPT

    def handleRequestExit(self, avatar):
        self.stopWeapon(avatar.doId)
        return self.ACCEPT
