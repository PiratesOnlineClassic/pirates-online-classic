# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.ship.BlackPearlShip
from pirates.ship.DistributedShip import DistributedShip


class BlackPearlShip(DistributedShip):
    __module__ = __name__

    def __init__(self, cr):
        DistributedShip.__init__(self, cr)

    def checkAbleDropAnchor(self):
        if self.shipStatusDisplay:
            self.shipStatusDisplay.disableAnchorButton()

    def announceGenerate(self):
        self.setupAggroCollisions()
        DistributedShip.announceGenerate(self)

    def disable(self):
        self.cleanupAggroCollisions()
        DistributedShip.disable(self)

    def handleChildLeave(self, child, zoneId):
        DistributedShip.handleChildLeave(self, child, zoneId)
        if child.isLocal():
            localAvatar.ship = None
        return

    def loadShipStatusDisplay(self):
        DistributedShip.loadShipStatusDisplay(self)
        self.shipStatusDisplay.hidePermissionButton()
# okay decompiling .\pirates\ship\BlackPearlShip.pyc
