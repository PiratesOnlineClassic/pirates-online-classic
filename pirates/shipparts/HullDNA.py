from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
from otp.speedchat import ColorSpace
from pirates.ship import ShipGlobals
from pirates.piratesbase import PiratesGlobals
notify = directNotify.newCategory('HullDNA')
HullDict = {
    ShipGlobals.DINGHY: 'models/shipparts/dingy',
    ShipGlobals.WARSHIPL1: 'models/shipparts/warshipL1',
    ShipGlobals.WARSHIPL2: 'models/shipparts/warshipL2',
    ShipGlobals.WARSHIPL3: 'models/shipparts/warshipL3',
    ShipGlobals.WARSHIPL4: 'models/shipparts/warshipL4',
    ShipGlobals.MERCHANTL1: 'models/shipparts/merchantL1',
    ShipGlobals.MERCHANTL2: 'models/shipparts/merchantL2',
    ShipGlobals.MERCHANTL3: 'models/shipparts/merchantL3',
    ShipGlobals.MERCHANTL4: 'models/shipparts/merchantL4',
    ShipGlobals.INTERCEPTORL1: 'models/shipparts/interceptorL1',
    ShipGlobals.INTERCEPTORL2: 'models/shipparts/interceptorL2',
    ShipGlobals.INTERCEPTORL3: 'models/shipparts/interceptorL3',
    ShipGlobals.INTERCEPTORL4: 'models/shipparts/interceptorL4',
    ShipGlobals.BLACK_PEARL: 'models/shipparts/blackpearl',
    ShipGlobals.GOLIATH: 'models/shipparts/goliath',
    ShipGlobals.SKEL_WARSHIPL3: 'models/shipparts/skeletonWarshipL3',
    ShipGlobals.SKEL_INTERCEPTORL3: 'models/shipparts/skeletonInterceptorL3'}
HullFlatDict = {
    ShipGlobals.DINGHY: 'models/shipparts/dingy',
    ShipGlobals.WARSHIPL1: 'models/shipparts/warship-geometry_Flat',
    ShipGlobals.WARSHIPL2: 'models/shipparts/warship-geometry_Flat',
    ShipGlobals.WARSHIPL3: 'models/shipparts/warship-geometry_Flat',
    ShipGlobals.WARSHIPL4: 'models/shipparts/warship-geometry_Flat',
    ShipGlobals.MERCHANTL1: 'models/shipparts/merchant-geometry_Flat',
    ShipGlobals.MERCHANTL2: 'models/shipparts/merchant-geometry_Flat',
    ShipGlobals.MERCHANTL3: 'models/shipparts/merchant-geometry_Flat',
    ShipGlobals.MERCHANTL4: 'models/shipparts/merchant-geometry_Flat',
    ShipGlobals.INTERCEPTORL1: 'models/shipparts/interceptor-geometry_Flat',
    ShipGlobals.INTERCEPTORL2: 'models/shipparts/interceptor-geometry_Flat',
    ShipGlobals.INTERCEPTORL3: 'models/shipparts/interceptor-geometry_Flat',
    ShipGlobals.INTERCEPTORL4: 'models/shipparts/interceptor-geometry_Flat',
    ShipGlobals.BLACK_PEARL: 'models/shipparts/blackpearl-geometry_Low',
    ShipGlobals.GOLIATH: 'models/shipparts/warship-geometry_Flat',
    ShipGlobals.SKEL_WARSHIPL3: 'models/shipparts/skeletonWarshipL3-geometry_Flat',
    ShipGlobals.SKEL_INTERCEPTORL3: 'models/shipparts/skeletonInterceptorL3-geometry_Flat'}
HullTexDict = {
    2: ('ship_hull_wood_1_dirty', 'ship_grunge_lichen_multi'),
    101: ('ship_hull_wood_1_dirty', None),
    102: ('ship_wood_goldish', None),
    180: ('ship_skel_hullwood_3', None),
    181: ('ship_skel_hullwood_4', None),
    250: ('ship_et_wood_A', None),
    251: ('ship_bp_hull_wood_1', None),
    252: ('ship_bp_hull_wood_2', None),
    253: ('ship_hull_wood_3_unsat', None),
    254: ('ship_wood_gold', None),
    255: ('ship_hull_wood_3_dirty', None)}
StripeTexDict = {
    1: ('ship_trim_red', None),
    2: ('ship_trim_red', None),
    3: ('ship_trim_red', None),
    180: ('ship_skel_trim_gold_3', None),
    200: ('ship_trim_navy_gold', None),
    201: ('ship_trim_navy_wood', None),
    202: ('ship_trim_gold', None),
    203: ('ship_trim_navy_window', None),
    204: ('ship_et_trim_A', None),
    205: ('ship_et_trim_B', None),
    206: ('ship_et_trim_C', None)}
PatternTexDict = {
    1: ('ship_pattern_r_b', None),
    200: ('ship_pattern_navy', None),
    208: ('ship_et_pattern_A', None)}
HullColors = [
    VBase4(1.0, 1.0, 1.0, 1.0),
    VBase4(0.0, 0.0, 0.0, 1.0),
    VBase4(0.933594, 0.265625, 0.28125, 1.0),
    VBase4(0.863281, 0.40625, 0.417969, 1.0),
    VBase4(1.0, 0.0, 0.0, 1.0),
    VBase4(0.7, 0.5, 0.3, 1.0),
    VBase4(0.6, 0.0, 0.0, 1.0),
    VBase4(0.710938, 0.234375, 0.4375, 1.0),
    VBase4(0.992188, 0.480469, 0.167969, 1.0),
    VBase4(0.996094, 0.898438, 0.320312, 1.0),
    VBase4(0.550781, 0.824219, 0.324219, 1.0),
    VBase4(0.242188, 0.742188, 0.515625, 1.0),
    VBase4(0.433594, 0.90625, 0.835938, 1.0),
    VBase4(0.347656, 0.820312, 0.953125, 1.0),
    VBase4(0.191406, 0.5625, 0.773438, 1.0),
    VBase4(0.63, 0.172, 0.088, 1.0),
    VBase4(1.0, 0.272, 0.139, 1.0),
    VBase4(0.4, 0.4, 0.4, 1.0),
    VBase4(0.2, 0.2, 0.2, 1.0),
    VBase4(0.4, 0.5, 0.8, 1.0)
]


class HullDNA(AvatarDNA.AvatarDNA):
    
    def __init__(self):
        self.shipClass = 0
        self.modelClass = 0
        self.baseTeam = PiratesGlobals.INVALID_TEAM
        self.hullTextureIndex = []
        self.stripeTextureIndex = []
        self.patternTextureIndex = []
        self.hullColorIndex = []
        self.stripeColorIndex = []
        self.patternColorIndex = []
        self.hullHilightColorIndex = []
        self.stripeHilightColorIndex = []
        self.patternHilightColorIndex = []
        self.mastConfig1 = 0
        self.mastConfig2 = 0
        self.mastConfig3 = 0
        self.foremastConfig = 0
        self.aftmastConfig = 0
        self.sailConfig1 = []
        self.sailConfig2 = []
        self.sailConfig3 = []
        self.mastTextureIndex = 0
        self.sailTextureIndex = 0
        self.sailLogoIndex = 0
        self.foresailConfig = []
        self.aftsailConfig = []
        self.cannonConfig = []
        self.leftBroadsideConfig = []
        self.rightBroadsideConfig = []
        self.broadsideAmmo = 0
        self.cannonAmmo = 0
        self.cannonType = 0
        self.wallDecorConfig = []
        self.floorDecorConfig = []
        self.prowType = 0
        self.ramType = 0
        self.cabinType = 0
        self.cabinMastConfig = []
        self.cabinCannonConfig = []
        self.cabinWallDecorConfig = []
        self.cabinWindowConfig = []
    
    def __str__(self):
        string = 'shipClass %s, hullTextureColor %s:%s:%s, stripeTextureColor %s:%s:%s, patternTextureColor %s:%s:%s, mastConfig1 %s:%s, mastConfig2 %s:%s, mastConfig3 %s:%s, foremastConfig %s:%s, aftmastConfig %s:%s, cannonConfig %s, leftBroadsideConfig %s, rightBroadsideConfig %s, wallDecorConfig %s, floorDecorConfig %s, prowType %s, ramType %s, cabinType %s' % (self.shipClass, self.hullTextureIndex, self.hullColorIndex, self.hullHilightColorIndex, self.stripeTextureIndex, self.stripeColorIndex, self.stripeHilightColorIndex, self.patternTextureIndex, self.patternColorIndex, self.patternHilightColorIndex, self.mastConfig1, self.sailConfig1, self.mastConfig2, self.sailConfig2, self.mastConfig3, self.sailConfig3, self.foremastConfig, self.foresailConfig, self.aftmastConfig, self.aftsailConfig, self.cannonConfig, self.leftBroadsideConfig, self.rightBroadsideConfig, self.wallDecorConfig, self.floorDecorConfig, self.prowType, self.ramType, self.cabinType)
        return string

    def setShipClass(self, val):
        self.shipClass = val
        self.modelClass = ShipGlobals.getModelClass(val)

    def setBaseTeam(self, val):
        self.baseTeam = val

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

    def setMastConfig1(self, val):
        self.mastConfig1 = val

    def setMastConfig2(self, val):
        self.mastConfig2 = val

    def setMastConfig3(self, val):
        self.mastConfig3 = val

    def setForemastConfig(self, val):
        self.foremastConfig = val

    def setAftmastConfig(self, val):
        self.aftmastConfig = val

    def setSailConfig1(self, val):
        self.sailConfig1 = val

    def setSailConfig2(self, val):
        self.sailConfig2 = val

    def setSailConfig3(self, val):
        self.sailConfig3 = val

    def setForesailConfig(self, val):
        self.foresailConfig = val

    def setAftsailConfig(self, val):
        self.aftsailConfig = val

    def setCannonConfig(self, val):
        self.cannonConfig = val

    def setLeftBroadsideConfig(self, val):
        self.leftBroadsideConfig = val

    def setRightBroadsideConfig(self, val):
        self.rightBroadsideConfig = val

    def setBroadsideAmmo(self, val):
        self.broadsideAmmo = val

    def setWallDecorConfig(self, val):
        self.wallDecorConfig = val

    def setFloorDecorConfig(self, val):
        self.floorDecorConfig = val

    def setProwType(self, val):
        self.prowType = val

    def setRamType(self, val):
        self.ramType = val

    def setCabinType(self, val):
        self.cabinType = val

    def getShipClass(self):
        return self.shipClass

    def getModelClass(self):
        return self.modelClass

    def getBaseTeam(self):
        return self.baseTeam

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

    def getMastConfig1(self):
        return self.mastConfig1

    def getMastConfig2(self):
        return self.mastConfig2

    def getMastConfig3(self):
        return self.mastConfig3

    def getForemastConfig(self):
        return self.foremastConfig

    def getAftmastConfig(self):
        return self.aftmastConfig

    def getSailConfig1(self):
        return self.sailConfig1

    def getSailConfig2(self):
        return self.sailConfig2

    def getSailConfig3(self):
        return self.sailConfig3

    def getForesailConfig(self):
        return self.foresailConfig

    def getAftsailConfig(self):
        return self.aftsailConfig

    def getCannonConfig(self):
        return self.cannonConfig

    def getLeftBroadsideConfig(self):
        return self.leftBroadsideConfig

    def getRightBroadsideConfig(self):
        return self.rightBroadsideConfig

    def getBroadsideAmmo(self):
        return self.broadsideAmmo

    def getWallDecorConfig(self):
        return self.wallDecorConfig

    def getFloorDecorConfig(self):
        return self.floorDecorConfig

    def getProwType(self):
        return self.prowType

    def getRamType(self):
        return self.ramType

    def getCabinType(self):
        return self.cabinType

