# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.Consumable
from . import Weapon
from . import WeaponGlobals
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.uberdog.UberDogGlobals import InventoryType

__modelTypes = {InventoryType.Potion1: ('models/props/largejug_B', Vec4(1, 1, 1, 1)), InventoryType.Potion2: ('models/props/largejug_B', Vec4(0.6, 0.6, 1, 1)), InventoryType.Potion3: ('models/props/largejug_B', Vec4(1, 0.6, 0.6, 1)), InventoryType.Potion4: ('models/props/largejug_B', Vec4(0.6, 1.0, 0.6, 1)), InventoryType.Potion5: ('models/props/largejug_B', Vec4(1, 0.6, 1, 1)), InventoryType.ShipRepairKit: ('models/props/largejug_B', Vec4(1, 0.6, 1, 1))}

def getImage(itemId):
    return


def getModel(itemId):
    modelData = __modelTypes.get(itemId)
    model = loader.loadModelCopy(modelData[0])
    model.setColor(modelData[1])
    return model


hitSfxs = None
repairSfxs = None
missSfxs = None

def getDrinkSfx():
    global hitSfxs
    if not hitSfxs:
        hitSfxs = (
         loader.loadSfx('audio/sfx_tonic_drink.mp3'),)
    return hitSfxs


def getShipRepairSfx():
    global repairSfxs
    if not repairSfxs:
        repairSfxs = (
         loader.loadSfx('audio/sfx_ship_teleport_in.mp3'),)
    return repairSfxs


def getMissSfx():
    global missSfxs
    if not missSfxs:
        missSfxs = (
         loader.loadSfx('audio/whoosh-10.mp3'), loader.loadSfx('audio/arm-Whoosh-05.mp3'))
    return missSfxs


class Consumable(Weapon.Weapon):
    __module__ = __name__

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'consumable')

    def loadModel(self):
        self.prop = getModel(self.itemId)
        self.prop.reparentTo(self)
        self.prop.setHpr(0, -90, 0)
        self.prop.setScale(0.24)
        self.prop.setPos(0, -0.3, -0.1)
        self.prop.flattenLight()
        coll = self.prop.find('**/Collision')
        coll.stash()
# okay decompiling .\pirates\battle\Consumable.pyc
