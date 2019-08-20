from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
from otp.speedchat import ColorSpace
from pirates.ship import ShipGlobals
from pirates.piratesbase import PiratesGlobals
notify = directNotify.newCategory('BowSpritDNA')
BowSpritDict = {
    ShipGlobals.SKELETON: 'models/shipparts/prow_skeleton',
    ShipGlobals.LADY: 'models/shipparts/prow_female',
    ShipGlobals.RAML3: 'models/shipparts/ram_spike',
    ShipGlobals.SKEL_RAML3: 'models/shipparts/skel_ram_spike'}
ProwColors = [
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


class BowSpritDNA(AvatarDNA.AvatarDNA):
    
    def __init__(self):
        self.baseTeam = PiratesGlobals.INVALID_TEAM
        self.prowType = 0
        self.posIndex = 0
        self.colorIndex = 0

    def __str__(self):
        string = 'prowType %s, posIndex %s, colorIndex %s' % (self.prowType, self.posIndex, self.colorIndex)
        return string
    
    def prowIsRam(self, prowIndex):
        if prowIndex >= ShipGlobals.RAML1:
            return 1
        
        return 0
    
    def setBaseTeam(self, val):
        self.baseTeam = val

    def setProwType(self, val):
        self.prowType = val

    def setPosIndex(self, val):
        self.posIndex = val

    def setColorIndex(self, val):
        self.colorIndex = val

    def getBaseTeam(self):
        return self.baseTeam

    def getProwType(self):
        return self.prowType

    def getPosIndex(self):
        return self.posIndex

    def getColorIndex(self):
        return self.colorIndex
