from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
from otp.speedchat import ColorSpace
from pirates.piratesbase import PiratesGlobals
from pirates.ship import ShipGlobals
notify = directNotify.newCategory('CabinDNA')
CabinDict = {
    ShipGlobals.WAR_CABINL1A: 'models/shipparts/warCabinAL1',
    ShipGlobals.WAR_CABINL2A: 'models/shipparts/warCabinAL2',
    ShipGlobals.WAR_CABINL3A: 'models/shipparts/warCabinAL3',
    ShipGlobals.MERCH_CABINL1A: 'models/shipparts/merchantCabinAL1',
    ShipGlobals.MERCH_CABINL2A: 'models/shipparts/merchantCabinAL2',
    ShipGlobals.MERCH_CABINL3A: 'models/shipparts/merchantCabinAL3',
    ShipGlobals.INT_CABINL1A: 'models/shipparts/interceptorCabinAL1',
    ShipGlobals.INT_CABINL2A: 'models/shipparts/interceptorCabinAL2',
    ShipGlobals.INT_CABINL3A: 'models/shipparts/interceptorCabinAL3',
    ShipGlobals.BLACK_PEARL_CABIN: 'models/shipparts/blackpearlCabin',
    ShipGlobals.GOLIATH_CABIN: 'models/shipparts/goliathCabinA',
    ShipGlobals.SKEL_WAR_CABINL3A: 'models/shipparts/skeletonWarCabinAL3'}

class CabinDNA(AvatarDNA.AvatarDNA):
    
    def __init__(self):
        self.shipClass = 0
        self.modelClass = 0
        self.baseTeam = PiratesGlobals.INVALID_TEAM
        self.cabinType = 0
        self.hullTextureIndex = []
        self.stripeTextureIndex = []
        self.patternTextureIndex = []
        self.hullColorIndex = []
        self.stripeColorIndex = []
        self.patternColorIndex = []
        self.hullHilightColorIndex = []
        self.stripeHilightColorIndex = []
        self.patternHilightColorIndex = []
        self.mastConfig = []
        self.cannonConfig = []
        self.wallDecorConfig = []
        self.floorDecorConfig = []
        self.windowConfig = []

    def __str__(self):
        string = 'shipClass %s, cabinType %s, hullTextureColor %s:%s:%s, stripeTextureColor %s:%s:%s, mastConfig %s, cannonConfig %s, wallDecorConfig %s, floorDecorConfig %s, windowConfig %s' % (self.shipClass, self.cabinType, self.hullTextureIndex, self.hullColorIndex, self.hullHilightColorIndex, self.stripeTextureIndex, self.stripeColorIndex, self.stripeHilightColorIndex, self.mastConfig, self.cannonConfig, self.wallDecorConfig, self.floorDecorConfig, self.windowConfig)
        return string
    
    def setShipClass(self, val):
        self.shipClass = val
        self.modelClass = ShipGlobals.getModelClass(val)

    def setBaseTeam(self, val):
        self.baseTeam = val

    def setCabinType(self, val):
        self.cabinType = val

    def setHullTextureIndex(self, val):
        self.hullTextureIndex = val

    def setStripeTextureIndex(self, val):
        self.stripeTextureIndex = val

    def setPatternTextureIndex(self, val):
        self.patternTextureIndex = val

    def setHullColorIndex(self, val):
        self.hullColorIndex = val

    def setStripeColorIndex(self, val):
        self.stripeColorIndex = val

    def setPatternColorIndex(self, val):
        self.patternColorIndex = val

    def setHullHilightColorIndex(self, val):
        self.hullHilightColorIndex = val

    def setStripeHilightColorIndex(self, val):
        self.stripeHilightColorIndex = val

    def setPatternHilightColorIndex(self, val):
        self.patternHilightColorIndex = val

    def setMastConfig(self, val):
        self.mastConfig = val

    def setCannonConfig(self, val):
        self.cannonConfig = val

    def setWallDecorConfig(self, val):
        self.wallDecorConfig = val

    def setFloorDecorConfig(self, val):
        self.floorDecorConfig = val

    def setWindowConfig(self, val):
        self.windowConfig = val

    def getShipClass(self):
        return self.shipClass

    def getModelClass(self):
        return self.modelClass

    def getBaseTeam(self):
        return self.baseTeam

    def getCabinType(self):
        return self.cabinType

    def getHullTextureIndex(self):
        return self.hullTextureIndex

    def getStripeTextureIndex(self):
        return self.stripeTextureIndex

    def getPatternTextureIndex(self):
        return self.patternTextureIndex

    def getHullColorIndex(self):
        return self.hullColorIndex

    def getStripeColorIndex(self):
        return self.stripeColorIndex

    def getPatternColorIndex(self):
        return self.patternColorIndex

    def getHullHilightColorIndex(self):
        return self.hullHilightColorIndex

    def getStripeHilightColorIndex(self):
        return self.stripeHilightColorIndex

    def getPatternHilightColorIndex(self):
        return self.patternHilightColorIndex

    def getMastConfig(self):
        return self.mastConfig

    def getCannonConfig(self):
        return self.cannonConfig

    def getWallDecorConfig(self):
        return self.wallDecorConfig

    def getFloorDecorConfig(self):
        return self.floorDecorConfig

    def getWindowConfig(self):
        return self.windowConfig

