from pirates.ship.DistributedShip import DistributedShip

class BlackPearlShip(DistributedShip):
    
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

    def loadShipStatusDisplay(self):
        DistributedShip.loadShipStatusDisplay(self)
        self.shipStatusDisplay.hidePermissionButton()


