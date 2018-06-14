from pirates.shipparts.DistributedShippartAI import DistributedShippartAI
from direct.directnotify import DirectNotifyGlobal
from pirates.destructibles.DistributedDestructibleArrayAI import DistributedDestructibleArrayAI
from pirates.ship import ShipGlobals

class DistributedMastDNA:

    def __init__(self):
        self.shipClass = 0
        self.baseTeam = 0

        self.mastType = 0
        self.posIndex = 0
        self.sailConfig = []
        self.textureIndex = 0
        self.colorIndex = 0

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

    def setMastType(self, mastType):
        self.mastType = mastType

    def d_setMastType(self, mastType):
        self.sendUpdate('setMastType', [mastType])

    def b_setMastType(self, mastType):
        self.setMastType(mastType)
        self.d_setMastType(mastType)

    def getMastType(self):
        return self.mastType

    def setPosIndex(self, posIndex):
        self.posIndex = posIndex

    def d_setPosIndex(self, posIndex):
        self.sendUpdate('setPosIndex', [posIndex])

    def b_setPosIndex(self, posIndex):
        self.setPosIndex(posIndex)
        self.d_setPosIndex(posIndex)

    def getPosIndex(self):
        return self.posIndex

    def setSailConfig(self, sailConfig):
        self.sailConfig = sailConfig

    def d_setSailConfig(self, sailConfig):
        self.sendUpdate('setSailConfig', [sailConfig])

    def b_setSailConfig(self, sailConfig):
        self.setSailConfig(sailConfig)
        self.d_setSailConfig(sailConfig)

    def getSailConfig(self):
        return self.sailConfig

    def setTextureIndex(self, textureIndex):
        self.textureIndex = textureIndex

    def d_setTextureIndex(self, textureIndex):
        self.sendUpdate('setTextureIndex', [textureIndex])

    def b_setTextureIndex(self, textureIndex):
        self.setTextureIndex(textureIndex)
        self.d_setTextureIndex(textureIndex)

    def getTextureIndex(self):
        return self.textureIndex

    def setColorIndex(self, colorIndex):
        self.colorIndex = colorIndex

    def d_setColorIndex(self, colorIndex):
        self.sendUpdate('setColorIndex', [colorIndex])

    def b_setColorIndex(self, colorIndex):
        self.setColorIndex(colorIndex)
        self.d_setColorIndex(colorIndex)

    def getColorIndex(self):
        return self.colorIndex

class DistributedMastAI(DistributedShippartAI, DistributedMastDNA, DistributedDestructibleArrayAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMastAI')

    def __init__(self, air):
        DistributedShippartAI.__init__(self, air)
        DistributedMastDNA.__init__(self)
        DistributedDestructibleArrayAI.__init__(self, air)

    def d_setBreakAnim(self, index, animMultiplier):
        self.sendUpdate('setBreakAnim', [index, animMultiplier])
