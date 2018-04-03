# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.CannonGlobals
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType

CANNON_NOT_FIRED = -1
CANNON_TGT_OUTOFRANGE = 0
CANNON_FIRED = 1
CANNON_RELOADING = 2
AI_FIRE_TIME = 3.0
CLIENT_BROADSIDE_FIRE_VELOCITY = 500.0
AI_BROADSIDE_FIRE_VELOCITY = 200.0
AI_FIRE_VELOCITY = 100.0
ADEX_ASSET = 0
ADEX_REP = 1
ADEX_RMOD = 2
ADEX_EXPLOS = 3
ADEX_TYPE = 4
BROADSIDE_POWERMOD = 0.7
CANNON_AMMO = {InventoryType.CannonRoundShot: ['roundshot', 1, 'R', 0, 'round'], InventoryType.CannonGrappleHook: ['grapple_hook', 1, 'R', 0, 'round'], InventoryType.CannonChainShot: ['chain_shot', 1, 'R', 2, 'explosive'], InventoryType.CannonExplosive: ['explosive', 1, 'R', 2, 'explosive'], InventoryType.CannonGrapeShot: ['grape_shot', 4, 'R', 2, 'explosive'], InventoryType.CannonFlamingSkull: ['flaming_skull', 8, 'P', 0, 'round'], InventoryType.CannonThunderbolt: ['thunderbolt', 13, 'M', 0, 'thunderbolt'], InventoryType.CannonFury: ['fury', 14, 'P', 0, 'round'], InventoryType.CannonBullet: ['bullet', 2, 'R', 0, 'round'], InventoryType.CannonGasCloud: ['gas_cloud', 3, 'M', 4, 'cloud'], InventoryType.CannonSkull: ['skull_ammo', 5, 'P', 0, 'round'], InventoryType.CannonFirebrand: ['firebrand', 6, 'R', 0, 'round'], InventoryType.CannonFlameCloud: ['flame_cloud', 7, 'M', 3, 'explosive'], InventoryType.CannonBarShot: ['bar_shot', 9, 'R', 2, 'shotgun'], InventoryType.CannonKnives: ['knives', 10, 'P', 0, 'round'], InventoryType.CannonMine: ['mine', 11, 'R', 0, 'mine'], InventoryType.CannonBarnacles: ['barnacles', 12, 'M', 0, 'round'], InventoryType.CannonComet: ['comet', 15, 'M', 2, 'explosive']}
MAX_AMMO = InventoryType.CannonFury

def getCannonballFlightTime(startPos, endPos, power):
    return 3
# okay decompiling .\pirates\battle\CannonGlobals.pyc
