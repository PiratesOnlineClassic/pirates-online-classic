from panda3d.core import *
from direct.directnotify.DirectNotifyGlobal import *
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
from otp.speedchat import ColorSpace
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.ship import ShipGlobals
notify = directNotify.newCategory('CannonDNA')
CannonDict = {
    InventoryType.CannonL1: 'models/shipparts/cannon',
    InventoryType.CannonL2: 'models/shipparts/cannon',
    InventoryType.CannonL3: 'models/shipparts/cannon',
    ShipGlobals.TUTORIAL_CANNON: 'models/shipparts/cannon',
    ShipGlobals.SKEL_CANNON_L1: 'models/shipparts/GP_cannon',
    ShipGlobals.SKEL_CANNON_L2: 'models/shipparts/GP_cannon',
    ShipGlobals.SKEL_CANNON_L3: 'models/shipparts/GP_cannon',
    ShipGlobals.BPCANNON: 'models/shipparts/cannon_bp'}

class CannonDNA(AvatarDNA.AvatarDNA):
    
    def __init__(self):
        self.baseTeam = 0
        self.cannonType = 0
        self.ammoType = InventoryType.CannonRoundShot

    def __str__(self):
        string = 'decorType %s, posIndex %s, colorIndex %s' % (self.decorType, self.posIndex, self.colorIndex)
        return string
    
    def setBaseTeam(self, val):
        self.baseTeam = val

    def setCannonType(self, val):
        self.cannonType = val

    def getBaseTeam(self):
        return self.baseTeam

    def getCannonType(self):
        return self.cannonType

