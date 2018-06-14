from pirates.shipparts.DistributedShippartAI import DistributedShippartAI
from direct.directnotify import DirectNotifyGlobal
from pirates.destructibles.DistributedDestructibleArrayAI import DistributedDestructibleArrayAI
from pirates.ship import ShipGlobals

class DistributedHullDNA:

    def __init__(self):
        self.shipClass = 0
        self.baseTeam = 0

        self.hullTextureIndex = []
        self.stripeTextureIndex = []
        self.patternTextureIndex = []
        self.hullColorIndex = []
        self.stripeColorIndex = []
        self.patternColorIndex = []
        self.hullHilightColorIndex = []
        self.stripeHilightColorIndex = []
        self.patternHilightColorIndex = []

        self.prowType = 0
        self.ramType = 0
        self.cabinType = 0
        self.cannonConfig = []
        self.leftBroadsideConfig = []
        self.rightBroadsideConfig = []
        self.broadsideAmmo = 0

        self.wallDecorConfig = []
        self.floorDecorConfig = []

    def setShipClass(self, shipClass):
        self.shipClass = shipClass

    def d_setShipClass(self, shipClass):
        self.sendUpdate('setShipClass', [shipClass])

    def b_setShipClass(self, shipClass):
        self.setShipClass(shipClass)
        self.d_setShipClass(shipClass)

    def getShipClass(self):
        return self.shipClass

    def setBaseTeam(self, baseTeam):
        self.baseTeam = baseTeam

    def d_setBaseTeam(self, baseTeam):
        self.sendUpdate('setBaseTeam', [baseTeam])

    def b_setBaseTeam(self, baseTeam):
        self.setBaseTeam(baseTeam)
        self.d_setBaseTeam(baseTeam)

    def getBaseTeam(self):
        return self.baseTeam

    def setHullTextureIndex(self, hullTextureIndex):
        self.hullTextureIndex = hullTextureIndex

    def d_setHullTextureIndex(self, hullTextureIndex):
        self.sendUpdate('setHullTextureIndex', [hullTextureIndex])

    def b_setHullTextureIndex(self, hullTextureIndex):
        self.setHullTextureIndex(hullTextureIndex)
        self.d_setHullTextureIndex(hullTextureIndex)

    def getHullTextureIndex(self):
        return self.hullTextureIndex

    def setStripeTextureIndex(self, stripeTextureIndex):
        self.stripeTextureIndex = stripeTextureIndex

    def d_setStripeTextureIndex(self, stripeTextureIndex):
        self.sendUpdate('setStripeTextureIndex', [stripeTextureIndex])

    def b_setStripeTextureIndex(self, stripeTextureIndex):
        self.setStripeTextureIndex(stripeTextureIndex)
        self.d_setStripeTextureIndex(stripeTextureIndex)

    def getStripeTextureIndex(self):
        return self.stripeTextureIndex

    def setPatternTextureIndex(self, patternTextureIndex):
        self.patternTextureIndex = patternTextureIndex

    def d_setPatternTextureIndex(self, patternTextureIndex):
        self.sendUpdate('setPatternTextureIndex', [patternTextureIndex])

    def b_setPatternTextureIndex(self, patternTextureIndex):
        self.setPatternTextureIndex(patternTextureIndex)
        self.d_setPatternTextureIndex(patternTextureIndex)

    def getPatternTextureIndex(self):
        return self.patternTextureIndex

    def setHullColorIndex(self, hullColorIndex):
        self.hullColorIndex = hullColorIndex

    def d_setHullColorIndex(self, hullColorIndex):
        self.sendUpdate('setHullColorIndex', [hullColorIndex])

    def b_setHullColorIndex(self, hullColorIndex):
        self.setHullColorIndex(hullColorIndex)
        self.d_setHullColorIndex(hullColorIndex)

    def getHullColorIndex(self):
        return self.hullColorIndex

    def setStripeColorIndex(self, stripeColorIndex):
        self.stripeColorIndex = stripeColorIndex

    def d_setStripeColorIndex(self, stripeColorIndex):
        self.sendUpdate('setStripeColorIndex', [stripeColorIndex])

    def b_setStripeColorIndex(self, stripeColorIndex):
        self.setStripeColorIndex(stripeColorIndex)
        self.d_setStripeColorIndex(stripeColorIndex)

    def getStripeColorIndex(self):
        return self.stripeColorIndex

    def setPatternColorIndex(self, patternColorIndex):
        self.patternColorIndex = patternColorIndex

    def d_setPatternColorIndex(self, patternColorIndex):
        self.sendUpdate('setPatternColorIndex', [patternColorIndex])

    def b_setPatternColorIndex(self, patternColorIndex):
        self.setPatternColorIndex(patternColorIndex)
        self.d_setPatternColorIndex(patternColorIndex)

    def getPatternColorIndex(self):
        return self.patternColorIndex

    def setHullHilightColorIndex(self, hullHilightColorIndex):
        self.hullHilightColorIndex = hullHilightColorIndex

    def d_setHullHilightColorIndex(self, hullHilightColorIndex):
        self.sendUpdate('setHullHilightColorIndex', [hullHilightColorIndex])

    def b_setHullHilightColorIndex(self, hullHilightColorIndex):
        self.setHullHilightColorIndex(hullHilightColorIndex)
        self.d_setHullHilightColorIndex(hullHilightColorIndex)

    def getHullHilightColorIndex(self):
        return self.hullHilightColorIndex

    def setStripeHilightColorIndex(self, stripeHilightColorIndex):
        self.stripeHilightColorIndex = stripeHilightColorIndex

    def d_setStripeHilightColorIndex(self, stripeHilightColorIndex):
        self.sendUpdate('setStripeHilightColorIndex', [stripeHilightColorIndex])

    def b_setStripeHilightColorIndex(self, stripeHilightColorIndex):
        self.setStripeHilightColorIndex(stripeHilightColorIndex)
        self.d_setStripeHilightColorIndex(stripeHilightColorIndex)

    def getStripeHilightColorIndex(self):
        return self.stripeHilightColorIndex

    def setPatternHilightColorIndex(self, patternHilightColorIndex):
        self.patternHilightColorIndex = patternHilightColorIndex

    def d_setPatternHilightColorIndex(self, patternHilightColorIndex):
        self.sendUpdate('setPatternHilightColorIndex', [patternHilightColorIndex])

    def b_setPatternHilightColorIndex(self, patternHilightColorIndex):
        self.setPatternHilightColorIndex(patternHilightColorIndex)
        self.d_setPatternHilightColorIndex(patternHilightColorIndex)

    def getPatternHilightColorIndex(self):
        return self.patternHilightColorIndex

    def setProwType(self, prowType):
        self.prowType = prowType

    def d_setProwType(self, prowType):
        self.sendUpdate('setProwType', [prowType])

    def b_setProwType(self, prowType):
        self.setProwType(prowType)
        self.d_setProwType(prowType)

    def getProwType(self):
        return self.prowType

    def setRamType(self, ramType):
        self.ramType = ramType

    def d_setRamType(self, ramType):
        self.sendUpdate('setRamType', [ramType])

    def b_setRamType(self, ramType):
        self.setRamType(ramType)
        self.d_setRamType(ramType)

    def getRamType(self):
        return self.ramType

    def setCabinType(self, cabinType):
        self.cabinType = cabinType

    def d_setCabinType(self, cabinType):
        self.sendUpdate('setCabinType', [cabinType])

    def b_setCabinType(self, cabinType):
        self.setCabinType(cabinType)
        self.d_setCabinType(cabinType)

    def getCabinType(self):
        return self.cabinType

    def setAttachmentConfig(self, attachmentConfig):
        self.attachmentConfig = attachmentConfig

    def d_setAttachmentConfig(self, attachmentConfig):
        self.sendUpdate('setAttachmentConfig', [attachmentConfig])

    def b_setAttachmentConfig(self, attachmentConfig):
        self.setAttachmentConfig(attachmentConfig)
        self.d_setAttachmentConfig(attachmentConfig)

    def getAttachmentConfig(self):
        return self.attachmentConfig

    def setCannonConfig(self, cannonConfig):
        self.cannonConfig = cannonConfig

    def d_setCannonConfig(self, cannonConfig):
        self.sendUpdate('setCannonConfig', [cannonConfig])

    def b_setCannonConfig(self, cannonConfig):
        self.setCannonConfig(cannonConfig)
        self.d_setCannonConfig(cannonConfig)

    def getCannonConfig(self):
        return self.cannonConfig

    def setLeftBroadsideConfig(self, leftBroadsideConfig):
        self.leftBroadsideConfig = leftBroadsideConfig

    def d_setLeftBroadsideConfig(self, leftBroadsideConfig):
        self.sendUpdate('setLeftBroadsideConfig', [leftBroadsideConfig])

    def b_setLeftBroadsideConfig(self, leftBroadsideConfig):
        self.setLeftBroadsideConfig(leftBroadsideConfig)
        self.d_setLeftBroadsideConfig(leftBroadsideConfig)

    def getLeftBroadsideConfig(self):
        return self.leftBroadsideConfig

    def setRightBroadsideConfig(self, rightBroadsideConfig):
        self.rightBroadsideConfig = rightBroadsideConfig

    def d_setRightBroadsideConfig(self, rightBroadsideConfig):
        self.sendUpdate('setRightBroadsideConfig', [rightBroadsideConfig])

    def b_setRightBroadsideConfig(self, rightBroadsideConfig):
        self.setRightBroadsideConfig(rightBroadsideConfig)
        self.d_setRightBroadsideConfig(rightBroadsideConfig)

    def getRightBroadsideConfig(self):
        return self.rightBroadsideConfig

    def setBroadsideAmmo(self, broadsideAmmo):
        self.broadsideAmmo = broadsideAmmo

    def d_setBroadsideAmmo(self, broadsideAmmo):
        self.sendUpdate('setBroadsideAmmo', [broadsideAmmo])

    def b_setBroadsideAmmo(self, broadsideAmmo):
        self.setBroadsideAmmo(broadsideAmmo)
        self.d_setBroadsideAmmo(broadsideAmmo)

    def getBroadsideAmmo(self):
        return self.broadsideAmmo

    def setWallDecorConfig(self, wallDecorConfig):
        self.wallDecorConfig = wallDecorConfig

    def d_setWallDecorConfig(self, wallDecorConfig):
        self.sendUpdate('setWallDecorConfig', [wallDecorConfig])

    def b_setWallDecorConfig(self, wallDecorConfig):
        self.setWallDecorConfig(wallDecorConfig)
        self.d_setWallDecorConfig(wallDecorConfig)

    def getWallDecorConfig(self):
        return self.wallDecorConfig

    def setFloorDecorConfig(self, floorDecorConfig):
        self.floorDecorConfig = floorDecorConfig

    def d_setFloorDecorConfig(self, floorDecorConfig):
        self.sendUpdate('setFloorDecorConfig', [floorDecorConfig])

    def b_setFloorDecorConfig(self, floorDecorConfig):
        self.setFloorDecorConfig(floorDecorConfig)
        self.d_setFloorDecorConfig(floorDecorConfig)

    def getFloorDecorConfig(self):
        return self.floorDecorConfig

class DistributedHullAI(DistributedShippartAI, DistributedHullDNA, DistributedDestructibleArrayAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHullAI')

    def __init__(self, air):
        DistributedShippartAI.__init__(self, air)
        DistributedHullDNA.__init__(self)
        DistributedDestructibleArrayAI.__init__(self, air)

        self.maxSp = 0
        self.sp = 0
        self.maxCargo = 0

    def setMaxSp(self, maxSp):
        self.maxSp = maxSp

    def d_setMaxSp(self, maxSp):
        self.sendUpdate('setMaxSp', [maxSp])

    def b_setMaxSp(self, maxSp):
        self.setMaxSp(maxSp)
        self.d_setMaxSp(maxSp)

    def getMaxSp(self):
        return self.maxSp

    def setSp(self, sp):
        self.sp = sp

    def d_setSp(self, sp):
        self.sendUpdate('setSp', [sp])

    def b_setSp(self, sp):
        self.setSp(sp)
        self.d_setSp(sp)

    def getSp(self):
        return self.sp

    def setMaxCargo(self, maxCargo):
        self.maxCargo = maxCargo

    def d_setMaxCargo(self, maxCargo):
        self.sendUpdate('setMaxCargo', [maxCargo])

    def b_setMaxCargo(self, maxCargo):
        self.setMaxCargo(maxCargo)
        self.d_setMaxCargo(maxCargo)

    def getMaxCargo(self):
        return self.maxCargo
