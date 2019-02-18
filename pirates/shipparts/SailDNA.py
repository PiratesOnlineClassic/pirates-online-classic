from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
from otp.speedchat import ColorSpace
from pirates.ship import ShipGlobals
from pirates.piratesbase import PiratesGlobals
notify = directNotify.newCategory('SailDNA')
SailTextureDict = {
    1: 'ship_sail',
    202: 'ship_sailBP'}
LogoDict = {
    200: 'logo_redSkull',
    201: 'ship_sailBP_patches',
    202: 'logo_eitc',
    203: 'logo_eitc_emblem',
    210: 'logo_french_flag',
    211: 'logo_spanish_flag'}
DefaultAnimDict = (('Idle', 'idle'), ('Hit', 'hit'), ('Billow', 'billow'), ('Rolldown', 'rolldown'), ('Hidden', 'hidden'))
SailColors = [
    VBase4(1.0, 1.0, 1.0, 1.0),
    VBase4(0.0, 0.0, 0.0, 1.0),
    VBase4(0.933594, 0.265625, 0.28125, 1.0),
    VBase4(0.863281, 0.40625, 0.417969, 1.0),
    VBase4(0.710938, 0.234375, 0.4375, 1.0),
    VBase4(0.992188, 0.480469, 0.167969, 1.0),
    VBase4(0.996094, 0.898438, 0.320312, 1.0),
    VBase4(0.550781, 0.824219, 0.324219, 1.0),
    VBase4(0.242188, 0.742188, 0.515625, 1.0),
    VBase4(0.433594, 0.90625, 0.835938, 1.0),
    VBase4(0.347656, 0.820312, 0.953125, 1.0),
    VBase4(0.191406, 0.5625, 0.773438, 1.0)
]


class SailDNA(AvatarDNA.AvatarDNA):
    
    def __init__(self):
        self.baseTeam = PiratesGlobals.INVALID_TEAM
        self.mastType = 0
        self.mastPosIndex = 0
        self.sailType = 0
        self.posIndex = 0
        self.textureIndex = 0
        self.colorIndex = 0
        self.logoIndex = 0

    def __str__(self):
        string = 'mastType %s, sailType %s, posIndex %s, textureIndex %s, colorIndex %s, logoIndex %s' % (self.mastType, self.sailType, self.posIndex, self.textureIndex, self.colorIndex, self.logoIndex)
        return string
    
    def getMastClass(self):
        if self.mastType >= ShipGlobals.MAINMASTL1 and self.mastType <= ShipGlobals.MAINMASTL5:
            return 'mainmast'
        elif self.mastType >= ShipGlobals.TRIMASTL1 and self.mastType <= ShipGlobals.TRIMASTL5:
            return 'trimast'
        elif self.mastType >= ShipGlobals.FOREMASTL1 and self.mastType <= ShipGlobals.FOREMASTL3:
            return 'foremast'
        elif self.mastType >= ShipGlobals.AFTMASTL1 and self.mastType <= ShipGlobals.AFTMASTL3:
            return 'aftmast'
        else:
            return None

    def setBaseTeam(self, val):
        self.baseTeam = val

    def setMastType(self, val):
        self.mastType = val

    def setMastPosIndex(self, val):
        self.mastPosIndex = val

    def setSailType(self, val):
        self.sailType = val

    def setPosIndex(self, val):
        self.posIndex = val

    def setTextureIndex(self, val):
        self.textureIndex = val

    def setColorIndex(self, val):
        self.colorIndex = val

    def setLogoIndex(self, val):
        self.logoIndex = val
    
    def getBaseTeam(self):
        return self.baseTeam

    def getMastType(self):
        return self.mastType

    def getMastPosIndex(self):
        return self.mastPosIndex

    def getSailType(self):
        return self.sailType

    def getPosIndex(self):
        return self.posIndex

    def getTextureIndex(self):
        return self.textureIndex

    def getColorIndex(self):
        return self.colorIndex

    def getLogoIndex(self):
        return self.logoIndex

