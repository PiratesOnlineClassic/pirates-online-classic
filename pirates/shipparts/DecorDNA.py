# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.shipparts.DecorDNA
import random

from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
from otp.speedchat import ColorSpace
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.ship import ShipGlobals

notify = directNotify.newCategory('DecorDNA')
WALL = 1
FLOOR = 2
WINDOW = 3
DecorDict = {1: ('models/shipparts/old_wallLanternB', FLOOR), 2: ('models/shipparts/lantern_wall', WALL), 3: ('models/shipparts/lantern_standing', FLOOR), 50: ('models/shipparts/skullhead', WALL), 51: ('models/props/barrel', FLOOR), 200: ('models/shipparts/window_small', WINDOW), 201: ('models/shipparts/window_med', WINDOW), 202: ('models/shipparts/window_arched', WINDOW)}
SkelDecorDict = {1: ('models/shipparts/old_wallLanternB', FLOOR), 2: ('models/shipparts/lantern_wall', WALL), 3: ('models/shipparts/lantern_standing', FLOOR), 50: ('models/shipparts/skullhead', WALL), 51: ('models/props/barrel', FLOOR), 200: ('models/shipparts/window', WINDOW), 201: ('models/shipparts/wideWindow', WINDOW)}

def getDecorType(index):
    if index < 50:
        return 'lantern'
    else:
        if index >= 50 and index < 200:
            return 'decoration'
        else:
            if index >= 200:
                return 'window'


DecorColors = [
 VBase4(1.0, 1.0, 1.0, 1.0), VBase4(0.0, 0.0, 0.0, 1.0), VBase4(0.933594, 0.265625, 0.28125, 1.0), VBase4(0.863281, 0.40625, 0.417969, 1.0), VBase4(0.710938, 0.234375, 0.4375, 1.0), VBase4(0.992188, 0.480469, 0.167969, 1.0), VBase4(0.996094, 0.898438, 0.320312, 1.0), VBase4(0.550781, 0.824219, 0.324219, 1.0), VBase4(0.242188, 0.742188, 0.515625, 1.0), VBase4(0.433594, 0.90625, 0.835938, 1.0), VBase4(0.347656, 0.820312, 0.953125, 1.0), VBase4(0.191406, 0.5625, 0.773438, 1.0)]

class DecorDNA(AvatarDNA.AvatarDNA):
    __module__ = __name__

    def __init__(self):
        self.baseTeam = PiratesGlobals.INVALID_TEAM
        self.decorType = 0
        self.posIndex = 0
        self.colorIndex = 0

    def __str__(self):
        string = 'decorType %s, posIndex %s, colorIndex %s' % (self.decorType, self.posIndex, self.colorIndex)
        return string

    def setBaseTeam(self, val):
        self.baseTeam = val

    def setDecorType(self, val):
        self.decorType = val

    def setPosIndex(self, val):
        self.posIndex = val

    def setColorIndex(self, val):
        self.colorIndex = val

    def getBaseTeam(self):
        return self.baseTeam

    def getDecorType(self):
        return self.decorType

    def getPosIndex(self):
        return self.posIndex

    def getColorIndex(self):
        return self.colorIndex
# okay decompiling .\pirates\shipparts\DecorDNA.pyc
