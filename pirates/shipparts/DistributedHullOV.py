from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObjectOV
from pirates.ship import ShipGlobals

class DistributedHullOV(DistributedObjectOV.DistributedObjectOV):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHullOV')
    
    def __init__(self, cr):
        DistributedObjectOV.DistributedObjectOV.__init__(self, cr)
        self.shipId = 0
        self.shipClass = 0
        self.baseTeam = 0
        self.hullTexIndex = 0
        self.stripTexIndex = 0
        self.patternTexIndex = 0
        self.hullColorIndex = 0
        self.stripColorIndex = 0
        self.patternColorIndex = 0
        self.hullHilightIndex = 0
        self.stripHilightIndex = 0
        self.patternHilightIndex = 0
        self.mastConfig1 = 0
        self.mastConfig2 = 0
        self.mastConfig3 = 0
        self.foreMastConfig = 0
        self.aftMastConfig = 0
        self.sailConfig1 = 0
        self.sailConfig2 = 0
        self.sailConfig3 = 0
        self.foreSailConfig = 0
        self.aftSailConfig = 0
        self.prowType = 0
        self.ramType = 0
        self.cabinType = 0
        self.cannonConfig = []
        self.rBroadsideConfig = []
        self.lBroadsideConfig = []
        self.pendingLinkToShip = None
    
    def announceGenerate(self):
        DistributedObjectOV.DistributedObjectOV.announceGenerate(self)

    def disable(self):
        DistributedObjectOV.DistributedObjectOV.disable(self)

    def __repr__(self):
        return repr(self.doId)

    def setShipId(self, val):
        self.shipId = val

    def setShipClass(self, val):
        self.shipClass = val
        messenger.send('setShipClass-%s' % self.shipId, [self.shipClass])

    def setBaseTeam(self, val):
        pass

    def setHullTextureIndex(self, val):
        pass

    def setStripeTextureIndex(self, val):
        pass

    def setPatternTextureIndex(self, val):
        pass

    def setHullColorIndex(self, val):
        pass

    def setStripeColorIndex(self, val):
        pass

    def setPatternColorIndex(self, val):
        pass

    def setHullHilightColorIndex(self, val):
        pass

    def setStripeHilightColorIndex(self, val):
        pass

    def setPatternHilightColorIndex(self, val):
        pass

    def setAftsailConfig(self, val):
        pass

    def setProwType(self, val):
        pass

    def setRamType(self, val):
        pass

    def setCabinType(self, val):
        pass

    def setCannonConfig(self, val):
        self.cannonConfig = val
        messenger.send('setHullCannonConfig-%s' % self.shipId, [val])

    def setLeftBroadsideConfig(self, val):
        self.lBroadsideConfig = val
        messenger.send('setHullLeftBroadsideConfig-%s' % self.shipId, [val])

    def setRightBroadsideConfig(self, val):
        self.rBroadsideConfig = val
        messenger.send('setHullRightBroadsideConfig-%s' % self.shipId, [val])

