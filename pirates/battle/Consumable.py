import Weapon
import WeaponGlobals
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
from pirates.uberdog.UberDogGlobals import InventoryType
__modelTypes = {
    InventoryType.Potion1: ('models/props/largejug_B', Vec4(1, 1, 1, 1), 0.24),
    InventoryType.Potion2: ('models/props/largejug_B', Vec4(1, 0, 0, 1), 0.24),
    InventoryType.Potion3: ('models/props/largejug_B', Vec4(0.2, 0.2, 1, 1), 0.24),
    InventoryType.Potion4: ('models/props/largejug_B', Vec4(0.2, 1.0, 0.2, 1), 0.24),
    InventoryType.Potion5: ('models/props/largejug_B', Vec4(0.7, 0.2, 1, 1), 0.24),
    InventoryType.ShipRepairKit: ('models/props/largejug_B', Vec4(1, 0.6, 1, 1), 0.24),
    InventoryType.PorkChunk: ('models/handheld/pir_m_hnd_foo_porktonic', Vec4(1, 1, 1, 1), 1.0)}

def getImage(itemId):
    return None


def getModel(itemId):
    modelData = __modelTypes.get(itemId)
    model = loader.loadModel(modelData[0])
    model.setColor(modelData[1])
    model.setScale(modelData[2])
    return model

hitSfxs = None
repairSfxs = None
missSfxs = None
eatSfxs = None

def getDrinkSfx():
    global hitSfxs
    if not hitSfxs:
        hitSfxs = (loader.loadSfx('audio/sfx_tonic_drink.mp3'),)
    
    return hitSfxs


def getShipRepairSfx():
    global repairSfxs
    if not repairSfxs:
        repairSfxs = (loader.loadSfx('audio/sfx_ship_teleport_in.mp3'),)
    
    return repairSfxs


def getMissSfx():
    global missSfxs
    if not missSfxs:
        missSfxs = (loader.loadSfx('audio/whoosh-10.mp3'), loader.loadSfx('audio/arm-Whoosh-05.mp3'))
    
    return missSfxs


def getEatSfx():
    global eatSfxs
    if not eatSfxs:
        eatSfxs = loader.loadSfx('audio/sfx_eat_meat.mp3')
    
    return eatSfxs


class Consumable(Weapon.Weapon):
    notify = DirectNotifyGlobal.directNotify.newCategory('Consumable')
    
    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'consumable')

    def loadModel(self):
        self.prop = getModel(self.itemId)
        self.prop.reparentTo(self)
        if self.itemId != InventoryType.PorkChunk:
            self.prop.setHpr(0, -90, 0)
            self.prop.setPos(0, -0.3, -0.1)
        else:
            self.prop.setHpr(0, 0, 0)
            self.prop.setPos(0, 0, 0)
        self.prop.flattenLight()
        coll = self.prop.find('**/Collision*')
        if not coll.isEmpty():
            coll.stash()
        else:
            self.notify.warning('Collision not found!')


