# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.shipparts.CannonDNA
import random

from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
from otp.speedchat import ColorSpace
from pandac.PandaModules import *
from pirates.ship import ShipGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

notify = directNotify.newCategory('CannonDNA')
CannonDict = {InventoryType.CannonL1: 'models/shipparts/cannon', InventoryType.CannonL2: 'models/shipparts/cannon', InventoryType.CannonL3: 'models/shipparts/cannon', ShipGlobals.TUTORIAL_CANNON: 'models/shipparts/cannon', ShipGlobals.SKEL_CANNON_L1: 'models/shipparts/GP_cannon', ShipGlobals.SKEL_CANNON_L2: 'models/shipparts/GP_cannon', ShipGlobals.SKEL_CANNON_L3: 'models/shipparts/GP_cannon', ShipGlobals.BPCANNON: 'models/shipparts/cannon_bp'}

class CannonDNA(AvatarDNA.AvatarDNA):
    __module__ = __name__

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
# okay decompiling .\pirates\shipparts\CannonDNA.pyc
