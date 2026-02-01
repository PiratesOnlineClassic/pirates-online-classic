import copy
import math
import zlib
import pickle
from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import *
from pirates.battle.EnemySkills import *
from pirates.battle import CannonGlobals
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.economy import EconomyGlobals
from pirates.reputation import RepChart
import random
import os
import copy
from . import Pistol
from . import Sword
from . import Doll
from . import Melee
from . import Dagger
from . import Grenade
from . import Wand
from . import Bayonet
from . import MonsterMelee
from . import Consumable
from . import Weapon
from . import DualCutlass
from . import Foil
from .WeaponConstants import *
__defensiveBuffs = [
    C_TAKECOVER,
    C_OPENFIRE,
    C_ATTUNE,
    C_HASTEN,
    C_REGEN]

def getIsDefensiveBuff(effectId):
    return __defensiveBuffs.count(effectId)

vfs = VirtualFileSystem.getGlobalPtr()
filename = Filename('WeaponGlobals.pkl')
searchPath = DSearchPath()
if __debug__:
    searchPath.appendDirectory(Filename.expandFrom('../resources/phase_2/etc'))
else:
    searchPath.appendDirectory(Filename.expandFrom('phase_2/etc'))
found = vfs.resolveFilename(filename, searchPath)
if not found:
    print('WeaponGlobals.pkl file not found: %s' % filename.cStr())

data = vfs.readFile(filename, 1)
__skillInfo = pickle.loads(zlib.decompress(data))
__attackEffectsSkillInfo = {}
__columnHeadings = __skillInfo.pop('columnHeadings')
for (heading, value) in list(__columnHeadings.items()):
    exec('%s = %s' % (heading, value), globals())

del searchPath
del __columnHeadings
del data
NA = -1
TARGET_SELECT_BUTTON = 'mouse1'
TEAM_COMBO_WINDOW = 2.0
NUM_PLAYER_WEAPONS = 6
COMBAT = 1
FIREARM = 2
GRENADE = 3
VOODOO = 4
STAFF = 5
MELEE = 6
THROWING = 7
CONSUMABLE = 7
SAILING = 8
CANNON = 9
__humanWeapons = {
    InventoryType.MeleeWeaponL1: MELEE,
    InventoryType.MeleeWeaponL2: MELEE,
    InventoryType.MeleeWeaponL3: MELEE,
    InventoryType.MeleeWeaponL4: MELEE,
    InventoryType.MeleeWeaponL5: MELEE,
    InventoryType.MeleeWeaponL6: MELEE,
    InventoryType.CutlassWeaponL1: COMBAT,
    InventoryType.CutlassWeaponL2: COMBAT,
    InventoryType.CutlassWeaponL3: COMBAT,
    InventoryType.CutlassWeaponL4: COMBAT,
    InventoryType.CutlassWeaponL5: COMBAT,
    InventoryType.CutlassWeaponL6: COMBAT,
    InventoryType.PistolWeaponL1: FIREARM,
    InventoryType.PistolWeaponL2: FIREARM,
    InventoryType.PistolWeaponL3: FIREARM,
    InventoryType.PistolWeaponL4: FIREARM,
    InventoryType.PistolWeaponL5: FIREARM,
    InventoryType.PistolWeaponL6: FIREARM,
    InventoryType.MusketWeaponL1: FIREARM,
    InventoryType.MusketWeaponL2: FIREARM,
    InventoryType.MusketWeaponL3: FIREARM,
    InventoryType.BayonetWeaponL1: FIREARM,
    InventoryType.BayonetWeaponL2: FIREARM,
    InventoryType.BayonetWeaponL3: FIREARM,
    InventoryType.DaggerWeaponL1: THROWING,
    InventoryType.DaggerWeaponL2: THROWING,
    InventoryType.DaggerWeaponL3: THROWING,
    InventoryType.DaggerWeaponL4: THROWING,
    InventoryType.DaggerWeaponL5: THROWING,
    InventoryType.DaggerWeaponL6: THROWING,
    InventoryType.GrenadeWeaponL1: GRENADE,
    InventoryType.GrenadeWeaponL2: GRENADE,
    InventoryType.GrenadeWeaponL3: GRENADE,
    InventoryType.GrenadeWeaponL4: GRENADE,
    InventoryType.GrenadeWeaponL5: GRENADE,
    InventoryType.GrenadeWeaponL6: GRENADE,
    InventoryType.WandWeaponL1: STAFF,
    InventoryType.WandWeaponL2: STAFF,
    InventoryType.WandWeaponL3: STAFF,
    InventoryType.WandWeaponL4: STAFF,
    InventoryType.WandWeaponL5: STAFF,
    InventoryType.WandWeaponL6: STAFF,
    InventoryType.DollWeaponL1: VOODOO,
    InventoryType.DollWeaponL2: VOODOO,
    InventoryType.DollWeaponL3: VOODOO,
    InventoryType.DollWeaponL4: VOODOO,
    InventoryType.DollWeaponL5: VOODOO,
    InventoryType.DollWeaponL6: VOODOO,
    InventoryType.KettleWeaponL1: VOODOO,
    InventoryType.KettleWeaponL2: VOODOO,
    InventoryType.KettleWeaponL3: VOODOO,
    InventoryType.Potion1: CONSUMABLE,
    InventoryType.Potion2: CONSUMABLE,
    InventoryType.Potion3: CONSUMABLE,
    InventoryType.Potion4: CONSUMABLE,
    InventoryType.Potion5: CONSUMABLE,
    InventoryType.ShipRepairKit: CONSUMABLE,
    InventoryType.PorkChunk: CONSUMABLE }
__enemyWeapons = {
    InventoryType.MonsterWeaponL1: COMBAT,
    InventoryType.MonsterWeaponL2: COMBAT,
    InventoryType.MonsterWeaponL3: COMBAT,
    InventoryType.MonsterWeaponL4: COMBAT,
    InventoryType.MonsterWeaponL5: COMBAT,
    InventoryType.DualCutlassL1: COMBAT,
    InventoryType.FoilL1: COMBAT}

def getWeaponTypes():
    return list(__humanWeapons.keys()) + list(__enemyWeapons.keys())


def getHumanWeaponTypes():
    return list(__humanWeapons.keys())


def getWeaponCategory(weaponId):
    weaponDict = __humanWeapons.copy()
    weaponDict.update(__enemyWeapons.copy())
    return weaponDict.get(weaponId)

__dcFieldNames = {
    InventoryType.MeleeRep: 'Melee',
    InventoryType.CutlassRep: 'Cutlass',
    InventoryType.PistolRep: 'Pistol',
    InventoryType.MusketRep: 'Musket',
    InventoryType.DaggerRep: 'Dagger',
    InventoryType.GrenadeRep: 'Grenade',
    InventoryType.DollRep: 'Doll',
    InventoryType.WandRep: 'Wand',
    InventoryType.KettleRep: 'Kettle',
    InventoryType.CannonRep: 'Cannon'}
__weaponId2Class = {
    InventoryType.MeleeWeaponL1: Melee.Melee,
    InventoryType.MeleeWeaponL2: Melee.Melee,
    InventoryType.MeleeWeaponL3: Melee.Melee,
    InventoryType.MeleeWeaponL4: Melee.Melee,
    InventoryType.MeleeWeaponL5: Melee.Melee,
    InventoryType.MeleeWeaponL6: Melee.Melee,
    InventoryType.CutlassWeaponL1: Sword.Sword,
    InventoryType.CutlassWeaponL2: Sword.Sword,
    InventoryType.CutlassWeaponL3: Sword.Sword,
    InventoryType.CutlassWeaponL4: Sword.Sword,
    InventoryType.CutlassWeaponL5: Sword.Sword,
    InventoryType.CutlassWeaponL6: Sword.Sword,
    InventoryType.PistolWeaponL1: Pistol.Pistol,
    InventoryType.PistolWeaponL2: Pistol.Pistol,
    InventoryType.PistolWeaponL3: Pistol.Pistol,
    InventoryType.PistolWeaponL4: Pistol.Pistol,
    InventoryType.PistolWeaponL5: Pistol.Pistol,
    InventoryType.PistolWeaponL6: Pistol.Pistol,
    InventoryType.MusketWeaponL1: Bayonet.Bayonet,
    InventoryType.MusketWeaponL2: Bayonet.Bayonet,
    InventoryType.MusketWeaponL3: Bayonet.Bayonet,
    InventoryType.BayonetWeaponL1: Bayonet.Bayonet,
    InventoryType.BayonetWeaponL2: Bayonet.Bayonet,
    InventoryType.BayonetWeaponL3: Bayonet.Bayonet,
    InventoryType.DaggerWeaponL1: Dagger.Dagger,
    InventoryType.DaggerWeaponL2: Dagger.Dagger,
    InventoryType.DaggerWeaponL3: Dagger.Dagger,
    InventoryType.DaggerWeaponL4: Dagger.Dagger,
    InventoryType.DaggerWeaponL5: Dagger.Dagger,
    InventoryType.DaggerWeaponL6: Dagger.Dagger,
    InventoryType.GrenadeWeaponL1: Grenade.Grenade,
    InventoryType.GrenadeWeaponL2: Grenade.Grenade,
    InventoryType.GrenadeWeaponL3: Grenade.Grenade,
    InventoryType.GrenadeWeaponL4: Grenade.Grenade,
    InventoryType.GrenadeWeaponL5: Grenade.Grenade,
    InventoryType.GrenadeWeaponL6: Grenade.Grenade,
    InventoryType.WandWeaponL1: Wand.Wand,
    InventoryType.WandWeaponL2: Wand.Wand,
    InventoryType.WandWeaponL3: Wand.Wand,
    InventoryType.WandWeaponL4: Wand.Wand,
    InventoryType.WandWeaponL5: Wand.Wand,
    InventoryType.WandWeaponL6: Wand.Wand,
    InventoryType.DollWeaponL1: Doll.Doll,
    InventoryType.DollWeaponL2: Doll.Doll,
    InventoryType.DollWeaponL3: Doll.Doll,
    InventoryType.DollWeaponL4: Doll.Doll,
    InventoryType.DollWeaponL5: Doll.Doll,
    InventoryType.DollWeaponL6: Doll.Doll,
    InventoryType.Potion1: Consumable.Consumable,
    InventoryType.Potion2: Consumable.Consumable,
    InventoryType.Potion3: Consumable.Consumable,
    InventoryType.Potion4: Consumable.Consumable,
    InventoryType.Potion5: Consumable.Consumable,
    InventoryType.ShipRepairKit: Consumable.Consumable,
    InventoryType.PorkChunk: Consumable.Consumable,
    InventoryType.MonsterWeaponL1: MonsterMelee.MonsterMelee,
    InventoryType.MonsterWeaponL2: MonsterMelee.MonsterMelee,
    InventoryType.MonsterWeaponL3: MonsterMelee.MonsterMelee,
    InventoryType.MonsterWeaponL4: MonsterMelee.MonsterMelee,
    InventoryType.MonsterWeaponL5: MonsterMelee.MonsterMelee,
    InventoryType.DualCutlassL1: DualCutlass.DualCutlass,
    InventoryType.FoilL1: Foil.Foil}
__weaponClass2Key = {
    Sword.Sword: 1,
    Pistol.Pistol: 2,
    Doll.Doll: 3,
    Dagger.Dagger: 4,
    Grenade.Grenade: 5,
    Wand.Wand: 6}

def getWeaponName(weaponId):
    return PLocalizer.InventoryTypeNames.get(weaponId, 'Unknown')


def getDCFieldName(weaponId):
    return __dcFieldNames[weaponId]


def getWeaponClass(weaponId):
    return __weaponId2Class.get(weaponId)


def getWeaponKey(weaponId):
    return __weaponClass2Key.get(__weaponId2Class.get(weaponId))

WEAPON_MOVIE_CLEAR = 0
WEAPON_MOVIE_START = 1
WEAPON_MOVIE_STOP = 2
LocalAvatarUsingSkill = 'localAvatarUsingSkill'
LocalAvatarUseProjectileSkill = 'localAvatarUseProjectileSkill'
LocalAvatarUseTargetedSkill = 'localAvatarUseTargetedSkill'
LocalAvatarUseShipSkill = 'localAvatarUseShipSkill'
LocalAvatarUseItem = 'localAvatarUseItem'
LocalAvatarSwitchingWeapons = 'localAvatarSwitchingWeapons'
__weaponStatList = {
    InventoryType.MeleeWeaponL1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.MeleeWeaponL2: ([
        0,
        0,
        0,
        0,
        0], [
        -2,
        0,
        0,
        0,
        0]),
    InventoryType.MeleeWeaponL3: ([
        0,
        0,
        0,
        0,
        0], [
        -4,
        0,
        0,
        0,
        0]),
    InventoryType.MeleeWeaponL4: ([
        0,
        0,
        0,
        0,
        0], [
        -6,
        0,
        0,
        0,
        0]),
    InventoryType.MeleeWeaponL5: ([
        0,
        0,
        0,
        0,
        0], [
        -8,
        0,
        0,
        0,
        0]),
    InventoryType.MeleeWeaponL6: ([
        0,
        0,
        0,
        0,
        0], [
        -10,
        0,
        0,
        0,
        0]),
    InventoryType.CutlassWeaponL1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.CutlassWeaponL2: ([
        0,
        0,
        0,
        0,
        0], [
        -2,
        0,
        0,
        0,
        0]),
    InventoryType.CutlassWeaponL3: ([
        0,
        0,
        0,
        0,
        0], [
        -4,
        0,
        0,
        0,
        0]),
    InventoryType.CutlassWeaponL4: ([
        0,
        0,
        0,
        0,
        0], [
        -6,
        0,
        0,
        0,
        0]),
    InventoryType.CutlassWeaponL5: ([
        0,
        0,
        0,
        0,
        0], [
        -8,
        0,
        0,
        0,
        0]),
    InventoryType.CutlassWeaponL6: ([
        0,
        0,
        0,
        0,
        0], [
        -10,
        0,
        0,
        0,
        0]),
    InventoryType.PistolWeaponL1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.PistolWeaponL2: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.PistolWeaponL3: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.PistolWeaponL4: ([
        0,
        0,
        0,
        0,
        0], [
        -1,
        0,
        0,
        0,
        0]),
    InventoryType.PistolWeaponL5: ([
        0,
        0,
        0,
        0,
        0], [
        -2,
        0,
        0,
        0,
        0]),
    InventoryType.PistolWeaponL6: ([
        0,
        0,
        0,
        0,
        0], [
        -3,
        0,
        0,
        0,
        0]),
    InventoryType.MusketWeaponL1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.MusketWeaponL2: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.MusketWeaponL3: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.BayonetWeaponL1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.BayonetWeaponL2: ([
        0,
        0,
        0,
        0,
        0], [
        -2,
        0,
        0,
        0,
        0]),
    InventoryType.BayonetWeaponL3: ([
        0,
        0,
        0,
        0,
        0], [
        -4,
        0,
        0,
        0,
        0]),
    InventoryType.DaggerWeaponL1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.DaggerWeaponL2: ([
        0,
        0,
        0,
        0,
        0], [
        -2,
        0,
        0,
        0,
        0]),
    InventoryType.DaggerWeaponL3: ([
        0,
        0,
        0,
        0,
        0], [
        -4,
        0,
        0,
        0,
        0]),
    InventoryType.DaggerWeaponL4: ([
        0,
        0,
        0,
        0,
        0], [
        -6,
        0,
        0,
        0,
        0]),
    InventoryType.DaggerWeaponL5: ([
        0,
        0,
        0,
        0,
        0], [
        -8,
        0,
        0,
        0,
        0]),
    InventoryType.DaggerWeaponL6: ([
        0,
        0,
        0,
        0,
        0], [
        -10,
        0,
        0,
        0,
        0]),
    InventoryType.GrenadeWeaponL1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.GrenadeWeaponL2: ([
        0,
        0,
        0,
        0,
        0], [
        -2,
        0,
        0,
        0,
        0]),
    InventoryType.GrenadeWeaponL3: ([
        0,
        0,
        0,
        0,
        0], [
        -4,
        0,
        0,
        0,
        0]),
    InventoryType.GrenadeWeaponL4: ([
        0,
        0,
        0,
        0,
        0], [
        -6,
        0,
        0,
        0,
        0]),
    InventoryType.GrenadeWeaponL5: ([
        0,
        0,
        0,
        0,
        0], [
        -8,
        0,
        0,
        0,
        0]),
    InventoryType.GrenadeWeaponL6: ([
        0,
        0,
        0,
        0,
        0], [
        -10,
        0,
        0,
        0,
        0]),
    InventoryType.WandWeaponL1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.WandWeaponL2: ([
        0,
        0,
        0,
        0,
        0], [
        -2,
        0,
        0,
        0,
        0]),
    InventoryType.WandWeaponL3: ([
        0,
        0,
        0,
        0,
        0], [
        -4,
        0,
        0,
        0,
        0]),
    InventoryType.WandWeaponL4: ([
        0,
        0,
        0,
        0,
        0], [
        -6,
        0,
        0,
        0,
        0]),
    InventoryType.WandWeaponL5: ([
        0,
        0,
        0,
        0,
        0], [
        -8,
        0,
        0,
        0,
        0]),
    InventoryType.WandWeaponL6: ([
        0,
        0,
        0,
        0,
        0], [
        -10,
        0,
        0,
        0,
        0]),
    InventoryType.DollWeaponL1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.DollWeaponL2: ([
        0,
        0,
        0,
        0,
        0], [
        -2,
        0,
        0,
        0,
        0]),
    InventoryType.DollWeaponL3: ([
        0,
        0,
        0,
        0,
        0], [
        -4,
        0,
        0,
        0,
        0]),
    InventoryType.DollWeaponL4: ([
        0,
        0,
        0,
        0,
        0], [
        -6,
        0,
        0,
        0,
        0]),
    InventoryType.DollWeaponL5: ([
        0,
        0,
        0,
        0,
        0], [
        -8,
        0,
        0,
        0,
        0]),
    InventoryType.DollWeaponL6: ([
        0,
        0,
        0,
        0,
        0], [
        -10,
        0,
        0,
        0,
        0]),
    InventoryType.KettleWeaponL1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.KettleWeaponL2: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.KettleWeaponL3: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.DualCutlassL1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.FoilL1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.Potion1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.Potion2: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.Potion3: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.Potion4: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.Potion5: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.ShipRepairKit: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.PorkChunk: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.MonsterWeaponL1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.MonsterWeaponL2: ([
        0,
        0,
        0,
        0,
        0], [
        -2,
        0,
        0,
        0,
        0]),
    InventoryType.MonsterWeaponL3: ([
        0,
        0,
        0,
        0,
        0], [
        -4,
        0,
        0,
        0,
        0]),
    InventoryType.MonsterWeaponL4: ([
        0,
        0,
        0,
        0,
        0], [
        -6,
        0,
        0,
        0,
        0]),
    InventoryType.MonsterWeaponL5: ([
        0,
        0,
        0,
        0,
        0], [
        -8,
        0,
        0,
        0,
        0]),
    InventoryType.CannonL1: ([
        0,
        0,
        0,
        0,
        0], [
        0,
        0,
        0,
        0,
        0]),
    InventoryType.CannonL2: ([
        0,
        0,
        0,
        0,
        0], [
        -5,
        0,
        0,
        0,
        0]),
    InventoryType.CannonL3: ([
        0,
        0,
        0,
        0,
        0], [
        -10,
        0,
        0,
        0,
        0])}

def getWeaponStats(itemId):
    entry = __weaponStatList.get(itemId)
    if entry:
        return entry
    else:
        return (None, None)

cutlassScalePVP = 1.6
pistolScalePVP = 0.8
dollScalePVP = 1.25
daggerScalePVP = 1.6
grenadeScalePVP = 0.8
wandScalePVP = 1.6
__weaponDamageScaleList = {
    InventoryType.MeleeWeaponL1: (1.0, 1.0, 2.0),
    InventoryType.MeleeWeaponL2: (1.0, 1.0, 2.0),
    InventoryType.MeleeWeaponL3: (1.0, 1.0, 2.0),
    InventoryType.MeleeWeaponL4: (1.0, 1.0, 2.0),
    InventoryType.MeleeWeaponL5: (1.0, 1.0, 2.0),
    InventoryType.MeleeWeaponL6: (1.0, 1.0, 2.0),
    InventoryType.CutlassWeaponL1: (1.0, 1.0, cutlassScalePVP),
    InventoryType.CutlassWeaponL2: (1.0, 1.0, cutlassScalePVP),
    InventoryType.CutlassWeaponL3: (1.0, 1.0, cutlassScalePVP),
    InventoryType.CutlassWeaponL4: (1.0, 1.0, cutlassScalePVP),
    InventoryType.CutlassWeaponL5: (1.0, 1.0, cutlassScalePVP),
    InventoryType.CutlassWeaponL6: (1.0, 1.0, cutlassScalePVP),
    InventoryType.PistolWeaponL1: (1.0, 1.0, pistolScalePVP),
    InventoryType.PistolWeaponL2: (0.8, 0.7566, pistolScalePVP),
    InventoryType.PistolWeaponL3: (0.7, 0.64, pistolScalePVP),
    InventoryType.PistolWeaponL4: (0.7, 0.64, pistolScalePVP),
    InventoryType.PistolWeaponL5: (0.7, 0.64, pistolScalePVP),
    InventoryType.PistolWeaponL6: (0.7, 0.64, pistolScalePVP),
    InventoryType.MusketWeaponL1: (1.0, 1.0, 1.2),
    InventoryType.MusketWeaponL2: (1.0, 1.0, 1.2),
    InventoryType.MusketWeaponL3: (1.0, 1.0, 1.2),
    InventoryType.BayonetWeaponL1: (1.0, 1.0, 1.4),
    InventoryType.BayonetWeaponL2: (1.0, 1.0, 1.4),
    InventoryType.BayonetWeaponL3: (1.0, 1.0, 1.4),
    InventoryType.DaggerWeaponL1: (1.0, 1.0, daggerScalePVP),
    InventoryType.DaggerWeaponL2: (1.0, 1.0, daggerScalePVP),
    InventoryType.DaggerWeaponL3: (1.0, 1.0, daggerScalePVP),
    InventoryType.DaggerWeaponL4: (1.0, 1.0, daggerScalePVP),
    InventoryType.DaggerWeaponL5: (1.0, 1.0, daggerScalePVP),
    InventoryType.DaggerWeaponL6: (1.0, 1.0, daggerScalePVP),
    InventoryType.GrenadeWeaponL1: (1.0, 1.0, grenadeScalePVP),
    InventoryType.GrenadeWeaponL2: (1.0, 1.0, grenadeScalePVP),
    InventoryType.GrenadeWeaponL3: (1.0, 1.0, grenadeScalePVP),
    InventoryType.GrenadeWeaponL4: (1.0, 1.0, grenadeScalePVP),
    InventoryType.GrenadeWeaponL5: (1.0, 1.0, grenadeScalePVP),
    InventoryType.GrenadeWeaponL6: (1.0, 1.0, grenadeScalePVP),
    InventoryType.WandWeaponL1: (1.0, 1.0, wandScalePVP),
    InventoryType.WandWeaponL2: (1.0, 1.0, wandScalePVP),
    InventoryType.WandWeaponL3: (1.0, 1.0, wandScalePVP),
    InventoryType.WandWeaponL4: (1.0, 1.0, wandScalePVP),
    InventoryType.WandWeaponL5: (1.0, 1.0, wandScalePVP),
    InventoryType.WandWeaponL6: (1.0, 1.0, wandScalePVP),
    InventoryType.DollWeaponL1: (1.0, 1.0, dollScalePVP),
    InventoryType.DollWeaponL2: (1.0, 1.0, dollScalePVP),
    InventoryType.DollWeaponL3: (1.0, 1.0, dollScalePVP),
    InventoryType.DollWeaponL4: (1.0, 1.0, dollScalePVP),
    InventoryType.DollWeaponL5: (1.0, 1.0, dollScalePVP),
    InventoryType.DollWeaponL6: (1.0, 1.0, dollScalePVP),
    InventoryType.DualCutlassL1: (1.0, 1.0, 1.0),
    InventoryType.FoilL1: (1.0, 1.0, 1.0),
    InventoryType.CannonL1: (1.0, 1.0, 1.0),
    InventoryType.CannonL2: (1.0, 1.0, 1.0),
    InventoryType.CannonL3: (1.0, 1.0, 1.0)}
__ammoNPCDamageScaleList = {
    InventoryType.PistolLeadShot: 1.0,
    InventoryType.PistolVenomShot: 1.0,
    InventoryType.PistolBaneShot: 1.0,
    InventoryType.PistolHexEaterShot: 1.0,
    InventoryType.PistolSilverShot: 1.0,
    InventoryType.PistolSteelShot: 1.0,
    InventoryType.GrenadeExplosion: 1.0,
    InventoryType.GrenadeShockBomb: 1.0,
    InventoryType.GrenadeFireBomb: 1.0,
    InventoryType.GrenadeSmokeCloud: 1.0,
    InventoryType.GrenadeSiege: 1.0,
    InventoryType.CannonRoundShot: 1.0,
    InventoryType.CannonChainShot: 1.0,
    InventoryType.CannonGrapeShot: 1.0,
    InventoryType.CannonFirebrand: 0.6,
    InventoryType.CannonThunderbolt: 0.4,
    InventoryType.CannonExplosive: 0.25,
    InventoryType.CannonFury: 0.5,
    InventoryType.CannonGrappleHook: 1.0,
    InventoryType.DaggerAsp: 1.0,
    InventoryType.DaggerAdder: 1.0,
    InventoryType.DaggerSidewinder: 1.0,
    InventoryType.DaggerViperNest: 1.0,
    InventoryType.MusketCrackShot: 1.0,
    InventoryType.MusketMarksman: 1.0,
    InventoryType.MusketLeadShot: 1.0,
    InventoryType.MusketScatterShot: 1.0,
    InventoryType.MusketCursedShot: 1.0,
    InventoryType.MusketCoalfireShot: 1.0,
    InventoryType.MusketHeavySlug: 1.0,
    InventoryType.MusketExploderShot: 1.0}

def getWeaponDamageScale(itemId):
    entry = __weaponDamageScaleList.get(itemId)
    if entry:
        return entry[0]
    else:
        return 1.0


def getAmmoNPCDamageScale(ammoId):
    entry = __ammoNPCDamageScaleList.get(ammoId)
    if entry:
        return entry
    else:
        return 1.0


def getWeaponExperienceScale(itemId):
    entry = __weaponDamageScaleList.get(itemId)
    if entry:
        return entry[1]
    else:
        return 1.0


def getWeaponPvpDamageScale(itemId):
    entry = __weaponDamageScaleList.get(itemId)
    if entry:
        return entry[2]
    else:
        return 1.0

__invId2RepId = {
    InventoryType.MeleeWeaponL1: InventoryType.MeleeRep,
    InventoryType.MeleeWeaponL2: InventoryType.MeleeRep,
    InventoryType.MeleeWeaponL3: InventoryType.MeleeRep,
    InventoryType.MeleeWeaponL4: InventoryType.MeleeRep,
    InventoryType.MeleeWeaponL5: InventoryType.MeleeRep,
    InventoryType.MeleeWeaponL6: InventoryType.MeleeRep,
    InventoryType.CutlassWeaponL1: InventoryType.CutlassRep,
    InventoryType.CutlassWeaponL2: InventoryType.CutlassRep,
    InventoryType.CutlassWeaponL3: InventoryType.CutlassRep,
    InventoryType.CutlassWeaponL4: InventoryType.CutlassRep,
    InventoryType.CutlassWeaponL5: InventoryType.CutlassRep,
    InventoryType.CutlassWeaponL6: InventoryType.CutlassRep,
    InventoryType.DualCutlassL1: InventoryType.CutlassRep,
    InventoryType.FoilL1: InventoryType.CutlassRep,
    InventoryType.PistolWeaponL1: InventoryType.PistolRep,
    InventoryType.PistolWeaponL2: InventoryType.PistolRep,
    InventoryType.PistolWeaponL3: InventoryType.PistolRep,
    InventoryType.PistolWeaponL4: InventoryType.PistolRep,
    InventoryType.PistolWeaponL5: InventoryType.PistolRep,
    InventoryType.PistolWeaponL6: InventoryType.PistolRep,
    InventoryType.MusketWeaponL1: InventoryType.MusketRep,
    InventoryType.MusketWeaponL2: InventoryType.MusketRep,
    InventoryType.MusketWeaponL3: InventoryType.MusketRep,
    InventoryType.BayonetWeaponL1: InventoryType.MusketRep,
    InventoryType.BayonetWeaponL2: InventoryType.MusketRep,
    InventoryType.BayonetWeaponL3: InventoryType.MusketRep,
    InventoryType.DaggerWeaponL1: InventoryType.DaggerRep,
    InventoryType.DaggerWeaponL2: InventoryType.DaggerRep,
    InventoryType.DaggerWeaponL3: InventoryType.DaggerRep,
    InventoryType.DaggerWeaponL4: InventoryType.DaggerRep,
    InventoryType.DaggerWeaponL5: InventoryType.DaggerRep,
    InventoryType.DaggerWeaponL6: InventoryType.DaggerRep,
    InventoryType.GrenadeWeaponL1: InventoryType.GrenadeRep,
    InventoryType.GrenadeWeaponL2: InventoryType.GrenadeRep,
    InventoryType.GrenadeWeaponL3: InventoryType.GrenadeRep,
    InventoryType.GrenadeWeaponL4: InventoryType.GrenadeRep,
    InventoryType.GrenadeWeaponL5: InventoryType.GrenadeRep,
    InventoryType.GrenadeWeaponL6: InventoryType.GrenadeRep,
    InventoryType.WandWeaponL1: InventoryType.WandRep,
    InventoryType.WandWeaponL2: InventoryType.WandRep,
    InventoryType.WandWeaponL3: InventoryType.WandRep,
    InventoryType.WandWeaponL4: InventoryType.WandRep,
    InventoryType.WandWeaponL5: InventoryType.WandRep,
    InventoryType.WandWeaponL6: InventoryType.WandRep,
    InventoryType.DollWeaponL1: InventoryType.DollRep,
    InventoryType.DollWeaponL2: InventoryType.DollRep,
    InventoryType.DollWeaponL3: InventoryType.DollRep,
    InventoryType.DollWeaponL4: InventoryType.DollRep,
    InventoryType.DollWeaponL5: InventoryType.DollRep,
    InventoryType.DollWeaponL6: InventoryType.DollRep,
    InventoryType.KettleWeaponL1: InventoryType.KettleRep,
    InventoryType.KettleWeaponL2: InventoryType.KettleRep,
    InventoryType.KettleWeaponL3: InventoryType.KettleRep,
    InventoryType.MonsterWeaponL1: InventoryType.MonsterRep,
    InventoryType.MonsterWeaponL2: InventoryType.MonsterRep,
    InventoryType.MonsterWeaponL3: InventoryType.MonsterRep,
    InventoryType.MonsterWeaponL4: InventoryType.MonsterRep,
    InventoryType.MonsterWeaponL5: InventoryType.MonsterRep,
    InventoryType.PistolPouchL1: InventoryType.PistolRep,
    InventoryType.PistolPouchL2: InventoryType.PistolRep,
    InventoryType.PistolPouchL3: InventoryType.PistolRep,
    InventoryType.DaggerPouchL1: InventoryType.DaggerRep,
    InventoryType.DaggerPouchL2: InventoryType.DaggerRep,
    InventoryType.DaggerPouchL3: InventoryType.DaggerRep,
    InventoryType.GrenadePouchL1: InventoryType.GrenadeRep,
    InventoryType.GrenadePouchL2: InventoryType.GrenadeRep,
    InventoryType.GrenadePouchL3: InventoryType.GrenadeRep,
    InventoryType.CannonPouchL1: InventoryType.CannonRep,
    InventoryType.CannonPouchL2: InventoryType.CannonRep,
    InventoryType.CannonPouchL3: InventoryType.CannonRep}

def getRepId(inventoryId):
    newId = __invId2RepId.get(inventoryId)
    if newId:
        return newId
    else:
        return 0

PERFECT_ACC = 100.0
HIGH_ACC = 80.0
MED_ACC = 60.0
LOW_ACC = 40.0
INSTANT_RECHARGE = 0.0
XFAST_RECHARGE = 1.0
FAST_RECHARGE = 2.0
MED_RECHARGE = 5.0
SLOW_RECHARGE = 10.0
XSLOW_RECHARGE = 20.0
CLOSE_RANGE = 10.0
SHORT_RANGE = 30.0
MED_RANGE = 60.0
LONG_RANGE = 100.0
FAR_RANGE = 150.0
DISTANT_RANGE = 200.0
INF_RANGE = NA
Ranges = (CLOSE_RANGE, SHORT_RANGE, MED_RANGE, LONG_RANGE, FAR_RANGE, DISTANT_RANGE)
MaxAimDistance = DISTANT_RANGE
AI_RANGE_TOLERANCE = 5.0
AI_AOE_RANGE_TOLERANCE = 10.0
AI_ENEMY_TOLERANCE = 0.0
NO_DELAY = 0.0
SHORT_DELAY = 2.5
MED_DELAY = 5.0
LONG_DELAY = 10.0
PERM_DUR = -1
INSTANT_DUR = 0.0
VERYSHORT_DUR = 8.0
SHORT_DUR = 15.0
MED_DUR = 30.0
MED2_DUR = 45.0
LONG_DUR = 60.0
NO_RECUR = 0.0
FAST_RECUR = 3.0
MED_RECUR = 5.0
SLOW_RECUR = 15.0
HIGH_QUANT = 100
MED_QUANT = 50
LOW_QUANT = 10
INF_QUANT = -1
STAFF_QUANT = -2
NO_AREA = 0
SMALL_AREA = 10.0
MED_AREA = 25.0
LARGE_AREA = 50.0
MAX_AREA_TARGETS = 10
SWIFT_NORM = 0
SWIFT_INC = 1
SWIFT_DEC = -1
SWIFT_MOD = [
    -1.0,
    -.5,
    0.0,
    0.5]
SWIFT_NORM_INDEX = 2
SWIFT_MIN_INDEX = 0
SWIFT_MAX_INDEX = 3
COMBO_SKILL_INDEX = 1
RADIAL_SKILL_INDEX = 2
PASSIVE_SKILL_INDEX = 3
TONIC_SKILL_INDEX = 4
BACKSTAB_BONUS = 1.3
BACKSTAB_ANGLE = 60
CHARGEABLE_WEAPONS = [
    InventoryType.PistolRep,
    InventoryType.GrenadeRep,
    InventoryType.WandRep]
__skills = {}
for (skillId, skillData) in list(__skillInfo.items()):
    repCat = skillData[REPUTATION_CATEGORY_INDEX]
    __skills.setdefault(repCat, []).append(skillId)


def getAllSkillIds():
    return list(__skillInfo.keys())


def getSkills(weaponRepId):
    return __skills.get(weaponRepId, [])


def getPlayerSkills(weaponRepId):
    skills = __skills.get(weaponRepId, [])
    skillSet = []
    for skillId in skills:
        if skillId >= 10000:
            skillSet.append(skillId)

    return skillSet


def getSkillName(skillId):
    return PLocalizer.InventoryTypeNames.get(skillId, 'Unknown')


def getSkillReputationCategoryId(skillId):
    cat = __skillInfo.get(skillId)
    if cat:
        return cat[REPUTATION_CATEGORY_INDEX]
    else:
        return 0


def canFreeUse(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[FREE_INDEX]

    return 0


def canPVPUse(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[PVP_INDEX]

    return 0


def isProjectileSkill(skillId, ammoSkillId):
    value = 0
    if skillId:
        value += __skillInfo[skillId][IS_PROJECTILE_INDEX]

    if ammoSkillId:
        value += __skillInfo[ammoSkillId][IS_PROJECTILE_INDEX]

    if skillId and ammoSkillId:
        if value == 2:
            return 1
        else:
            return 0
    else:
        return value


def isFirearm(weaponId):
    return weaponId in (InventoryType.PistolWeaponL1, InventoryType.PistolWeaponL2, InventoryType.PistolWeaponL3, InventoryType.PistolWeaponL4, InventoryType.PistolWeaponL5, InventoryType.PistolWeaponL6, InventoryType.MusketWeaponL1, InventoryType.MusketWeaponL2, InventoryType.MusketWeaponL3, InventoryType.BayonetWeaponL1, InventoryType.BayonetWeaponL2, InventoryType.BayonetWeaponL3)


def isBayonet(weaponId):
    return weaponId in (InventoryType.BayonetWeaponL1, InventoryType.BayonetWeaponL2, InventoryType.BayonetWeaponL3)


def isBladedWeapon(weaponId):
    return weaponId in (InventoryType.CutlassWeaponL1, InventoryType.CutlassWeaponL2, InventoryType.CutlassWeaponL3, InventoryType.CutlassWeaponL4, InventoryType.CutlassWeaponL5, InventoryType.CutlassWeaponL6, InventoryType.DaggerWeaponL1, InventoryType.DaggerWeaponL2, InventoryType.DaggerWeaponL3, InventoryType.DaggerWeaponL4, InventoryType.DaggerWeaponL5, InventoryType.DaggerWeaponL6, InventoryType.DualCutlassL1, InventoryType.FoilL1)


def isFriendlyFireWeapon(weaponId):
    return weaponId in (InventoryType.DollWeaponL1, InventoryType.DollWeaponL2, InventoryType.DollWeaponL3, InventoryType.DollWeaponL4, InventoryType.DollWeaponL5, InventoryType.DollWeaponL6)


def isVoodooWeapon(weaponId):
    return weaponId in (InventoryType.DollWeaponL1, InventoryType.DollWeaponL2, InventoryType.DollWeaponL3, InventoryType.DollWeaponL4, InventoryType.DollWeaponL5, InventoryType.DollWeaponL6, InventoryType.WandWeaponL1, InventoryType.WandWeaponL2, InventoryType.WandWeaponL3, InventoryType.WandWeaponL4, InventoryType.WandWeaponL5, InventoryType.WandWeaponL6, InventoryType.KettleWeaponL1, InventoryType.KettleWeaponL2, InventoryType.KettleWeaponL3)


def getSkillInterrupt(skillId):
    if skillId:
        value = __skillInfo[skillId][INTERRUPT_INDEX]
        return value

    return 0


def getSkillUnattune(skillId):
    if skillId:
        value = __skillInfo[skillId][UNATTUNE_INDEX]
        return value

    return 0


def isHealingSkill(skillId):
    return skillId in (InventoryType.DollHeal, InventoryType.DollCure)


def isFriendlyFire(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][FRIENDLY_FIRE_INDEX]
    if ammoSkillId:
        value |= __skillInfo[ammoSkillId][FRIENDLY_FIRE_INDEX]

    return value


def getSkillAmmoInventoryId(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[AMMO_INVENTORY_TYPE]
    return None


def getAllAmmoSkills():
    skillIds = []
    for skillId in list(__skillInfo.keys()):
        if getSkillAmmoInventoryId(skillId):
            skillIds.append(skillId)

    return skillIds


def getSkillIdForAmmoSkillId(ammoSkillId):
    skillIds = getAllAmmoSkills()
    for skillId in skillIds:
        if ammoSkillId == getSkillAmmoInventoryId(skillId):
            return skillId
    return None


def getSkillMaxQuantity(skillId):
    return __skillInfo[skillId][MAX_QUANTITY_INDEX]


def isInfiniteAmmo(skillId):
    quant = __skillInfo[skillId][MAX_QUANTITY_INDEX]
    return quant == INF_QUANT or quant == STAFF_QUANT


def getAttackMaxCharge(skillId, ammoSkillId = 0):
    value = 0
    if skillId:
        value += __skillInfo[skillId][MAX_CHARGE_INDEX]

    if ammoSkillId:
        value += __skillInfo[ammoSkillId][MAX_CHARGE_INDEX]

    return value


def getSkillLevel(skillId):
    return __skillInfo[skillId][SKILL_LEVEL_INDEX]


def getSkillTrack(skillId):
    track = __skillInfo[skillId][SKILL_TRACK_INDEX]
    if track:
        return track
    else:
        return -1


def getSkillIcon(skillId):
    if skillId not in __skillInfo:
        return 'base'

    icon = __skillInfo[skillId][SKILL_ICON_INDEX]
    if icon:
        return str(icon)
    else:
        return 'base'


def getMojoCost(skillId):
    mojoCost = __skillInfo[skillId][SELF_MOJO_INDEX]
    if mojoCost:
        return mojoCost
    else:
        return 0


def getHitEffect(skillId):
    skill = __skillInfo[skillId]
    if skill:
        return skill[HIT_VFX]

    return 0


def getCenterEffect(skillId, ammoSkillId = 0):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[CENTER_VFX]

    ammoSkill = __skillInfo.get(ammoSkillId)
    if ammoSkill:
        return ammoSkill[CENTER_VFX]


def getUsableInAir(skillId, ammoSkillId = 0):
    val = 0
    skill = __skillInfo.get(skillId)
    if skill:
        val += skill[USABLE_IN_AIR]

    ammoSkill = __skillInfo.get(ammoSkillId)
    if ammoSkill:
        val += ammoSkill[USABLE_IN_AIR]

    return val


def getNPCModifier(skillId):
    skill = __skillInfo[skillId]
    if skill:
        return skill[NPC_MODIFIER]

    return 1


def isValidSkill(skillId, weaponId, repId):
    skillInfo = __skillInfo.get(skillId)
    if skillInfo:
        if skillInfo[REPUTATION_CATEGORY_INDEX] == repId:
            return 1

    return 0


def isValidAttack(skillId, ammoSkillId, weaponId, repId):
    skillRep = getSkillReputationCategoryId(skillId)
    if not skillRep:
        return 1
    valid = skillRep == repId or skillRep == InventoryType.SailingRep
    if ammoSkillId:
        valid = valid and getSkillReputationCategoryId(ammoSkillId) == repId
    return valid


def getAttackReputation(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][REPUTATION_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][REPUTATION_INDEX]

    return value


def getAttackEffects(skillId, ammoSkillId = None):
    data = __attackEffectsSkillInfo.get((skillId, ammoSkillId))
    if data:
        return data

    skill = __skillInfo.get(skillId)
    if skill:
        selfHP = skill[SELF_HP_INDEX]
        targetHP = skill[TARGET_HP_INDEX]
        selfPower = skill[SELF_POWER_INDEX]
        targetPower = skill[TARGET_POWER_INDEX]
        selfLuck = 0
        targetEffect = skill[EFFECT_FLAG_INDEX]
        selfMojo = skill[SELF_MOJO_INDEX]
        targetMojo = skill[TARGET_MOJO_INDEX]
        selfSwiftness = skill[SELF_SWIFTNESS_INDEX]
        targetSwiftness = skill[TARGET_SWIFTNESS_INDEX]
        if ammoSkillId:
            skill = __skillInfo.get(ammoSkillId)
            if skill:
                selfHP += skill[SELF_HP_INDEX]
                targetHP += skill[TARGET_HP_INDEX]
                selfPower += skill[SELF_POWER_INDEX]
                targetPower += skill[TARGET_POWER_INDEX]
                selfLuck += 0
                targetEffect = skill[EFFECT_FLAG_INDEX]
                selfMojo += skill[SELF_MOJO_INDEX]
                targetMojo += skill[TARGET_MOJO_INDEX]
                selfSwiftness = skill[SELF_SWIFTNESS_INDEX]
                targetSwiftness += skill[TARGET_SWIFTNESS_INDEX]

        finalData = ([
            selfHP,
            selfPower,
            selfLuck,
            selfMojo,
            selfSwiftness], [
            targetHP,
            targetPower,
            targetEffect,
            targetMojo,
            targetSwiftness])
        __attackEffectsSkillInfo[(skillId, ammoSkillId)] = finalData
        return finalData
    return None


def getAttackTargetHP(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][TARGET_HP_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][TARGET_HP_INDEX]

    return value


def getAttackSelfHP(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][SELF_HP_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][SELF_HP_INDEX]

    return value


def getAttackTargetPower(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][TARGET_POWER_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][TARGET_POWER_INDEX]

    return value


def getAttackSelfPower(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][SELF_POWER_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][SELF_POWER_INDEX]

    return value


def getAttackTargetMojo(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][TARGET_MOJO_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][TARGET_MOJO_INDEX]

    return value


def getAttackSelfMojo(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][SELF_MOJO_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][SELF_MOJO_INDEX]

    if config.GetBool('mana-free-skills', 0):
        if value < 0:
            value = 0

    return value


def getAttackTargetSwiftness(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][TARGET_SWIFTNESS_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][TARGET_SWIFTNESS_INDEX]

    return value


def getAttackHullHP(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][HULL_HP_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][HULL_HP_INDEX]

    return value


def getAttackSailHP(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][SAIL_HP_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][SAIL_HP_INDEX]

    return value


def getAttackAccuracy(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][ACCURACY_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][ACCURACY_INDEX]
        value /= 2

    value = max(0, min(100, value))
    return value


def getAttackDodge(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][DODGE_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][DODGE_INDEX]

    value = max(0, min(100, value))
    return value


def getAttackRechargeTime(skillId, ammoSkillId = None):
    value = 0.0
    if skillId:
        value += __skillInfo[skillId][RECHARGE_INDEX]

    if ammoSkillId:
        value += __skillInfo[ammoSkillId][RECHARGE_INDEX]

    return value


def getAttackRange(skillId, ammoSkillId = None):
    range = 0.0
    skillValue = __skillInfo[skillId][RANGE_INDEX]
    if ammoSkillId:
        ammoValue = __skillInfo[ammoSkillId][RANGE_INDEX]
        if skillValue == INF_RANGE:
            if ammoValue == INF_RANGE:
                range = INF_RANGE
                return range
            else:
                range = ammoValue
        elif ammoValue == INF_RANGE:
            range = skillValue
        else:
            range = max(skillValue, ammoValue)
    elif skillValue == INF_RANGE:
        return range
    else:
        range = skillValue
    return range


def getAttackDelay(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][DELAY_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][DELAY_INDEX]

    return value


def getAttackDuration(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][DURATION_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][DURATION_INDEX]

    return value


def getAttackRecur(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][RECUR_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][RECUR_INDEX]

    return value


def getAttackAreaRadius(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][AREA_EFFECT_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][AREA_EFFECT_INDEX]

    value = max(0, min(DISTANT_RANGE, value))
    return value


def isAttackAreaSelfDamaging(skillId, ammoSkillId = None):
    value = 0
    if skillId:
        value |= __skillInfo[skillId][AREA_EFFECT_SELF_DAMAGE_INDEX]

    if ammoSkillId:
        value |= __skillInfo[ammoSkillId][AREA_EFFECT_SELF_DAMAGE_INDEX]

    return value


def getAttackVolley(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][VOLLEY_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][VOLLEY_INDEX]

    return float(value)


def getAttackProjectilePower(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][PROJECTILE_POWER_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][PROJECTILE_POWER_INDEX]

    return value


def getAttackReactionDelay(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][REACTION_DELAY_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][REACTION_DELAY_INDEX]

    return value


def getNumHits(skillId, ammoSkillId = None):
    value = __skillInfo[skillId][NUM_HIT_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][NUM_HIT_INDEX]

    return value


def getIsInstantSkill(skillId, ammoSkillId = None):
    skillValue = __skillInfo[skillId][INSTANT_INDEX]
    ammoValue = 1
    if ammoSkillId:
        ammoValue = __skillInfo[ammoSkillId][INSTANT_INDEX]

    if skillValue and ammoValue:
        return 1
    else:
        return 0


def getIsHostileBuff(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[HOSTILE_BUFF]

    return 0


def getNeedTarget(skillId, ammoSkillId = None):
    skill = __skillInfo.get(skillId)
    if skill:
        skillNeedsTarget = skill[NEED_TARGET_INDEX]
        if ammoSkillId:
            ammoSkill = __skillInfo.get(ammoSkillId)
            ammoNeedsTarget = ammoSkill[NEED_TARGET_INDEX]
            return skillNeedsTarget or ammoNeedsTarget
        else:
            return skillNeedsTarget
    return 0


def getNeedSight(skillId, ammoSkillId = None):
    skill = __skillInfo.get(skillId)
    if skill:
        skillNeedsSight = skill[NEED_SIGHT]
        if ammoSkillId:
            ammoSkill = __skillInfo.get(ammoSkillId)
            ammoNeedsSight = ammoSkill[NEED_SIGHT]
            return skillNeedsSight or ammoNeedsSight
        else:
            return skillNeedsSight
    return 0


def getShipAcceleration(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SHIP_ACCEL_INDEX]

    return 0


def getShipMaxSpeed(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SHIP_MAXSPEED_INDEX]

    return 0


def getShipRevAcceleration(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SHIP_REVACCEL_INDEX]

    return 0


def getShipRevMaxSpeed(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SHIP_REVMAXSPEED_INDEX]

    return 0


def getShipTurnRate(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SHIP_TURNRATE_INDEX]

    return 0


def getShipMaxTurn(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SHIP_MAXTURN_INDEX]

    return 0


def getIsShout(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SHOUT_INDEX]

    return 0


def getShipEffects(skillId, ammoSkillId = 0):
    skill = __skillInfo.get(skillId)
    if ammoSkillId:
        skill = __skillInfo.get(ammoSkillId)

    if skill:
        return [
            skill[SHIP_ACCEL_INDEX],
            skill[SHIP_MAXSPEED_INDEX],
            skill[SHIP_REVACCEL_INDEX],
            skill[SHIP_REVMAXSPEED_INDEX],
            skill[SHIP_TURNRATE_INDEX],
            skill[SHIP_MAXTURN_INDEX]]

    return [
        0,
        0,
        0,
        0,
        0,
        0]


def getIsShipSkill(skillId):
    return skillId >= InventoryType.begin_SkillSailing and skillId <= InventoryType.end_SkillSailing


def getIsCannonSkill(skillId):
    return skillId >= InventoryType.begin_WeaponSkillCannon and skillId <= InventoryType.end_WeaponSkillCannon


def getIsDollAttackSkill(skillId):
    return skillId >= InventoryType.DollPoke and skillId <= InventoryType.end_WeaponSkillDoll


def getIsStaffAttackSkill(skillId):
    return skillId >= InventoryType.StaffBlast and skillId <= InventoryType.StaffDesolation


def getIsStaffChargeSkill(skillId):
    return skillId >= EnemySkills.STAFF_FIZZLE and skillId <= EnemySkills.STAFF_DESOLATION_CHARGE


def getIsGrappleSkill(skillId, ammoSkillId):
    if ammoSkillId == InventoryType.CannonGrappleHook:
        return 1
    else:
        return 0


def getAnimTime(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[ANIM_TIME_INDEX]

    return 0

EFFECT_FLAME = 2

def getSkillEffectFlag(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[EFFECT_FLAG_INDEX]

    return 0


def getAttackClass(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[ATTACK_CLASS_INDEX]

    return 0


def getAttackAreaShape(skillId, ammoSkillId):
    if ammoSkillId:
        ammoShape = __skillInfo[ammoSkillId][AREA_SHAPE_INDEX]
        if ammoShape:
            return ammoShape


    skillShape = __skillInfo[skillId][AREA_SHAPE_INDEX]
    if skillShape:
        return skillShape

    return AREA_OFF

PLAYABLE_INDEX = 0
HIT_SFX_INDEX = 1
MISS_SFX_INDEX = 2
OUCH_SFX_INDEX = 3
ANIM_TYPE = 0
FUNC_TYPE = 1
INTERVAL_TYPE = 2
NONE_TYPE = 3
__skillAnim = {
    InventoryType.MeleePunch: ('getBoxingPunch', Melee.getHitSfx, Melee.getMissSfx),
    InventoryType.MeleeJab: ('getBoxingPunch', Melee.getHitSfx, Melee.getMissSfx),
    InventoryType.MeleeKick: ('getKick', Melee.getHitSfx, Melee.getMissSfx),
    InventoryType.MeleeRoundhouse: ('getKick', Melee.getHitSfx, Melee.getMissSfx),
    InventoryType.MeleeHeadbutt: ('getKrazyPunch', Melee.getHitSfx, Melee.getMissSfx),
    InventoryType.MeleeHaymaker: ('getBoxingPunch', Melee.getHitSfx, Melee.getMissSfx),
    InventoryType.MeleeThrowDirt: ('getKrazyPunch', Melee.getHitSfx, Melee.getMissSfx),
    InventoryType.CutlassHack: ('getHack', Sword.getHitSfx, Sword.getMissSfx),
    InventoryType.CutlassSlash: ('getSlash', Sword.getHitSfx, Sword.getMissSfx),
    InventoryType.CutlassStab: ('getThrust', Sword.getHitSfx, Sword.getMissSfx),
    InventoryType.CutlassFlourish: ('getFlourish', Sword.getHitSfx, Sword.getMissSfx),
    InventoryType.CutlassCleave: ('getCleave', Sword.getHitSfx, Sword.getMissSfx),
    InventoryType.CutlassTaunt: ('getTaunt', Sword.getHitSfx, Sword.getMissSfx),
    InventoryType.CutlassBrawl: ('getBrawl', Sword.getHitSfx, Sword.getMissSfx),
    InventoryType.CutlassSweep: ('getSweep', Sword.getHitSfx, Sword.getMissSfx),
    InventoryType.CutlassBladestorm: ('getBladestorm', Sword.getHitSfx, Sword.getMissSfx),
    InventoryType.PistolShoot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx),
    InventoryType.PistolTakeAim: ('getPistolTakeAimAnim', Pistol.getHitSfx, Pistol.getMissSfx),
    EnemySkills.PISTOL_CHARGE: ('getPistolChargingAnim', Pistol.getAimSfx, Pistol.getAimSfx),
    EnemySkills.PISTOL_RELOAD: ('getPistolReloadAnim', None, None),
    InventoryType.PistolLeadShot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx),
    InventoryType.PistolBaneShot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx),
    InventoryType.PistolSilverShot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx),
    InventoryType.PistolHexEaterShot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx),
    InventoryType.PistolSteelShot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx),
    InventoryType.PistolVenomShot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx),
    InventoryType.MusketShoot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx),
    InventoryType.MusketTakeAim: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx),
    InventoryType.MusketDeadeye: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx),
    InventoryType.BayonetShoot: ('getBayonetFireAnim', Bayonet.getShootSfx, Bayonet.getShootSfx),
    InventoryType.BayonetStab: ('getBayonetStab', Bayonet.getHitSfx, Bayonet.getMissSfx),
    InventoryType.BayonetRush: ('getBayonetRush', Bayonet.getHitSfx, Bayonet.getMissSfx),
    InventoryType.BayonetBash: ('getBayonetBash', Bayonet.getHitSfx, Bayonet.getMissSfx),
    InventoryType.DaggerCut: ('getCut', Dagger.getHitSfx, Dagger.getMissSfx),
    InventoryType.DaggerSwipe: ('getSwipe', Dagger.getHitSfx, Dagger.getMissSfx),
    InventoryType.DaggerGouge: ('getGouge', Dagger.getHitSfx, Dagger.getMissSfx),
    InventoryType.DaggerEviscerate: ('getEviscerate', Dagger.getHitSfx, Dagger.getMissSfx),
    InventoryType.DaggerAsp: ('getDaggerAspInterval', Dagger.getHitSfx, Dagger.getMissSfx),
    InventoryType.DaggerAdder: ('getDaggerAdderInterval', Dagger.getHitSfx, Dagger.getMissSfx),
    InventoryType.DaggerThrowDirt: ('getDaggerThrowDirtInterval', Dagger.getHitSfx, Dagger.getMissSfx),
    InventoryType.DaggerSidewinder: ('getDaggerSidewinderInterval', Dagger.getHitSfx, Dagger.getMissSfx),
    InventoryType.DaggerViperNest: ('getDaggerViperNestInterval', Dagger.getHitSfx, Dagger.getMissSfx),
    EnemySkills.DAGGER_THROW_KNIFE: ('getDaggerAspInterval', Dagger.getHitSfx, Dagger.getMissSfx),
    EnemySkills.DAGGER_THROW_VENOMBLADE: ('getDaggerAdderInterval', Dagger.getHitSfx, Dagger.getMissSfx),
    EnemySkills.DAGGER_THROW_BARBED: ('getDaggerSidewinderInterval', Dagger.getHitSfx, Dagger.getMissSfx),
    EnemySkills.DAGGER_THROW_INTERRUPT: ('getDaggerAspInterval', Dagger.getHitSfx, Dagger.getMissSfx),
    InventoryType.GrenadeThrow: ('getGrenadeThrow', Grenade.getHitSfx, Grenade.getMissSfx),
    InventoryType.GrenadeLongVolley: ('getGrenadeLongVolley', Grenade.getHitSfx, Grenade.getMissSfx),
    EnemySkills.GRENADE_CHARGE: ('getGrenadeChargingAnim', Grenade.getAimSfx, Grenade.getAimSfx),
    EnemySkills.GRENADE_RELOAD: ('getGrenadeReloadAnim', Grenade.getReloadSfx, Grenade.getReloadSfx),
    InventoryType.GrenadeExplosion: ('getGrenadeThrow', Grenade.getHitSfx, Grenade.getMissSfx),
    InventoryType.GrenadeShockBomb: ('getGrenadeThrow', Grenade.getHitSfx, Grenade.getMissSfx),
    InventoryType.GrenadeFireBomb: ('getGrenadeThrow', Grenade.getHitSfx, Grenade.getMissSfx),
    InventoryType.GrenadeSmokeCloud: ('getGrenadeThrow', Grenade.getHitSfx, Grenade.getMissSfx),
    InventoryType.GrenadeSiege: ('getGrenadeThrow', Grenade.getHitSfx, Grenade.getMissSfx),
    InventoryType.DollAttune: ('getAttune', Doll.getAttuneSfx, Doll.getMissSfx),
    EnemySkills.DOLL_UNATTUNE: ('getUnattune', Doll.getUnattuneSfx, Doll.getMissSfx),
    EnemySkills.DOLL_POKE2: ('getPoke', Doll.getPokeSfx, Doll.getMissSfx),
    InventoryType.DollPoke: ('getPoke', Doll.getPokeSfx, Doll.getMissSfx),
    InventoryType.DollSwarm: ('getSwarm', Doll.getSwarmSfx, Doll.getMissSfx),
    InventoryType.DollHeal: ('getHeal', Doll.getHealSfx, Doll.getMissSfx),
    InventoryType.DollBurn: ('getBurn', Doll.getScorchSfx, Doll.getMissSfx),
    InventoryType.DollShackles: ('getShackles', Doll.getShacklesSfx, Doll.getMissSfx),
    InventoryType.DollCure: ('getCure', Doll.getCureSfx, Doll.getMissSfx),
    InventoryType.DollCurse: ('getCurse', Doll.getCurseSfx, Doll.getMissSfx),
    InventoryType.DollLifeDrain: ('getLifeDrain', Doll.getLifedrainSfx, Doll.getMissSfx),
    EnemySkills.STAFF_WITHER_CHARGE: ('getChargeWitherAnim', Wand.getWitherChargeSfx, Wand.getWitherHoldSfx),
    EnemySkills.STAFF_SOULFLAY_CHARGE: ('getChargeSoulflayAnim', Wand.getSoulflayChargeSfx, Wand.getSoulflayHoldSfx),
    EnemySkills.STAFF_PESTILENCE_CHARGE: ('getChargePestilenceAnim', Wand.getPestilenceChargeSfx, Wand.getPestilenceHoldSfx),
    EnemySkills.STAFF_HELLFIRE_CHARGE: ('getChargeHellfireAnim', Wand.getHellfireChargeSfx, Wand.getHellfireHoldSfx),
    EnemySkills.STAFF_BANISH_CHARGE: ('getChargeBanishAnim', Wand.getBanishChargeSfx, Wand.getBanishHoldSfx),
    EnemySkills.STAFF_DESOLATION_CHARGE: ('getChargeDesolationAnim', Wand.getDesolationChargeSfx, Wand.getDesolationHoldSfx),
    EnemySkills.STAFF_FIZZLE: ('getFizzleAnim', Wand.getChargeSfx, Wand.getChargeLoopSfx),
    InventoryType.StaffBlast: ('getCastFireAnim', Wand.getBlastFireSfx, Wand.getBlastFireSfx, Wand.getBlastHitSfx),
    InventoryType.StaffSoulFlay: ('getCastSoulFlayAnim', Wand.getSoulflayFireSfx, Wand.getSoulflayFireSfx, Wand.getSoulflayHitSfx),
    InventoryType.StaffPestilence: ('getCastPestilenceAnim', Wand.getPestilenceFireSfx, Wand.getPestilenceFireSfx, Wand.getPestilenceHitSfx),
    InventoryType.StaffWither: ('getCastWitherAnim', Wand.getWitherFireSfx, Wand.getWitherFireSfx, Wand.getWitherHitSfx),
    InventoryType.StaffHellfire: ('getCastHellfireAnim', Wand.getHellfireFireSfx, Wand.getHellfireFireSfx, Wand.getHellfireHitSfx),
    InventoryType.StaffBanish: ('getCastBanishAnim', Wand.getBanishFireSfx, Wand.getBanishFireSfx, Wand.getBanishHitSfx),
    InventoryType.StaffDesolation: ('getCastDesolationAnim', Wand.getDesolationFireSfx, Wand.getDesolationFireSfx, Wand.getDesolationHitSfx),
    InventoryType.UseItem: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx),
    InventoryType.Potion1: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx),
    InventoryType.Potion2: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx),
    InventoryType.Potion3: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx),
    InventoryType.Potion4: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx),
    InventoryType.Potion5: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx),
    InventoryType.ShipRepairKit: ('getShipRepair', Consumable.getShipRepairSfx, Consumable.getMissSfx),
    InventoryType.PorkChunk: ('getDrink', Consumable.getEatSfx, Consumable.getMissSfx),
    InventoryType.SailBroadsideLeft: ('getBroadsideLeft', None, None),
    InventoryType.SailBroadsideRight: ('getBroadsideRight', None, None),
    InventoryType.SailFullSail: ('getFullSail', None, None),
    InventoryType.SailComeAbout: ('getComeAbout', None, None),
    InventoryType.SailOpenFire: ('getOpenFire', None, None),
    InventoryType.SailRammingSpeed: ('getRammingSpeed', None, None),
    InventoryType.SailTakeCover: ('getTakeCover', None, None),
    InventoryType.SailPowerRecharge: ('getPowerRecharge', None, None),
    EnemySkills.CLAW_RAKE: ('getCrabAttackRight', MonsterMelee.getCrabAttackLeftSfx, MonsterMelee.getCrabAttackLeftSfx, 0),
    EnemySkills.CLAW_STRIKE: ('getCrabAttackLeft', MonsterMelee.getCrabAttackLeftSfx, MonsterMelee.getCrabAttackLeftSfx, 0),
    EnemySkills.DUAL_CLAW: ('getCrabAttackBoth', MonsterMelee.getCrabAttackBothSfx, MonsterMelee.getCrabAttackBothSfx, 0),
    EnemySkills.STUMP_KICK: ('getStumpKick', MonsterMelee.getMossmanAttackKickSfx, MonsterMelee.getMossmanAttackKickSfx, 0),
    EnemySkills.STUMP_KICK_RIGHT: ('getStumpKickRight', MonsterMelee.getMossmanAttackKickSfx, MonsterMelee.getMossmanAttackKickSfx, 0),
    EnemySkills.STUMP_SLAP_LEFT: ('getStumpSlapLeft', MonsterMelee.getMossmanAttackSlapSfx, MonsterMelee.getMossmanAttackSlapSfx, 0),
    EnemySkills.STUMP_SLAP_RIGHT: ('getStumpSlapRight', MonsterMelee.getMossmanAttackSlapSfx, MonsterMelee.getMossmanAttackSlapSfx, 0),
    EnemySkills.STUMP_SWAT_LEFT: ('getStumpSwatLeft', MonsterMelee.getMossmanAttackSwatSfx, MonsterMelee.getMossmanAttackSwatSfx, 0),
    EnemySkills.STUMP_SWAT_RIGHT: ('getStumpSwatRight', MonsterMelee.getMossmanAttackSwatSfx, MonsterMelee.getMossmanAttackSwatSfx, 0),
    EnemySkills.STUMP_STOMP: ('getStumpStomp', MonsterMelee.getMossmanAttackJumpSfx, MonsterMelee.getMossmanAttackJumpSfx, 0),
    EnemySkills.FLYTRAP_ATTACK_A: ('getFlyTrapAttackA', MonsterMelee.getFlytrapAttackASfx, MonsterMelee.getFlytrapAttackASfx, 0),
    EnemySkills.FLYTRAP_ATTACK_JAB: ('getFlyTrapAttackJab', MonsterMelee.getFlytrapAttackJabSfx, MonsterMelee.getFlytrapAttackJabSfx, 0),
    EnemySkills.FLYTRAP_LEFT_FAKE: ('getFlyTrapLeftFake', MonsterMelee.getFlytrapAttackFakeSfx, MonsterMelee.getFlytrapAttackFakeSfx, 0),
    EnemySkills.FLYTRAP_RIGHT_FAKE: ('getFlyTrapRightFake', MonsterMelee.getFlytrapAttackFakeSfx, MonsterMelee.getFlytrapAttackFakeSfx, 0),
    EnemySkills.FLYTRAP_SPIT: ('getFlyTrapSpit', MonsterMelee.getFlytrapAttackSpitSfx, MonsterMelee.getFlytrapAttackSpitSfx, 0),
    EnemySkills.POISON_VOMIT: ('getKrakenVomit', MonsterMelee.getEnsnareSfx, MonsterMelee.getMissSfx, 0),
    EnemySkills.GROUND_SLAP: ('getTentacleSlap', MonsterMelee.getSmashSfx, MonsterMelee.getMissSfx, 0),
    EnemySkills.ENSNARE: ('getTentacleEnsnare', MonsterMelee.getEnsnareSfx, MonsterMelee.getMissSfx, 0),
    EnemySkills.CONSTRICT: ('getTentacleConstrict', MonsterMelee.getHitSfx, MonsterMelee.getMissSfx, 0),
    EnemySkills.PILEDRIVER: ('getTentaclePiledriver', MonsterMelee.getSmashSfx, MonsterMelee.getMissSfx, 0),
    EnemySkills.POUND: ('getTentaclePound', MonsterMelee.getHitSfx, MonsterMelee.getMissSfx, 0),
    EnemySkills.SCORPION_ATTACK_LEFT: ('getScorpionAttackLeft', MonsterMelee.getScorpionAttackLeftSfx, MonsterMelee.getScorpionAttackLeftSfx, 0),
    EnemySkills.SCORPION_ATTACK_RIGHT: ('getScorpionAttackRight', MonsterMelee.getScorpionAttackLeftSfx, MonsterMelee.getScorpionAttackLeftSfx, 0),
    EnemySkills.SCORPION_ATTACK_BOTH: ('getScorpionAttackBoth', MonsterMelee.getScorpionAttackBothSfx, MonsterMelee.getScorpionAttackBothSfx, 0),
    EnemySkills.SCORPION_ATTACK_TAIL_STING: ('getScorpionAttackTailSting', MonsterMelee.getScorpionAttackTailStingSfx, MonsterMelee.getScorpionAttackTailStingSfx, 0),
    EnemySkills.SCORPION_PICK_UP_HUMAN: ('getScorpionPickUpHuman', MonsterMelee.getScorpionPickUpHumanSfx, MonsterMelee.getScorpionPickUpHumanSfx, 0),
    EnemySkills.SCORPION_REAR_UP: ('getScorpionRearUp', MonsterMelee.getScorpionRearUpSfx, MonsterMelee.getScorpionRearUpSfx, 0),
    EnemySkills.ALLIGATOR_ATTACK_LEFT: ('getAlligatorAttackLeft', MonsterMelee.getAlligatorAttackLeftSfx, MonsterMelee.getAlligatorAttackLeftSfx, 0),
    EnemySkills.ALLIGATOR_ATTACK_RIGHT: ('getAlligatorAttackRight', MonsterMelee.getAlligatorAttackLeftSfx, MonsterMelee.getAlligatorAttackLeftSfx, 0),
    EnemySkills.ALLIGATOR_ATTACK_STRAIGHT: ('getAlligatorAttackStraight', MonsterMelee.getAlligatorAttackStraightSfx, MonsterMelee.getAlligatorAttackStraightSfx, 0),
    EnemySkills.ALLIGATOR_CRUSH: ('getAlligatorAttackStraight', MonsterMelee.getAlligatorAttackStraightSfx, MonsterMelee.getAlligatorAttackStraightSfx, 0),
    EnemySkills.ALLIGATOR_MAIM: ('getAlligatorAttackRight', MonsterMelee.getAlligatorAttackLeftSfx, MonsterMelee.getAlligatorAttackLeftSfx, 0),
    EnemySkills.BAT_ATTACK_LEFT: ('getBatAttackLeft', MonsterMelee.getBatAttackSfx, MonsterMelee.getBatAttackSfx, 0),
    EnemySkills.BAT_ATTACK_RIGHT: ('getBatAttackRight', MonsterMelee.getBatAttackSfx, MonsterMelee.getBatAttackSfx, 0),
    EnemySkills.BAT_SHRIEK: ('getBatShriek', MonsterMelee.getBatAttackSfx, MonsterMelee.getBatAttackSfx, 0),
    EnemySkills.BAT_FLURRY: ('getBatFlurry', MonsterMelee.getBatAttackSfx, MonsterMelee.getBatAttackSfx, 0),
    EnemySkills.WASP_ATTACK: ('getWaspAttack', MonsterMelee.getWaspStingSfx, MonsterMelee.getWaspStingSfx, 0),
    EnemySkills.WASP_ATTACK_LEAP: ('getWaspAttackLeap', MonsterMelee.getWaspLeapStingSfx, MonsterMelee.getWaspLeapStingSfx, 0),
    EnemySkills.WASP_POISON_STING: ('getWaspAttackSting', MonsterMelee.getWaspStingSfx, MonsterMelee.getWaspStingSfx, 0),
    EnemySkills.WASP_PAIN_BITE: ('getWaspAttack', MonsterMelee.getWaspStingSfx, MonsterMelee.getWaspStingSfx, 0),
    EnemySkills.SERPENT_VENOM: ('getWaspAttack', MonsterMelee.getWaspStingSfx, MonsterMelee.getWaspStingSfx, 0),
    EnemySkills.CUTLASS_CHOP: ('getChop', Sword.getHitSfx, Sword.getMissSfx, 0),
    EnemySkills.CUTLASS_DOUBLESLASH: ('getDoubleSlash', Sword.getHitSfx, Sword.getMissSfx, 0),
    EnemySkills.CUTLASS_LUNGE: ('getLunge', Sword.getHitSfx, Sword.getMissSfx, 0),
    EnemySkills.CUTLASS_STAB: ('getStab', Sword.getHitSfx, Sword.getMissSfx, 0),
    EnemySkills.CUTLASS_ROLLTHRUST: ('getRollThrust', Sword.getHitSfx, Sword.getMissSfx, 0),
    EnemySkills.CUTLASS_COMBOA: ('getComboA', Sword.getHitSfx, Sword.getMissSfx, 0),
    EnemySkills.CUTLASS_WILDSLASH: ('getWildSlash', Sword.getHitSfx, Sword.getMissSfx, 0),
    EnemySkills.CUTLASS_FLURRY: ('getFlurry', Sword.getHitSfx, Sword.getMissSfx, 0),
    EnemySkills.CUTLASS_RIPOSTE: ('getRiposte', Sword.getHitSfx, Sword.getMissSfx, 0),
    EnemySkills.FOIL_FLECHE: ('getFoilFleche', Foil.getHitSfx, Foil.getMissSfx, 0),
    EnemySkills.FOIL_REPRISE: ('getFoilReprise', Foil.getHitSfx, Foil.getMissSfx, 0),
    EnemySkills.FOIL_SWIPE: ('getFoilSwipe', Foil.getHitSfx, Foil.getMissSfx, 0),
    EnemySkills.FOIL_IMPALE: ('getFoilImpale', Foil.getHitSfx, Foil.getMissSfx, 0),
    EnemySkills.FOIL_REMISE: ('getFoilRemise', Foil.getHitSfx, Foil.getMissSfx, 0),
    EnemySkills.FOIL_BALESTRAKICK: ('getFoilBalestraKick', Foil.getHitSfx, Foil.getMissSfx, 0),
    EnemySkills.FOIL_CADENCE: ('getFoilCadence', Foil.getHitSfx, Foil.getMissSfx, 0),
    EnemySkills.DUALCUTLASS_COMBINATION: ('getDualCutlassCombination', DualCutlass.getHitSfx, DualCutlass.getMissSfx, 0),
    EnemySkills.DUALCUTLASS_SPIN: ('getDualCutlassSpin', DualCutlass.getHitSfx, DualCutlass.getMissSfx, 0),
    EnemySkills.DUALCUTLASS_BARRAGE: ('getDualCutlassBarrage', DualCutlass.getHitSfx, DualCutlass.getMissSfx, 0),
    EnemySkills.DUALCUTLASS_XSLASH: ('getDualCutlassXSlash', DualCutlass.getHitSfx, DualCutlass.getMissSfx, 0),
    EnemySkills.DUALCUTLASS_GORE: ('getDualCutlassGore', DualCutlass.getHitSfx, DualCutlass.getMissSfx, 0)}

def getSkillAnimInfo(skillId):
    skillInfo = __skillAnim.get(skillId)
    return skillInfo

RESULT_MISS = 0
RESULT_HIT = 1
RESULT_DELAY = 2
RESULT_OUT_OF_RANGE = 3
RESULT_NOT_AVAILABLE = 4
RESULT_NOT_RECHARGED = 5
RESULT_AGAINST_PIRATE_CODE = 6
RESULT_PARRY = 7
RESULT_DODGE = 8
RESULT_RESIST = 9

def getSkillResultName(result):
    return PLocalizer.SkillResultNames[result]

__multiHitAttacks = {
  InventoryType.DaggerSwipe: [0.1, 0.4],
  InventoryType.DaggerEviscerate: [0.15, 0.65, 1.15],
  InventoryType.DaggerViperNest: [1.0, 1.4, 1.7],
  InventoryType.CutlassBladestorm: [0.4, 0.7, 1.13, 1.41, 2.6],
  InventoryType.CutlassFlourish: [0.56, 0.93, 1.3],
  InventoryType.BayonetRush: [0.15, 0.65, 1.15, 1.6],
  EnemySkills.CUTLASS_DOUBLESLASH: [0.3, 0.8],
  EnemySkills.CUTLASS_FLURRY: [0.15, 0.65, 1.15],
  EnemySkills.CUTLASS_COMBOA: [0.56, 0.93, 1.3],
  EnemySkills.DUAL_CLAW: [0.3, 0.5],
  EnemySkills.BAT_FLURRY: [0.4, 0.7, 1.13, 1.41],
  EnemySkills.FOIL_REPRISE: [0.3, 0.8],
  EnemySkills.FOIL_REMISE: [0.5, 0.9],
  EnemySkills.FOIL_CADENCE: [0.5, 0.9, 1.3, 1.8],
  EnemySkills.DUALCUTLASS_COMBINATION: [0.36, 0.8, 1.2, 1.3, 1.68, 2.1],
  EnemySkills.DUALCUTLASS_BARRAGE: [0.62, 0.9, 1.25, 1.5, 1.8],
  EnemySkills.DUALCUTLASS_SPIN: [0.29, 0.5, 0.75, 0.95],
  EnemySkills.DUALCUTLASS_XSLASH: [0.7, 1.7],
  EnemySkills.DUALCUTLASS_GORE: [0.4, 1.6]
}

def getMultiHitAttacks(skillId):
  return __multiHitAttacks.get(skillId)

__projectileAttacks = {
  InventoryType.DaggerAsp: (80, 0.708, (150, 15)),
  InventoryType.DaggerAdder: (80, 0.708, (150, 15)),
  InventoryType.DaggerSidewinder: (80, 0.292, (150, 15)),
  InventoryType.StaffBlast: (80, 0.0, (70, 5)),
  InventoryType.StaffHellfire: (100, 0.0, (100, 5)),
  EnemySkills.FLYTRAP_SPIT: (100, 0.958, (70, 5)),
  EnemySkills.DAGGER_THROW_KNIFE: (80, 0.708, (150, 15)),
  EnemySkills.DAGGER_THROW_VENOMBLADE: (80, 0.708, (150, 15)),
  EnemySkills.DAGGER_THROW_BARBED: (80, 0.292, (150, 15)),
  EnemySkills.DAGGER_THROW_INTERRUPT: (80, 0.708, (150, 15))
}

def getProjectileSpeed(skillId):
    entry = __projectileAttacks.get(skillId)
    if entry:
        return entry[0]
    return None

def getProjectileAnimT(skillId):
    entry = __projectileAttacks.get(skillId)
    if entry:
        return entry[1]
    return None


def getProjectileDefaultRange(skillId):
    entry = __projectileAttacks.get(skillId)
    if entry:
        return entry[2]
    return None


def getLevelDamageModifier(level):
    return level * 0.05 + 1.0


def getComparativeLevelDamageModifier(attacker, defender):
    attackerLevel = attacker.getLevel()
    defenderLevel = defender.getLevel()
    THRESHOLD = 2.0
    if attackerLevel > defenderLevel:
        if not attacker.isNpc:
            mod = max(0, attackerLevel - defenderLevel - THRESHOLD) * 0.05 + 1.0
        else:
            mod = max(0, attackerLevel - defenderLevel - THRESHOLD) * 0.125 + 1.0
    elif not attacker.isNpc:
        mod = min(0, (attackerLevel - defenderLevel) + THRESHOLD) * 0.1 + 1.0
    else:
        mod = min(0, (attackerLevel - defenderLevel) + THRESHOLD) * 0.03 + 1.0
    if not attacker.isNpc:
        mod = min(1.5, mod)
    else:
        mod = max(0.5, mod)
    return max(0.1, mod)


def getComparativeLevelAccuracyModifier(attacker, defender):
    attackerLevel = attacker.getLevel()
    defenderLevel = defender.getLevel()
    THRESHOLD = 3.0
    mod = 0.0
    if not attacker.isNpc:
        if attackerLevel > defenderLevel:
            mod = min(100.0, max(0, attackerLevel - defenderLevel - THRESHOLD) * 6.0)
        else:
            mod = max(-50.0, min(0, (attackerLevel - defenderLevel) + THRESHOLD) * 6.0)

    return mod


def getComparativeShipLevelDamageModifier(attacker, defender):
    attackerLevel = attacker.getLevel()
    defenderLevel = defender.getLevel()
    THRESHOLD = 5.0
    if attackerLevel > defenderLevel:
        mod = 1.0
        if attacker.isNpc:
            mod = max(0, attackerLevel - defenderLevel - THRESHOLD) * 0.06 + 1.0

    elif attacker.isNpc:
        mod = min(0, (attackerLevel - defenderLevel) + THRESHOLD) * 0.06 + 1.0
    else:
        mod = min(0, (attackerLevel - defenderLevel) + THRESHOLD) * 0.02 + 1.0
    return max(0, mod)

MP_DAMAGE_DELAY = 0.25
COMBO_DAMAGE_DELAY = 0.5
__comboBonuses = {
    2: -1,
    3: -2,
    5: -4,
    7: -5,
    10: -7,
    15: -10,
    20: -12,
    25: -15,
    30: -17,
    50: -20,
    75: -25,
    100: -30}

def getComboBonus(val):
    return __comboBonuses.get(val, 0)


def skillTableSanityCheck():
    for (skillId, skillInfo) in list(__skillInfo.items()):
        maxQuant = getSkillMaxQuantity(skillId)
        ammoInvId = getSkillAmmoInventoryId(skillId)
        if maxQuant != INF_QUANT and maxQuant != STAFF_QUANT:
            pass
        else:
            ammoInvId = getSkillAmmoInventoryId(skillId)

    return 1

__effectTable = {
    C_FLAMING: ((-30, 0, 0, 0, 0), 3),
    C_ON_FIRE: ((-24, 0, 0, 0, 0), 3),
    C_WOUND: ((-40, 0, 0, 0, 0), 3),
    C_ACID: ((-28, 0, 0, 0, 0), 3),
    C_POISON: ((-20, 0, 0, 0, 0), 3),
    C_REGEN: ((20, 0, 0, 0, 0), 3),
    C_STUN: ((0, 0, 0, 0, -1), 1),
    C_UNSTUN: ((0, 0, 0, 0, 0), 1),
    C_SLOW: ((0, 0, 0, 0, 0), 1),
    C_PAIN: ((0, 0, 0, 0, 0), 1),
    C_HOLD: ((0, 0, 0, 0, -1), 1),
    C_BLIND: ((0, 0, 0, 0, 0), 1),
    C_TAUNT: ((0, 0, 0, 0, 0), 1),
    C_MINE: ((0, 0, 0, 0, 0), 1),
    C_CURSE: ((0, 0, 0, 0, 0), 1),
    C_HASTEN: ((0, 0, 0, 0, 0), 1),
    C_WEAKEN: ((0, 0, 0, 0, 0), 1),
    C_FULLSAIL: ((0, 0, 0, 0, 0), 1),
    C_COMEABOUT: ((0, 0, 0, 0, 0), 1),
    C_OPENFIRE: ((0, 0, 0, 0, 0), 1),
    C_RAM: ((0, 0, 0, 0, 0), 1),
    C_TAKECOVER: ((0, 0, 0, 0, 0), 1),
    C_RECHARGE: ((0, 0, 0, 0, 0), 1),
    C_ATTUNE: ((0, 0, 0, 0, 0), 10),
    C_DIRT: ((0, 0, 0, 0, 0), 1),
    C_SPAWN: ((0, 0, 0, 0, 0), 1),
    C_SOULTAP: ((0, 0, 0, 0, 0), 1),
    C_LIFEDRAIN: ((0, 0, 0, 0, 0), 1),
    C_MANADRAIN: ((0, 0, 0, 0, 0), 1),
    C_BUFF_BREAK: ((0, 0, 0, 0, 0), 1),
    C_UNDEAD_KILLER: ((0, 0, 0, 0, 0), 1),
    C_MONSTER_KILLER: ((0, 0, 0, 0, 0), 1),
    C_SHIPHEAL: ((0, 0, 0, 0, 0), 1),
    C_VOODOO_STUN: ((0, 0, 0, 0, 0), 1),
    C_VOODOO_STUN_LOCK: ((0, 0, 0, 0, 0), 1),
    C_VOODOO_HEX_STUN: ((0, 0, 0, 0, 0), 1),
    C_INTERRUPTED: ((0, 0, 0, 0, 0), 1)}

def getEffects(effectId):
    return __effectTable.get(effectId)[0]


def getBuffStackNumber(buffId):
    return __effectTable.get(buffId)[1]

CURSED_DAM_AMP = 0.3
WEAKEN_PENALTY = 0.3
BLIND_PERCENT = 0.75
TAUNT_PERCENT = 0.9
RESIST_DAMAGE_PENALTY = 0.1
OPEN_FIRE_BONUS = 1.5
TAKE_COVER_BONUS = 0.25
TREASURE_SENSE_BONUS = 10
CANNON_SHOOT_RATE_REDUCTION = 0.25
POWER_RECHARGE_RATE_REDUCTION = 0.75
LEVELUP_DAMAGE_MULTIPLIER = 0.25
LOW_HEALTH_THRESHOLD = 0.25
__buffPriority = {
    C_RAM: (1, 3),
    C_FULLSAIL: (1, 1),
    C_COMEABOUT: (1, 1),
    C_TAKECOVER: (2, 1),
    C_OPENFIRE: (2, 1),
    C_UNSTUN: (3, 2),
    C_STUN: (3, 1)}

def getBuffCategory(buffId):
    val = __buffPriority.get(buffId)
    if val:
        return val[0]

    return 0


def getBuffPriority(buffId):
    val = __buffPriority.get(buffId)
    if val:
        return val[1]

    return 0

__weaponVolley = {
    InventoryType.PistolWeaponL1: 1,
    InventoryType.PistolWeaponL2: 2,
    InventoryType.PistolWeaponL3: 3,
    InventoryType.PistolWeaponL4: 3,
    InventoryType.PistolWeaponL5: 3,
    InventoryType.PistolWeaponL6: 4,
    InventoryType.MusketWeaponL1: 1,
    InventoryType.MusketWeaponL2: 2,
    InventoryType.MusketWeaponL3: 3,
    InventoryType.BayonetWeaponL1: 1,
    InventoryType.BayonetWeaponL2: 2,
    InventoryType.BayonetWeaponL3: 3,
    InventoryType.GrenadeWeaponL1: 1,
    InventoryType.GrenadeWeaponL2: 1,
    InventoryType.GrenadeWeaponL3: 1}

def getWeaponVolley(weaponId):
    val = __weaponVolley.get(weaponId)
    if val:
        return val

    return 0

__staffChargeSkills = {
    InventoryType.StaffWither: EnemySkills.STAFF_WITHER_CHARGE,
    InventoryType.StaffSoulFlay: EnemySkills.STAFF_SOULFLAY_CHARGE,
    InventoryType.StaffPestilence: EnemySkills.STAFF_PESTILENCE_CHARGE,
    InventoryType.StaffHellfire: EnemySkills.STAFF_HELLFIRE_CHARGE,
    InventoryType.StaffBanish: EnemySkills.STAFF_BANISH_CHARGE,
    InventoryType.StaffDesolation: EnemySkills.STAFF_DESOLATION_CHARGE}

def getChargeSkill(skillId):
    return __staffChargeSkills.get(skillId)


def getAIProjectileAirTime(distance):
    return max(min(distance * 0.04, 2.6), 1.2)

BackstabSkills = (InventoryType.DaggerCut, InventoryType.DaggerSwipe, InventoryType.DaggerGouge, InventoryType.DaggerEviscerate)
StartingSkills = [
    InventoryType.CutlassHack,
    InventoryType.CutlassSlash,
    InventoryType.SailBroadsideLeft,
    InventoryType.SailBroadsideRight,
    InventoryType.DaggerCut,
    InventoryType.DaggerSwipe,
    InventoryType.StaffBlast,
    InventoryType.StaffSoulFlay,
    InventoryType.GrenadeThrow,
    InventoryType.GrenadeExplosion,
    InventoryType.PistolShoot,
    InventoryType.PistolLeadShot,
    InventoryType.DollAttune,
    InventoryType.DollPoke,
    InventoryType.CannonShoot,
    InventoryType.CannonRoundShot]
DontResetSkills = [
    InventoryType.SailPowerRecharge,
    InventoryType.CannonGrappleHook]
