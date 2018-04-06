# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.ship.ShipGlobals
import copy
import math
import random

from direct.actor import Actor
from direct.showbase.PythonUtil import Enum
from direct.task import Task
from pandac.PandaModules import *
from pirates.uberdog.UberDogGlobals import *
from pirates.uberdog.UberDogGlobals import InventoryType

AI_RAM_LATENCY_BUFFER = 500
BROADSIDE_MAX_AUTOAIM_DIST = 2000
BROADSIDE_LEFT = 0
BROADSIDE_RIGHT = 1
AI_SHIP = 0
PLAYER_SHIP = 1
BREAK_HP_LOSS = 0.1
SIDE_BREAK_HP_LOSS = 0.2
SHIP_MOVIE_BOARD = 0
SHIP_MOVIE_UNBOARD = 1
SHIP_BOARD_FROM_SWIM = 0
SHIP_BOARD_FROM_WALK = 1
SHIP_HULL = 1
SHIP_CABIN = 2
SHIP_MAST = 3
SHIP_SAIL = 4
SHIP_BOWSPRIT = 5
SHIP_DECOR = 6
SHIP_CANNON = 7
ARMOR_REAR = 0
ARMOR_LEFT = -1
ARMOR_RIGHT = 1
CHARTER_DURATION = 1800
AVOID_SPHERE_RADIUS = 100
FORMATION_AVOID_SPHERE_RADIUS = 100
OBJ_SPHERE_COLL_NAME = 'shipObjSphere'
OBJ_SPHERE_ENTER_EVENT = 'enter' + OBJ_SPHERE_COLL_NAME
OBJ_SPHERE_EXIT_EVENT = 'exit' + OBJ_SPHERE_COLL_NAME
OBJ_SPHERE_AGAIN_EVENT = 'again' + OBJ_SPHERE_COLL_NAME
SHOVE_OFF_TIMER = 45
AT_SEA_TIMER = 3600
SHIP_REPAIR_REFUNDTIME = 600
SUNK_REPAIR_COST_MULTIPLIER = 2
SHIP_REAR_DAMAGE_BONUS = 1.25
DINGHY = 200
INTERCEPTORL1 = 1
INTERCEPTORL2 = 2
INTERCEPTORL3 = 3
INTERCEPTORL4 = 4
MERCHANTL1 = 11
MERCHANTL2 = 12
MERCHANTL3 = 13
MERCHANTL4 = 14
WARSHIPL1 = 21
WARSHIPL2 = 22
WARSHIPL3 = 23
WARSHIPL4 = 24
PLAYER_SHIPS = (
 INTERCEPTORL1, INTERCEPTORL2, INTERCEPTORL3, INTERCEPTORL4, MERCHANTL1, MERCHANTL2, MERCHANTL3, MERCHANTL4, WARSHIPL1, WARSHIPL2, WARSHIPL3, WARSHIPL4)
BLACK_PEARL = 50
DAUNTLESS = 51
FLYING_DUTCHMAN = 52
GOLIATH = 53
JOLLY_ROGER = 54
SKEL_WARSHIPL3 = 60
SKEL_INTERCEPTORL3 = 61
STUMPY_SHIP = 255
NAVY_FERRET = 80
NAVY_GREYHOUND = 81
NAVY_KINGFISHER = 82
NAVY_PREDATOR = 83
NAVY_BULWARK = 84
NAVY_VANGUARD = 85
NAVY_MONARCH = 86
NAVY_COLOSSUS = 87
NAVY_PANTHER = 88
NAVY_CENTURION = 89
NAVY_MAN_O_WAR = 90
NAVY_DREADNOUGHT = 91
EITC_SEA_VIPER = 100
EITC_BLOODHOUND = 101
EITC_BARRACUDA = 102
EITC_CORSAIR = 103
EITC_SENTINEL = 104
EITC_IRONWALL = 105
EITC_OGRE = 106
EITC_BEHEMOTH = 107
EITC_CORVETTE = 108
EITC_MARAUDER = 109
EITC_WARLORD = 110
EITC_JUGGERNAUT = 111
SKEL_PHANTOM = 120
SKEL_REVENANT = 121
SKEL_STORM_REAPER = 122
SKEL_BLACK_HARBINGER = 123
SKEL_DEATH_OMEN = 124
SKEL_SHADOW_CROW_FR = 125
SKEL_HELLHOUND_FR = 126
SKEL_BLOOD_SCOURGE_FR = 127
SKEL_SHADOW_CROW_SP = 128
SKEL_HELLHOUND_SP = 129
SKEL_BLOOD_SCOURGE_SP = 130
MAINMAST_SQUARE = 1
MAINMAST_TRI = 2
AFTMAST_TRI = 3
FOREMAST_MULTI = 4
FOREMAST_TRI = 5
SKEL_MAINMAST_A = 6
SKEL_MAINMAST_B = 7
SKEL_TRIMAST = 8
SKEL_FOREMAST = 9
SKEL_AFTMAST = 10
PLAYER_INTERCEPTORL1 = 1
PLAYER_INTERCEPTORL2 = 2
PLAYER_INTERCEPTORL3 = 3
PLAYER_MERCHANTL1 = 11
PLAYER_MERCHANTL2 = 12
PLAYER_MERCHANTL3 = 13
PLAYER_WARSHIPL1 = 21
PLAYER_WARSHIPL2 = 22
PLAYER_WARSHIPL3 = 23
NPC_INTERCEPTORL1 = 101
NPC_INTERCEPTORL2 = 102
NPC_INTERCEPTORL3 = 103
NPC_INTERCEPTORL4 = 104
NPC_MERCHANTL1 = 111
NPC_MERCHANTL2 = 112
NPC_MERCHANTL3 = 113
NPC_MERCHANTL4 = 114
NPC_WARSHIPL1 = 121
NPC_WARSHIPL2 = 122
NPC_WARSHIPL3 = 123
NPC_WARSHIPL4 = 124
ShipInfoDefs = {INTERCEPTORL1: {'modelClass': INTERCEPTORL1, 'armor': (900, 900, 1200), 'mastInfo': {0: 2, 4: 1}, 'turnMod': 1, 'speedMod': 1, 'accelMod': 1}, INTERCEPTORL2: {'modelClass': INTERCEPTORL2, 'armor': (900, 900, 180), 'mastInfo': {0: 2, 4: 1}, 'turnMod': 1, 'speedMod': 0.9, 'accelMod': 0.9}, INTERCEPTORL3: {'modelClass': INTERCEPTORL3, 'armor': (2100, 2100, 3000), 'mastInfo': {0: 2, 3: 2, 4: 1}, 'turnMod': 1, 'speedMod': 0.8, 'accelMod': 0.8}, INTERCEPTORL4: {'modelClass': INTERCEPTORL3, 'armor': (2100, 2100, 3000), 'mastInfo': {0: 2, 3: 2, 4: 1}, 'turnMod': 1, 'speedMod': 0.8, 'accelMod': 0.8}, MERCHANTL1: {'modelClass': MERCHANTL1, 'armor': (1500, 600, 900), 'mastInfo': {0: 2, 1: 1, 4: 2}, 'turnMod': 0.5, 'speedMod': 0.9, 'accelMod': 0.5}, MERCHANTL2: {'modelClass': MERCHANTL2, 'armor': (2100, 1200, 1500), 'mastInfo': {0: 1, 1: 2, 2: 1, 4: 2}, 'turnMod': 0.5, 'speedMod': 0.8, 'accelMod': 0.5}, MERCHANTL3: {'modelClass': MERCHANTL3, 'armor': (3300, 2400, 2700), 'mastInfo': {0: 2, 1: 2, 2: 2, 4: 2}, 'turnMod': 0.5, 'speedMod': 0.7, 'accelMod': 0.5}, MERCHANTL4: {'modelClass': MERCHANTL3, 'armor': (3300, 2400, 2700), 'mastInfo': {0: 3, 1: 3, 2: 3, 4: 2}, 'turnMod': 0.5, 'speedMod': 0.7, 'accelMod': 0.5}, WARSHIPL1: {'modelClass': WARSHIPL1, 'hp': 2400, 'armor': (1500, 1200, 900), 'mastInfo': {0: 1, 1: 2, 4: 2}, 'turnMod': 0.9, 'speedMod': 0.8, 'accelMod': 0.9}, WARSHIPL2: {'modelClass': WARSHIPL2, 'hp': 4800, 'armor': (3900, 2400, 1800), 'mastInfo': {0: 2, 1: 2, 3: 2, 4: 2}, 'turnMod': 0.9, 'speedMod': 0.7, 'accelMod': 0.8}, WARSHIPL3: {'modelClass': WARSHIPL3, 'hp': 7200, 'armor': (5400, 3600, 3000), 'mastInfo': {0: 2, 1: 3, 3: 2, 4: 2}, 'turnMod': 0.9, 'speedMod': 0.6, 'accelMod': 0.7}, WARSHIPL4: {'modelClass': WARSHIPL4, 'hp': 10000, 'armor': (5400, 3600, 3000), 'mastInfo': {0: 3, 1: 3, 3: 2, 4: 2}, 'turnMod': 0.9, 'speedMod': 0.6, 'accelMod': 0.7}}
SHIP_CLASS_LIST = [
 'DINGHY', 'INTERCEPTORL1', 'INTERCEPTORL2', 'INTERCEPTORL3', 'INTERCEPTORL4', 'MERCHANTL1', 'MERCHANTL2', 'MERCHANTL3', 'WARSHIPL1', 'WARSHIPL2', 'WARSHIPL3', 'WARSHIPL4', 'BLACK_PEARL', 'DAUNTLESS', 'FLYING_DUTCHMAN', 'GOLIATH', 'SKEL_WARSHIPL3', 'SKEL_INTERCEPTORL3', 'STUMPY_SHIP', 'NAVY_FERRET', 'NAVY_GREYHOUND', 'NAVY_KINGFISHER', 'NAVY_PREDATOR', 'NAVY_BULWARK', 'NAVY_VANGUARD', 'NAVY_MONARCH', 'NAVY_COLOSSUS', 'NAVY_PANTHER', 'NAVY_CENTURION', 'NAVY_MAN_O_WAR', 'NAVY_DREADNOUGHT', 'EITC_SEA_VIPER', 'EITC_BLOODHOUND', 'EITC_BARRACUDA', 'EITC_CORSAIR', 'EITC_SENTINEL', 'EITC_IRONWALL', 'EITC_OGRE', 'EITC_BEHEMOTH', 'EITC_CORVETTE', 'EITC_MARAUDER', 'EITC_WARLORD', 'EITC_JUGGERNAUT', 'SKEL_PHANTOM', 'SKEL_REVENANT', 'SKEL_STORM_REAPER', 'SKEL_BLACK_HARBINGER', 'SKEL_DEATH_OMEN', 'SKEL_SHADOW_CROW_FR', 'SKEL_HELLHOUND_FR', 'SKEL_BLOOD_SCOURGE_FR', 'SKEL_SHADOW_CROW_SP', 'SKEL_HELLHOUND_SP', 'SKEL_BLOOD_SCOURGE_SP']

def getShipSizeIndex(shipClass):
    return shipClass % 10 - 1


WAR_CABINL1A = 1
WAR_CABINL2A = 5
WAR_CABINL2B = 6
WAR_CABINL3A = 11
MERCH_CABINL1A = 21
MERCH_CABINL2A = 25
MERCH_CABINL3A = 31
INT_CABINL1A = 41
INT_CABINL2A = 45
INT_CABINL3A = 51
SKEL_WAR_CABINL3A = 52
BLACK_PEARL_CABIN = 200
GOLIATH_CABIN = 212
_cabinToType = {WAR_CABINL1A: 0, WAR_CABINL2A: 0, WAR_CABINL2B: 1, WAR_CABINL3A: 0, MERCH_CABINL1A: 0, MERCH_CABINL2A: 0, MERCH_CABINL3A: 0, INT_CABINL1A: -1, INT_CABINL2A: -1, INT_CABINL3A: -1, SKEL_WAR_CABINL3A: 0, BLACK_PEARL_CABIN: 0, GOLIATH_CABIN: 0}

def getCabinType(shipClass):
    cabinId = __baseShipConfigs[shipClass]['setCabinType']
    if cabinId:
        return _cabinToType[cabinId]
    return -1


def getHullInfo(shipClass):
    shipInfo = __baseShipConfigs[shipClass]
    hullInfo = [[shipInfo['setHullTextureIndex'], shipInfo['setHullColorIndex']], [shipInfo['setStripeTextureIndex'], shipInfo['setStripeColorIndex']], [shipInfo['setPatternTextureIndex'], shipInfo['setPatternColorIndex']]]
    for s in hullInfo:
        for p in s:
            p += [0] * (3 - len(p))

    return hullInfo


def getMastInfo(shipClass):
    shipInfo = __baseShipConfigs[shipClass]
    mastInfo = {}
    mast1 = shipInfo['setMastConfig1']
    mast2 = shipInfo['setMastConfig2']
    mast3 = shipInfo['setMastConfig3']
    mastF = shipInfo['setForemastConfig']
    mastA = shipInfo['setAftmastConfig']
    if mast1 > 0:
        mastInfo[0] = __mastClassification[mast1][2]
    if mast2 > 0:
        mastInfo[1] = __mastClassification[mast2][2]
    if mast3 > 0:
        mastInfo[2] = __mastClassification[mast3][2]
    if mastF > 0:
        mastInfo[3] = 1
    if mastA > 0:
        mastInfo[4] = 1
    return mastInfo


MAINMASTL1 = 1
MAINMASTL2 = 2
MAINMASTL3 = 3
MAINMASTL4 = 4
MAINMASTL5 = 5
TRIMASTL1 = 6
TRIMASTL2 = 7
TRIMASTL3 = 8
TRIMASTL4 = 9
TRIMASTL5 = 10
FOREMASTL1 = 11
FOREMASTL2 = 12
FOREMASTL3 = 13
AFTMASTL1 = 14
AFTMASTL2 = 15
AFTMASTL3 = 16
SKEL_MAINMASTL1_A = 17
SKEL_MAINMASTL2_A = 18
SKEL_MAINMASTL3_A = 19
SKEL_MAINMASTL4_A = 20
SKEL_MAINMASTL5_A = 21
SKEL_MAINMASTL1_B = 22
SKEL_MAINMASTL2_B = 23
SKEL_MAINMASTL3_B = 24
SKEL_MAINMASTL4_B = 25
SKEL_MAINMASTL5_B = 26
SKEL_TRIMASTL1 = 27
SKEL_TRIMASTL2 = 28
SKEL_TRIMASTL3 = 29
SKEL_TRIMASTL4 = 30
SKEL_TRIMASTL5 = 31
SKEL_FOREMASTL1 = 32
SKEL_FOREMASTL2 = 33
SKEL_FOREMASTL3 = 34
SKEL_AFTMASTL1 = 35
SKEL_AFTMASTL2 = 36
SKEL_AFTMASTL3 = 37
MAINSAILL1 = 1
MAINSAILL2 = 2
MAINSAILL3 = 3
FORESAILL1 = 4
FORESAILL2 = 5
FORESAILL3 = 6
AFTSAILL1 = 7
AFTSAILL2 = 8
AFTSAILL3 = 9
FLAG = 10
SKELETON = 1
LADY = 2
RAML1 = 101
RAML2 = 102
RAML3 = 103
SKEL_RAML3 = 104
CANNONL1 = InventoryType.CannonL1
CANNONL2 = InventoryType.CannonL2
CANNONL3 = InventoryType.CannonL3
CANNONL4 = InventoryType.CannonL4
SKEL_CANNON_L1 = 250
SKEL_CANNON_L2 = 251
SKEL_CANNON_L3 = 252
BPCANNON = 254
TUTORIAL_CANNON = 255
MAINMAST = 1
FOREMAST = 2
AFTMAST = 3
__mastClassification = {MAINMASTL1: (MAINMAST, 1, 1), MAINMASTL2: (MAINMAST, 2, 2), MAINMASTL3: (MAINMAST, 3, 3), MAINMASTL4: (MAINMAST, 4, 4), MAINMASTL5: (MAINMAST, 5, 5), TRIMASTL1: (MAINMAST, 2, 1), TRIMASTL2: (MAINMAST, 2, 2), TRIMASTL3: (MAINMAST, 2, 3), TRIMASTL4: (MAINMAST, 2, 4), TRIMASTL5: (MAINMAST, 2, 5), FOREMASTL1: (FOREMAST, 1, 1), FOREMASTL2: (FOREMAST, 1, 2), FOREMASTL3: (FOREMAST, 1, 3), AFTMASTL1: (AFTMAST, 1, 1), AFTMASTL2: (AFTMAST, 1, 2), AFTMASTL3: (AFTMAST, 1, 3), SKEL_MAINMASTL1_A: (MAINMAST, 1, 1), SKEL_MAINMASTL2_A: (MAINMAST, 2, 2), SKEL_MAINMASTL3_A: (MAINMAST, 3, 3), SKEL_MAINMASTL4_A: (MAINMAST, 4, 4), SKEL_MAINMASTL5_A: (MAINMAST, 5, 5), SKEL_MAINMASTL1_B: (MAINMAST, 1, 1), SKEL_MAINMASTL2_B: (MAINMAST, 2, 2), SKEL_MAINMASTL3_B: (MAINMAST, 3, 3), SKEL_MAINMASTL4_B: (MAINMAST, 4, 4), SKEL_MAINMASTL5_B: (MAINMAST, 5, 5), SKEL_TRIMASTL1: (MAINMAST, 2, 1), SKEL_TRIMASTL2: (MAINMAST, 2, 2), SKEL_TRIMASTL3: (MAINMAST, 2, 3), SKEL_TRIMASTL4: (MAINMAST, 2, 4), SKEL_TRIMASTL5: (MAINMAST, 2, 5), SKEL_FOREMASTL1: (FOREMAST, 2, 1), SKEL_FOREMASTL2: (FOREMAST, 2, 2), SKEL_FOREMASTL3: (FOREMAST, 2, 3), SKEL_AFTMASTL1: (AFTMAST, 1, 1), SKEL_AFTMASTL2: (AFTMAST, 1, 2), SKEL_AFTMASTL3: (AFTMAST, 1, 3)}

def getMastClassification(mastType):
    return __mastClassification.get(mastType)


defaultAcceleration = 20
defaultMaxSpeed = 120
defaultMaxReverseSpeed = defaultMaxSpeed / 2.5
defaultReverseAcceleration = defaultAcceleration / 2.5
defaultMaxReverseAcceleration = 10
defaultTurn = 6
defaultMaxTurn = 20
defaultShipMass = 1.0
defaultWaterIntake = 0.05
__hullStats = {WARSHIPL1: {'maxHp': 4200, 'maxArrayHp': [1000, 600, 600, 450, 450, 300, 300, 450, 450], 'maxSp': 900, 'maxCargo': 5, 'maxCrew': 8, 'maxCannons': 8, 'maxBroadsides': 10, 'rammingPower': 450, 'acceleration': 0.7 * defaultAcceleration, 'maxSpeed': 0.7 * defaultMaxSpeed, 'reverseAcceleration': 0.7 * defaultReverseAcceleration, 'maxReverseSpeed': 0.7 * defaultMaxReverseAcceleration, 'turn': 0.6 * defaultTurn, 'maxTurn': 0.6 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, WARSHIPL2: {'maxHp': 8400, 'maxArrayHp': [1500, 1200, 1200, 1150, 1150, 900, 900, 1150, 1150], 'maxSp': 1400, 'maxCargo': 9, 'maxCrew': 10, 'maxCannons': 10, 'maxBroadsides': 14, 'rammingPower': 900, 'acceleration': 0.7 * defaultAcceleration, 'maxSpeed': 0.7 * defaultMaxSpeed, 'reverseAcceleration': 0.7 * defaultReverseAcceleration, 'maxReverseSpeed': 0.7 * defaultMaxReverseAcceleration, 'turn': 0.6 * defaultTurn, 'maxTurn': 0.6 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, WARSHIPL3: {'maxHp': 12600, 'maxArrayHp': [2500, 1800, 1800, 1500, 1500, 1200, 1200, 1500, 1500], 'maxSp': 2400, 'maxCargo': 12, 'maxCrew': 12, 'maxCannons': 14, 'maxBroadsides': 20, 'rammingPower': 1800, 'acceleration': 0.7 * defaultAcceleration, 'maxSpeed': 0.7 * defaultMaxSpeed, 'reverseAcceleration': 0.7 * defaultReverseAcceleration, 'maxReverseSpeed': 0.7 * defaultMaxReverseAcceleration, 'turn': 0.6 * defaultTurn, 'maxTurn': 0.6 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, WARSHIPL4: {'maxHp': 12600, 'maxArrayHp': [2500, 1800, 1800, 1500, 1500, 1200, 1200, 1500, 1500], 'maxSp': 2400, 'maxCargo': 12, 'maxCrew': 12, 'maxCannons': 14, 'maxBroadsides': 20, 'rammingPower': 1800, 'acceleration': 0.7 * defaultAcceleration, 'maxSpeed': 0.7 * defaultMaxSpeed, 'reverseAcceleration': 0.7 * defaultReverseAcceleration, 'maxReverseSpeed': 0.7 * defaultMaxReverseAcceleration, 'turn': 0.6 * defaultTurn, 'maxTurn': 0.6 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, MERCHANTL1: {'maxHp': 3600, 'maxArrayHp': [1400, 300, 300, 450, 450, 750, 750], 'maxSp': 1100, 'maxCargo': 7, 'maxCrew': 6, 'maxCannons': 4, 'maxBroadsides': 10, 'rammingPower': 300, 'acceleration': 0.6 * defaultAcceleration, 'maxSpeed': 0.6 * defaultMaxSpeed, 'reverseAcceleration': 0.6 * defaultReverseAcceleration, 'maxReverseSpeed': 0.6 * defaultMaxReverseAcceleration, 'turn': 0.6 * defaultTurn, 'maxTurn': 0.6 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 14.0}, MERCHANTL2: {'maxHp': 7200, 'maxArrayHp': [2000, 600, 600, 750, 750, 1050, 1050], 'maxSp': 1400, 'maxCargo': 11, 'maxCrew': 8, 'maxCannons': 8, 'maxBroadsides': 18, 'rammingPower': 600, 'acceleration': 0.6 * defaultAcceleration, 'maxSpeed': 0.6 * defaultMaxSpeed, 'reverseAcceleration': 0.6 * defaultReverseAcceleration, 'maxReverseSpeed': 0.6 * defaultMaxReverseAcceleration, 'turn': 0.6 * defaultTurn, 'maxTurn': 0.6 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 14.0}, MERCHANTL3: {'maxHp': 10800, 'maxArrayHp': [3200, 1200, 1200, 1350, 1350, 1650, 1650], 'maxSp': 3100, 'maxCargo': 16, 'maxCrew': 10, 'maxCannons': 10, 'maxBroadsides': 24, 'rammingPower': 1200, 'acceleration': 0.6 * defaultAcceleration, 'maxSpeed': 0.6 * defaultMaxSpeed, 'reverseAcceleration': 0.6 * defaultReverseAcceleration, 'maxReverseSpeed': 0.6 * defaultMaxReverseAcceleration, 'turn': 0.6 * defaultTurn, 'maxTurn': 0.6 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 14.0}, MERCHANTL4: {}, INTERCEPTORL1: {'maxHp': 2400, 'maxArrayHp': [800, 450, 450, 600, 600, 450, 450], 'maxSp': 800, 'maxCargo': 3, 'maxCrew': 3, 'maxCannons': 2, 'maxBroadsides': 6, 'rammingPower': 150, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.8 * defaultTurn, 'maxTurn': 0.8 * defaultMaxTurn, 'mass': 20.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 5.0}, INTERCEPTORL2: {'maxHp': 4800, 'maxArrayHp': [1200, 600, 600, 900, 900, 600, 600], 'maxSp': 800, 'maxCargo': 6, 'maxCrew': 6, 'maxCannons': 6, 'maxBroadsides': 10, 'rammingPower': 300, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.8 * defaultTurn, 'maxTurn': 0.8 * defaultMaxTurn, 'mass': 30.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 5.0}, INTERCEPTORL3: {'maxHp': 7200, 'maxArrayHp': [2000, 1050, 1050, 1500, 1500, 1050, 1050], 'maxSp': 1000, 'maxCargo': 9, 'maxCrew': 9, 'maxCannons': 8, 'maxBroadsides': 14, 'rammingPower': 600, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.8 * defaultTurn, 'maxTurn': 0.8 * defaultMaxTurn, 'mass': 40.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 5.0}, INTERCEPTORL4: {}, STUMPY_SHIP: {'maxHp': 2400, 'maxArrayHp': [800, 450, 450, 600, 600, 450, 450], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 2, 'maxCannons': 2, 'maxBroadsides': 0, 'rammingPower': 150, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.7 * defaultTurn, 'maxTurn': 0.7 * defaultMaxTurn, 'mass': 20.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 5.0}, BLACK_PEARL: {'maxHp': 12000, 'maxArrayHp': [2400, 1800, 1800, 1500, 1500, 1200, 1200, 1500, 1500], 'maxSp': 0, 'maxCargo': 18, 'maxCrew': 12, 'maxCannons': 14, 'maxBroadsides': 18, 'rammingPower': 2000, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.7 * defaultTurn, 'maxTurn': 0.7 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, GOLIATH: {'maxHp': 3500, 'maxArrayHp': [3000, 1800, 1800, 1500, 1500, 1200, 1200, 1500, 1500], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 8, 'maxCannons': 18, 'maxBroadsides': 18, 'rammingPower': 900, 'acceleration': 1.0 * defaultAcceleration, 'maxSpeed': 1.2 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.8 * defaultTurn, 'maxTurn': 0.8 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, NAVY_PANTHER: {'maxHp': 1700, 'maxArrayHp': [1000, 600, 600, 450, 450, 300, 300, 450, 450], 'maxSp': 0, 'maxCargo': 2, 'maxCrew': 3, 'maxCannons': 8, 'maxBroadsides': 10, 'rammingPower': 150, 'acceleration': 0.9 * defaultAcceleration, 'maxSpeed': 0.9 * defaultMaxSpeed, 'reverseAcceleration': 0.9 * defaultReverseAcceleration, 'maxReverseSpeed': 0.9 * defaultMaxReverseAcceleration, 'turn': 0.5 * defaultTurn, 'maxTurn': 0.5 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, NAVY_CENTURION: {'maxHp': 2100, 'maxArrayHp': [2200, 1200, 1200, 1050, 1050, 900, 900, 1050, 1050], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 6, 'maxCannons': 10, 'maxBroadsides': 14, 'rammingPower': 450, 'acceleration': 0.9 * defaultAcceleration, 'maxSpeed': 0.9 * defaultMaxSpeed, 'reverseAcceleration': 0.9 * defaultReverseAcceleration, 'maxReverseSpeed': 0.9 * defaultMaxReverseAcceleration, 'turn': 0.5 * defaultTurn, 'maxTurn': 0.5 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, NAVY_MAN_O_WAR: {'maxHp': 2100, 'maxArrayHp': [3100, 1800, 1800, 1500, 1500, 1200, 1200, 1500, 1500], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 8, 'maxCannons': 14, 'maxBroadsides': 20, 'rammingPower': 900, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, NAVY_DREADNOUGHT: {'maxHp': 2100, 'maxArrayHp': [3100, 1800, 1800, 1500, 1500, 1200, 1200, 1500, 1500], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 8, 'maxCannons': 14, 'maxBroadsides': 20, 'rammingPower': 900, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, NAVY_BULWARK: {'maxHp': 1400, 'maxArrayHp': [1400, 300, 300, 450, 450, 750, 750], 'maxSp': 0, 'maxCargo': 2, 'maxCrew': 6, 'maxCannons': 4, 'maxBroadsides': 10, 'rammingPower': 150, 'acceleration': 0.9 * defaultAcceleration, 'maxSpeed': 0.9 * defaultMaxSpeed, 'reverseAcceleration': 0.9 * defaultReverseAcceleration, 'maxReverseSpeed': 0.9 * defaultMaxReverseAcceleration, 'turn': 0.5 * defaultTurn, 'maxTurn': 0.5 * defaultMaxTurn, 'mass': 40.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 14.0}, NAVY_VANGUARD: {'maxHp': 1800, 'maxArrayHp': [2000, 600, 600, 750, 750, 1050, 1050], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 10, 'maxCannons': 8, 'maxBroadsides': 18, 'rammingPower': 300, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.5 * defaultTurn, 'maxTurn': 0.5 * defaultMaxTurn, 'mass': 70.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 14.0}, NAVY_MONARCH: {'maxHp': 1800, 'maxArrayHp': [3200, 1200, 1200, 1350, 1350, 1650, 1650], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 14, 'maxCannons': 10, 'maxBroadsides': 24, 'rammingPower': 600, 'acceleration': 0.7 * defaultAcceleration, 'maxSpeed': 0.7 * defaultMaxSpeed, 'reverseAcceleration': 0.7 * defaultReverseAcceleration, 'maxReverseSpeed': 0.7 * defaultMaxReverseAcceleration, 'turn': 0.5 * defaultTurn, 'maxTurn': 0.5 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 14.0}, NAVY_COLOSSUS: {'maxHp': 1800, 'maxArrayHp': [3200, 1200, 1200, 1350, 1350, 1650, 1650], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 14, 'maxCannons': 10, 'maxBroadsides': 24, 'rammingPower': 600, 'acceleration': 0.7 * defaultAcceleration, 'maxSpeed': 0.7 * defaultMaxSpeed, 'reverseAcceleration': 0.7 * defaultReverseAcceleration, 'maxReverseSpeed': 0.7 * defaultMaxReverseAcceleration, 'turn': 0.5 * defaultTurn, 'maxTurn': 0.5 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 14.0}, NAVY_FERRET: {'maxHp': 1000, 'maxArrayHp': [800, 450, 450, 600, 600, 450, 450], 'maxSp': 0, 'maxCargo': 1, 'maxCrew': 4, 'maxCannons': 2, 'maxBroadsides': 6, 'rammingPower': 75, 'acceleration': 1.8 * defaultAcceleration, 'maxSpeed': 1.8 * defaultMaxSpeed, 'reverseAcceleration': 1.8 * defaultReverseAcceleration, 'maxReverseSpeed': 1.8 * defaultMaxReverseAcceleration, 'turn': 1.4 * defaultTurn, 'maxTurn': 1.4 * defaultMaxTurn, 'mass': 20.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 5.0}, NAVY_GREYHOUND: {'maxHp': 1200, 'maxArrayHp': [800, 450, 450, 900, 900, 450, 450], 'maxSp': 0, 'maxCargo': 2, 'maxCrew': 8, 'maxCannons': 6, 'maxBroadsides': 10, 'rammingPower': 225, 'acceleration': 1.0 * defaultAcceleration, 'maxSpeed': 1.0 * defaultMaxSpeed, 'reverseAcceleration': 1.0 * defaultReverseAcceleration, 'maxReverseSpeed': 1.0 * defaultMaxReverseAcceleration, 'turn': 0.9 * defaultTurn, 'maxTurn': 0.9 * defaultMaxTurn, 'mass': 30.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 5.0}, NAVY_KINGFISHER: {'maxHp': 1200, 'maxArrayHp': [2000, 1050, 1050, 1500, 1500, 1050, 1050], 'maxSp': 0, 'maxCargo': 2, 'maxCrew': 3, 'maxCannons': 8, 'maxBroadsides': 14, 'rammingPower': 450, 'acceleration': 0.9 * defaultAcceleration, 'maxSpeed': 0.9 * defaultMaxSpeed, 'reverseAcceleration': 0.9 * defaultReverseAcceleration, 'maxReverseSpeed': 0.9 * defaultMaxReverseAcceleration, 'turn': 0.8 * defaultTurn, 'maxTurn': 0.8 * defaultMaxTurn, 'mass': 40.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 5.0}, NAVY_PREDATOR: {'maxHp': 1200, 'maxArrayHp': [2000, 1050, 1050, 1500, 1500, 1050, 1050], 'maxSp': 0, 'maxCargo': 2, 'maxCrew': 3, 'maxCannons': 8, 'maxBroadsides': 14, 'rammingPower': 450, 'acceleration': 0.9 * defaultAcceleration, 'maxSpeed': 0.9 * defaultMaxSpeed, 'reverseAcceleration': 0.9 * defaultReverseAcceleration, 'maxReverseSpeed': 0.9 * defaultMaxReverseAcceleration, 'turn': 0.8 * defaultTurn, 'maxTurn': 0.8 * defaultMaxTurn, 'mass': 40.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 5.0}, EITC_CORVETTE: {'maxHp': 1700, 'maxArrayHp': [1000, 600, 600, 450, 450, 300, 300, 450, 450], 'maxSp': 0, 'maxCargo': 2, 'maxCrew': 3, 'maxCannons': 8, 'maxBroadsides': 10, 'rammingPower': 150, 'acceleration': 0.9 * defaultAcceleration, 'maxSpeed': 0.9 * defaultMaxSpeed, 'reverseAcceleration': 0.9 * defaultReverseAcceleration, 'maxReverseSpeed': 0.9 * defaultMaxReverseAcceleration, 'turn': 0.5 * defaultTurn, 'maxTurn': 0.5 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, EITC_MARAUDER: {'maxHp': 2100, 'maxArrayHp': [2200, 1200, 1200, 1050, 1050, 900, 900, 1050, 1050], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 6, 'maxCannons': 10, 'maxBroadsides': 14, 'rammingPower': 450, 'acceleration': 0.9 * defaultAcceleration, 'maxSpeed': 0.9 * defaultMaxSpeed, 'reverseAcceleration': 0.9 * defaultReverseAcceleration, 'maxReverseSpeed': 0.9 * defaultMaxReverseAcceleration, 'turn': 0.5 * defaultTurn, 'maxTurn': 0.5 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, EITC_WARLORD: {'maxHp': 2100, 'maxArrayHp': [3100, 1800, 1800, 1500, 1500, 1200, 1200, 1500, 1500], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 8, 'maxCannons': 14, 'maxBroadsides': 20, 'rammingPower': 900, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, EITC_JUGGERNAUT: {'maxHp': 2100, 'maxArrayHp': [3100, 1800, 1800, 1500, 1500, 1200, 1200, 1500, 1500], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 8, 'maxCannons': 14, 'maxBroadsides': 20, 'rammingPower': 900, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, EITC_SENTINEL: {'maxHp': 1400, 'maxArrayHp': [1400, 300, 300, 450, 450, 750, 750], 'maxSp': 0, 'maxCargo': 2, 'maxCrew': 6, 'maxCannons': 4, 'maxBroadsides': 10, 'rammingPower': 150, 'acceleration': 0.9 * defaultAcceleration, 'maxSpeed': 0.9 * defaultMaxSpeed, 'reverseAcceleration': 0.9 * defaultReverseAcceleration, 'maxReverseSpeed': 0.9 * defaultMaxReverseAcceleration, 'turn': 0.5 * defaultTurn, 'maxTurn': 0.5 * defaultMaxTurn, 'mass': 40.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 14.0}, EITC_IRONWALL: {'maxHp': 1800, 'maxArrayHp': [2000, 600, 600, 750, 750, 1050, 1050], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 10, 'maxCannons': 8, 'maxBroadsides': 18, 'rammingPower': 300, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.5 * defaultTurn, 'maxTurn': 0.5 * defaultMaxTurn, 'mass': 70.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 14.0}, EITC_OGRE: {'maxHp': 1800, 'maxArrayHp': [3200, 1200, 1200, 1350, 1350, 1650, 1650], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 14, 'maxCannons': 10, 'maxBroadsides': 24, 'rammingPower': 600, 'acceleration': 0.7 * defaultAcceleration, 'maxSpeed': 0.7 * defaultMaxSpeed, 'reverseAcceleration': 0.7 * defaultReverseAcceleration, 'maxReverseSpeed': 0.7 * defaultMaxReverseAcceleration, 'turn': 0.5 * defaultTurn, 'maxTurn': 0.5 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 14.0}, EITC_BEHEMOTH: {'maxHp': 1800, 'maxArrayHp': [3200, 1200, 1200, 1350, 1350, 1650, 1650], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 14, 'maxCannons': 10, 'maxBroadsides': 24, 'rammingPower': 600, 'acceleration': 0.7 * defaultAcceleration, 'maxSpeed': 0.7 * defaultMaxSpeed, 'reverseAcceleration': 0.7 * defaultReverseAcceleration, 'maxReverseSpeed': 0.7 * defaultMaxReverseAcceleration, 'turn': 0.5 * defaultTurn, 'maxTurn': 0.5 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 14.0}, EITC_SEA_VIPER: {'maxHp': 1000, 'maxArrayHp': [800, 450, 450, 600, 600, 450, 450], 'maxSp': 0, 'maxCargo': 1, 'maxCrew': 4, 'maxCannons': 2, 'maxBroadsides': 6, 'rammingPower': 75, 'acceleration': 1.8 * defaultAcceleration, 'maxSpeed': 1.8 * defaultMaxSpeed, 'reverseAcceleration': 1.8 * defaultReverseAcceleration, 'maxReverseSpeed': 1.8 * defaultMaxReverseAcceleration, 'turn': 1.4 * defaultTurn, 'maxTurn': 1.4 * defaultMaxTurn, 'mass': 20.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 5.0}, EITC_BLOODHOUND: {'maxHp': 1200, 'maxArrayHp': [800, 450, 450, 900, 900, 450, 450], 'maxSp': 0, 'maxCargo': 2, 'maxCrew': 8, 'maxCannons': 6, 'maxBroadsides': 10, 'rammingPower': 225, 'acceleration': 1.0 * defaultAcceleration, 'maxSpeed': 1.0 * defaultMaxSpeed, 'reverseAcceleration': 1.0 * defaultReverseAcceleration, 'maxReverseSpeed': 1.0 * defaultMaxReverseAcceleration, 'turn': 0.9 * defaultTurn, 'maxTurn': 0.9 * defaultMaxTurn, 'mass': 30.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 5.0}, EITC_BARRACUDA: {'maxHp': 1200, 'maxArrayHp': [2000, 1050, 1050, 1500, 1500, 1050, 1050], 'maxSp': 0, 'maxCargo': 2, 'maxCrew': 3, 'maxCannons': 8, 'maxBroadsides': 14, 'rammingPower': 450, 'acceleration': 0.9 * defaultAcceleration, 'maxSpeed': 0.9 * defaultMaxSpeed, 'reverseAcceleration': 0.9 * defaultReverseAcceleration, 'maxReverseSpeed': 0.9 * defaultMaxReverseAcceleration, 'turn': 0.8 * defaultTurn, 'maxTurn': 0.8 * defaultMaxTurn, 'mass': 40.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 5.0}, EITC_CORSAIR: {'maxHp': 1200, 'maxArrayHp': [2000, 1050, 1050, 1500, 1500, 1050, 1050], 'maxSp': 0, 'maxCargo': 2, 'maxCrew': 3, 'maxCannons': 8, 'maxBroadsides': 14, 'rammingPower': 450, 'acceleration': 0.9 * defaultAcceleration, 'maxSpeed': 0.9 * defaultMaxSpeed, 'reverseAcceleration': 0.9 * defaultReverseAcceleration, 'maxReverseSpeed': 0.9 * defaultMaxReverseAcceleration, 'turn': 0.8 * defaultTurn, 'maxTurn': 0.8 * defaultMaxTurn, 'mass': 40.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 5.0}, SKEL_PHANTOM: {'maxHp': 2500, 'maxArrayHp': [1300, 1200, 1200, 900, 900, 600, 600], 'maxSp': 0, 'maxCargo': 2, 'maxCrew': 8, 'maxCannons': 8, 'maxBroadsides': 14, 'rammingPower': 600, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, SKEL_REVENANT: {'maxHp': 2500, 'maxArrayHp': [1300, 1200, 1200, 900, 900, 600, 600], 'maxSp': 0, 'maxCargo': 2, 'maxCrew': 8, 'maxCannons': 8, 'maxBroadsides': 14, 'rammingPower': 600, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, SKEL_STORM_REAPER: {'maxHp': 2500, 'maxArrayHp': [1300, 1200, 1200, 900, 900, 600, 600], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 8, 'maxCannons': 8, 'maxBroadsides': 14, 'rammingPower': 600, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, SKEL_BLACK_HARBINGER: {'maxHp': 2500, 'maxArrayHp': [1300, 1200, 1200, 900, 900, 600, 600], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 8, 'maxCannons': 8, 'maxBroadsides': 14, 'rammingPower': 600, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, SKEL_DEATH_OMEN: {'maxHp': 2500, 'maxArrayHp': [1300, 1200, 1200, 900, 900, 600, 600], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 8, 'maxCannons': 8, 'maxBroadsides': 14, 'rammingPower': 600, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, SKEL_SHADOW_CROW_FR: {'maxHp': 2500, 'maxArrayHp': [1100, 1200, 1200, 900, 900, 600, 600], 'maxSp': 0, 'maxCargo': 1, 'maxCrew': 8, 'maxCannons': 6, 'maxBroadsides': 600, 'rammingPower': 0, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, SKEL_HELLHOUND_FR: {'maxHp': 3000, 'maxArrayHp': [1500, 1500, 1500, 1100, 1100, 800, 800], 'maxSp': 0, 'maxCargo': 2, 'maxCrew': 8, 'maxCannons': 6, 'maxBroadsides': 600, 'rammingPower': 0, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, SKEL_BLOOD_SCOURGE_FR: {'maxHp': 4000, 'maxArrayHp': [1900, 2000, 2000, 1500, 1500, 1000, 1000], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 8, 'maxCannons': 6, 'maxBroadsides': 600, 'rammingPower': 0, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, SKEL_SHADOW_CROW_SP: {'maxHp': 2500, 'maxArrayHp': [1100, 1200, 1200, 900, 900, 600, 600], 'maxSp': 0, 'maxCargo': 1, 'maxCrew': 8, 'maxCannons': 6, 'maxBroadsides': 600, 'rammingPower': 0, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, SKEL_HELLHOUND_SP: {'maxHp': 3000, 'maxArrayHp': [1500, 1500, 1500, 1100, 1100, 800, 800], 'maxSp': 0, 'maxCargo': 2, 'maxCrew': 8, 'maxCannons': 6, 'maxBroadsides': 600, 'rammingPower': 0, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}, SKEL_BLOOD_SCOURGE_SP: {'maxHp': 4000, 'maxArrayHp': [1900, 2000, 2000, 1500, 1500, 1000, 1000], 'maxSp': 0, 'maxCargo': 3, 'maxCrew': 8, 'maxCannons': 6, 'maxBroadsides': 600, 'rammingPower': 0, 'acceleration': 0.8 * defaultAcceleration, 'maxSpeed': 0.8 * defaultMaxSpeed, 'reverseAcceleration': 0.8 * defaultReverseAcceleration, 'maxReverseSpeed': 0.8 * defaultMaxReverseAcceleration, 'turn': 0.3 * defaultTurn, 'maxTurn': 0.3 * defaultMaxTurn, 'mass': 100.0, 'waterIntakeDrag': 1.0 * defaultWaterIntake, 'sphereRadius': 30.0}}
__maxHullStats = {}

def getHullStats(hullId):
    return __hullStats.get(hullId)


def getMaxHullStats():
    global __maxHullStats
    if not __maxHullStats:
        for shipClass in PLAYER_SHIPS:
            hullInfo = __hullStats[shipClass]
            for key, val in hullInfo.items():
                __maxHullStats[key] = max(__maxHullStats.get(key, 0), val)

    return __maxHullStats


BaseLevel = {INTERCEPTORL1: 2, MERCHANTL1: 4, WARSHIPL1: 8, INTERCEPTORL2: 12, MERCHANTL2: 16, WARSHIPL2: 20, INTERCEPTORL3: 26, MERCHANTL3: 30, WARSHIPL3: 34, BLACK_PEARL: 40, SKEL_WARSHIPL3: 32, SKEL_INTERCEPTORL3: 26}
WaterlineOffsets = {INTERCEPTORL1: -4, INTERCEPTORL2: -4, INTERCEPTORL3: -4, MERCHANTL1: -4, MERCHANTL2: -4, MERCHANTL3: -4, WARSHIPL1: -4, WARSHIPL2: -4, WARSHIPL3: -4, BLACK_PEARL: -10, GOLIATH: -10, SKEL_WARSHIPL3: -4, SKEL_INTERCEPTORL3: -4}
TiltFakeMass = {INTERCEPTORL1: 1.0, INTERCEPTORL2: 1.4, INTERCEPTORL3: 1.7, MERCHANTL1: 2.5, MERCHANTL2: 3.0, MERCHANTL3: 3.5, WARSHIPL1: 2.5, WARSHIPL2: 3.0, WARSHIPL3: 4.0, BLACK_PEARL: 4.5, GOLIATH: 4.5, SKEL_INTERCEPTORL3: 1.7, SKEL_WARSHIPL3: 4.0}
SamplePoints = Enum('\n    FL, F, FR,\n     L, C,  R,\n    BL, B, BR,\n    ')
SamplePointOffsets = {INTERCEPTORL1: [(0, -11), {SamplePoints.FL: (-13, 29), SamplePoints.F: (0, 29), SamplePoints.FR: (13, 29), SamplePoints.L: (-13, 0), SamplePoints.C: (0, 0), SamplePoints.R: (13, 0), SamplePoints.BL: (-13, -29), SamplePoints.B: (0, -29), SamplePoints.BR: (13, -29)}], INTERCEPTORL2: [(0, -8), {SamplePoints.FL: (-20, 50), SamplePoints.F: (0, 50), SamplePoints.FR: (20, 50), SamplePoints.L: (-20, 0), SamplePoints.C: (0, 0), SamplePoints.R: (20, 0), SamplePoints.BL: (-20, -50), SamplePoints.B: (0, -50), SamplePoints.BR: (20, -50)}], INTERCEPTORL3: [(0, 0), {SamplePoints.FL: (-26, 50), SamplePoints.F: (0, 50), SamplePoints.FR: (26, 50), SamplePoints.L: (-26, 0), SamplePoints.C: (0, 0), SamplePoints.R: (26, 0), SamplePoints.BL: (-26, -50), SamplePoints.B: (0, -50), SamplePoints.BR: (26, -50)}], MERCHANTL1: [(0, 0), {SamplePoints.FL: (-23, 33), SamplePoints.F: (0, 33), SamplePoints.FR: (23, 33), SamplePoints.L: (-23, 0), SamplePoints.C: (0, 0), SamplePoints.R: (23, 0), SamplePoints.BL: (-23, -33), SamplePoints.B: (0, -33), SamplePoints.BR: (23, -33)}], MERCHANTL2: [(0, 0), {SamplePoints.FL: (-35, 60), SamplePoints.F: (0, 60), SamplePoints.FR: (35, 60), SamplePoints.L: (-35, 0), SamplePoints.C: (0, 0), SamplePoints.R: (35, 0), SamplePoints.BL: (-35, -60), SamplePoints.B: (0, -60), SamplePoints.BR: (35, -60)}], MERCHANTL3: [(0, 0), {SamplePoints.FL: (-38, 68), SamplePoints.F: (0, 68), SamplePoints.FR: (38, 68), SamplePoints.L: (-38, 0), SamplePoints.C: (0, 0), SamplePoints.R: (38, 0), SamplePoints.BL: (-38, -68), SamplePoints.B: (0, -68), SamplePoints.BR: (38, -68)}], WARSHIPL1: [(0, -5), {SamplePoints.FL: (-22, 45), SamplePoints.F: (0, 45), SamplePoints.FR: (22, 45), SamplePoints.L: (-22, 0), SamplePoints.C: (0, 0), SamplePoints.R: (22, 0), SamplePoints.BL: (-22, -45), SamplePoints.B: (0, -45), SamplePoints.BR: (22, -45)}], WARSHIPL2: [(0, 0), {SamplePoints.FL: (-28, 64), SamplePoints.F: (0, 64), SamplePoints.FR: (28, 64), SamplePoints.L: (-28, 0), SamplePoints.C: (0, 0), SamplePoints.R: (28, 0), SamplePoints.BL: (-28, -64), SamplePoints.B: (0, -64), SamplePoints.BR: (28, -64)}], WARSHIPL3: [(0, -5), {SamplePoints.FL: (-42, 84), SamplePoints.F: (0, 84), SamplePoints.FR: (42, 84), SamplePoints.L: (-42, 0), SamplePoints.C: (0, 0), SamplePoints.R: (42, 0), SamplePoints.BL: (-42, -84), SamplePoints.B: (0, -84), SamplePoints.BR: (42, -84)}], BLACK_PEARL: [(0, -5), {SamplePoints.FL: (-32, 94), SamplePoints.F: (0, 94), SamplePoints.FR: (32, 94), SamplePoints.L: (-32, 0), SamplePoints.C: (0, 0), SamplePoints.R: (32, 0), SamplePoints.BL: (-32, -94), SamplePoints.B: (0, -94), SamplePoints.BR: (32, -94)}], GOLIATH: [(0, -5), {SamplePoints.FL: (-32, 94), SamplePoints.F: (0, 94), SamplePoints.FR: (32, 94), SamplePoints.L: (-32, 0), SamplePoints.C: (0, 0), SamplePoints.R: (32, 0), SamplePoints.BL: (-32, -94), SamplePoints.B: (0, -94), SamplePoints.BR: (32, -94)}], SKEL_INTERCEPTORL3: [(0, 0), {SamplePoints.FL: (-26, 50), SamplePoints.F: (0, 50), SamplePoints.FR: (26, 50), SamplePoints.L: (-26, 0), SamplePoints.C: (0, 0), SamplePoints.R: (26, 0), SamplePoints.BL: (-26, -50), SamplePoints.B: (0, -50), SamplePoints.BR: (26, -50)}], SKEL_WARSHIPL3: [(0, -5), {SamplePoints.FL: (-42, 84), SamplePoints.F: (0, 84), SamplePoints.FR: (42, 84), SamplePoints.L: (-42, 0), SamplePoints.C: (0, 0), SamplePoints.R: (42, 0), SamplePoints.BL: (-42, -84), SamplePoints.B: (0, -84), SamplePoints.BR: (42, -84)}]}
__shipLevelStatMultiplier = {0: (0.5, 0, 10), 1: (0.7, 0, 15), 2: (0.9, 0, 20), 3: (1.1, 0, 25), 4: (1.3, 0, 30), 5: (1.5, 0, 35), 6: (1.7, 0, 40), 7: (1.9, 0, 45), 8: (2.1, 0, 50), 9: (2.3, 0, 55), 10: (2.5, 0, 60), 11: (2.7, 0, 65), 12: (2.9, 0, 70), 13: (3.1, 0, 75), 14: (3.3, 0, 80), 15: (3.5, 0, 85), 16: (3.7, 0, 90), 17: (3.9, 0, 95), 18: (4.1, 0, 100), 19: (4.3, 0, 105), 20: (4.5, 0, 110), 21: (4.7, 0, 115), 22: (4.9, 0, 120), 23: (5.1, 0, 125), 24: (5.3, 0, 130), 25: (5.5, 0, 135), 26: (5.7, 0, 140), 27: (5.9, 0, 145), 28: (6.1, 0, 150), 29: (6.3, 0, 155), 30: (6.5, 0, 160), 31: (6.7, 0, 165), 32: (6.9, 0, 170), 33: (7.1, 0, 175), 34: (7.3, 0, 180), 35: (7.5, 0, 185), 36: (7.7, 0, 190), 37: (7.9, 0, 195), 38: (8.1, 0, 200), 39: (8.3, 0, 205), 40: (8.5, 0, 210), 41: (8.7, 0, 215), 42: (8.9, 0, 220), 43: (9.1, 0, 225), 44: (9.3, 0, 230), 45: (9.5, 0, 235)}

def getModifiedShipStats(level):
    modifiers = __shipLevelStatMultiplier.get(level)
    return modifiers


def getShipExp(level):
    modifiers = __shipLevelStatMultiplier.get(level)
    if modifiers:
        return modifiers[2]
    return modifiers


__boardingSphere = {DINGHY: ((Vec3(-1.15, 3.675, 3.5), 90), 7), WARSHIPL1: ((Vec3(0, 0, 100), 90), 25), WARSHIPL2: ((Vec3(0, 0, 100), 90), 45), WARSHIPL3: ((Vec3(-6.0, 13.0, 21.9), -90), 60), WARSHIPL4: ((Vec3(0, 0, 100), 90), 60), MERCHANTL1: ((Vec3(0, 0, 100), 90), 25), MERCHANTL2: ((Vec3(8, -11, 33), 90), 40), MERCHANTL3: ((Vec3(0, 0, 100), 90), 55), MERCHANTL4: ((Vec3(0, 0, 100), 90), 75), INTERCEPTORL1: ((Vec3(2.74993, 23.197, 9.27622), 90), 25), INTERCEPTORL2: ((Vec3(0, 0, 100), 90), 35), INTERCEPTORL3: ((Vec3(11.899, -1.7117, 21.8932), -29), 45), INTERCEPTORL4: ((Vec3(0, 0, 100), 90), 55), BLACK_PEARL: ((Vec3(-6.0, 13.0, 21.9), -90), 60), GOLIATH: ((Vec3(-6.0, 13.0, 21.9), -90), 60), STUMPY_SHIP: ((Vec3(2.74993, 23.197, 9.27622), 90), 25), SKEL_WARSHIPL3: ((Vec3(-6.0, 13.0, 21.9), -90), 60), SKEL_INTERCEPTORL3: ((Vec3(11.899, -1.7117, 21.8932), -29), 45)}
__exitSphere = {DINGHY: (0, 0, 0), WARSHIPL1: (21.26, 13.44, 21.93), WARSHIPL2: (21.26, 13.44, 21.93), WARSHIPL3: (21.26, 13.44, 21.93), WARSHIPL4: (21.26, 13.44, 21.93), MERCHANTL1: (-5.44, 6.735, 12.278), MERCHANTL2: (-5.44, 6.735, 12.278), MERCHANTL3: (-5.44, 6.735, 12.278), MERCHANTL4: (-5.44, 6.735, 12.278), INTERCEPTORL1: (2.354, -15.201, 5.493), INTERCEPTORL2: (2.354, -15.201, 5.493), INTERCEPTORL3: (2.354, -15.201, 5.493), INTERCEPTORL4: (2.354, -15.201, 5.493), BLACK_PEARL: (21.26, 13.44, 21.93), GOLIATH: (21.26, 13.44, 21.93), SKEL_WARSHIPL3: (21.26, 13.44, 21.93), SKEL_INTERCEPTORL3: (2.354, -15.201, 5.493)}
__rammingSphereValues = {DINGHY: (0, 0, 0, 5), WARSHIPL1: (0, -140, 10, 30), WARSHIPL2: (0, -160, 15, 40), WARSHIPL3: (0, -180, 20, 50), WARSHIPL4: (0, -200, 25, 60), MERCHANTL1: (0, -120, 10, 30), MERCHANTL2: (0, -140, 15, 40), MERCHANTL3: (0, -160, 20, 50), MERCHANTL4: (0, -180, 25, 60), INTERCEPTORL1: (0, -110, 10, 30), INTERCEPTORL2: (0, -130, 15, 40), INTERCEPTORL3: (0, -150, 20, 50), INTERCEPTORL4: (0, -170, 25, 60), BLACK_PEARL: (0, -190, 20, 50), GOLIATH: (0, -190, 20, 50), SKEL_WARSHIPL3: (0, -180, 20, 50), SKEL_INTERCEPTORL3: (0, -150, 20, 50)}
__shipLowLODScale = {DINGHY: 0, WARSHIPL1: 0.5, WARSHIPL2: 0.8, WARSHIPL3: 1.0, WARSHIPL4: 1.0, MERCHANTL1: 0.6, MERCHANTL2: 1.0, MERCHANTL3: 1.3, MERCHANTL4: 1.0, INTERCEPTORL1: 0.58, INTERCEPTORL2: 1.005, INTERCEPTORL3: 1.3, INTERCEPTORL4: 1.0, BLACK_PEARL: 1.0, GOLIATH: 1.0, SKEL_WARSHIPL3: 1.0, SKEL_INTERCEPTORL3: 1.0}
__shipLowLODPosOffset = {DINGHY: Vec3(0, 0, 0), WARSHIPL1: Vec3(0, 2, 2), WARSHIPL2: Vec3(0, -9, 4), WARSHIPL3: Vec3(0, -1, 1.3), WARSHIPL4: Vec3(0, 0, 0), MERCHANTL1: Vec3(0, 0, 0), MERCHANTL2: Vec3(0, 0, 0), MERCHANTL3: Vec3(0, 2, 6), MERCHANTL4: Vec3(0, 0, 0), INTERCEPTORL1: Vec3(0, 6, -3), INTERCEPTORL2: Vec3(0, 0, 0), INTERCEPTORL3: Vec3(0, 3, -3.2), INTERCEPTORL4: Vec3(0, 0, 0), BLACK_PEARL: Vec3(0, 0, 0), GOLIATH: Vec3(0, 0, 0), SKEL_WARSHIPL3: Vec3(0, 0, 0), SKEL_INTERCEPTORL3: Vec3(0, 0, 0)}
BOARDING_POS_H_INDEX = 0
BOARDING_SCALE_INDEX = 1
__broadsideMaxDelay = {DINGHY: 0, WARSHIPL1: 0.6, WARSHIPL2: 1.0, WARSHIPL3: 1.5, WARSHIPL4: 1.5, MERCHANTL1: 0.8, MERCHANTL2: 1.6, MERCHANTL3: 1.75, MERCHANTL4: 1.75, INTERCEPTORL1: 0.3, INTERCEPTORL2: 0.5, INTERCEPTORL3: 0.75, INTERCEPTORL4: 1.0, BLACK_PEARL: 1.25, GOLIATH: 1.2, SKEL_WARSHIPL3: 1.25, SKEL_INTERCEPTORL3: 1.0}

def getBroadsideMaxDelay(modelClass):
    shipData = __broadsideMaxDelay.get(modelClass)
    return shipData


def getBoardingSpherePosH(shipClass):
    return __boardingSphere.get(shipClass)[BOARDING_POS_H_INDEX]


def getBoardingSphereScale(shipClass):
    return __boardingSphere.get(shipClass)[BOARDING_SCALE_INDEX]


def getExitSpherePos(shipClass):
    return __exitSphere.get(shipClass)


def getRammingSphereScale(shipClass):
    return __rammingSphereValues.get(shipClass)


def getLowLODScale(shipClass):
    return __shipLowLODScale.get(shipClass)


def getLowLODPosOffset(shipClass):
    return __shipLowLODPosOffset.get(shipClass)


__holeSizes = {MAINMASTL1: (14, 4, 5), MAINMASTL2: (24, 3, 5), MAINMASTL3: (30, 3, 5), MAINMASTL4: (36, 2, 5), MAINMASTL5: (42, 2, 5), TRIMASTL1: (6, 6, 5), TRIMASTL2: (8, 5, 5), TRIMASTL3: (12, 4, 5), TRIMASTL4: (16, 3, 5), TRIMASTL5: (20, 2, 5), FOREMASTL1: (8, 4, 5), FOREMASTL2: (12, 3, 5), FOREMASTL3: (16, 2, 5), AFTMASTL1: (14, 4, 5), AFTMASTL2: (24, 3, 5), AFTMASTL3: (30, 2, 5), SKEL_MAINMASTL1_A: (14, 4, 5), SKEL_MAINMASTL2_A: (24, 3, 5), SKEL_MAINMASTL3_A: (30, 3, 5), SKEL_MAINMASTL4_A: (36, 2, 5), SKEL_MAINMASTL5_A: (42, 2, 5), SKEL_MAINMASTL1_B: (14, 4, 5), SKEL_MAINMASTL2_B: (24, 3, 5), SKEL_MAINMASTL3_B: (30, 3, 5), SKEL_MAINMASTL4_B: (36, 2, 5), SKEL_MAINMASTL5_B: (42, 2, 5), SKEL_TRIMASTL1: (6, 6, 5), SKEL_TRIMASTL2: (8, 5, 5), SKEL_TRIMASTL3: (12, 4, 5), SKEL_TRIMASTL4: (16, 3, 5), SKEL_TRIMASTL5: (20, 2, 5), SKEL_FOREMASTL1: (8, 4, 5), SKEL_FOREMASTL2: (12, 3, 5), SKEL_FOREMASTL3: (16, 2, 5), SKEL_AFTMASTL1: (14, 4, 5), SKEL_AFTMASTL2: (24, 3, 5), SKEL_AFTMASTL3: (30, 2, 5), INTERCEPTORL1: (5, 4, [4, 4, 4, 4, 4, 4, 4]), INTERCEPTORL2: (8, 3, [8, 8, 8, 8, 8, 8, 8]), INTERCEPTORL3: (11, 3, [25, 25, 25, 25, 25, 25, 25]), INTERCEPTORL4: (14, 2, [35, 35, 35, 35, 35, 35, 35]), MERCHANTL1: (9, 4, [20, 20, 20, 10, 10, 15, 15]), MERCHANTL2: (12, 3, [30, 30, 30, 20, 20, 25, 25]), MERCHANTL3: (15, 3, [35, 35, 35, 25, 25, 30, 30]), MERCHANTL4: (18, 2, [40, 40, 40, 30, 30, 35, 35]), WARSHIPL1: (7, 3, [15, 15, 15, 15, 15, 25, 25, 20, 20]), WARSHIPL2: (10, 3, [15, 25, 25, 25, 25, 35, 35, 30, 30]), WARSHIPL3: (14, 3, [30, 30, 30, 30, 30, 40, 40, 35, 35]), WARSHIPL4: (18, 2, [40, 40, 40, 40, 40, 50, 50, 45, 45]), BLACK_PEARL: (14, 3, [30, 30, 30, 30, 30, 40, 40, 35, 35]), GOLIATH: (14, 3, [30, 30, 30, 30, 30, 40, 40, 35, 35]), SKEL_INTERCEPTORL3: (11, 3, [25, 25, 25, 25, 25, 25, 25]), SKEL_WARSHIPL3: (14, 3, [30, 30, 30, 30, 30, 40, 40, 35, 35])}

def getHoleSizes(itemClass):
    return __holeSizes.get(itemClass)


__boardingRopeHeight = {DINGHY: 1.0, WARSHIPL1: 0.6, WARSHIPL2: 0.8, WARSHIPL3: 1.0, WARSHIPL4: 1.0, MERCHANTL1: 0.6, MERCHANTL2: 0.8, MERCHANTL3: 1.0, MERCHANTL4: 1.0, INTERCEPTORL1: 0.5, INTERCEPTORL2: 0.7, INTERCEPTORL3: 1.0, INTERCEPTORL4: 1.0, BLACK_PEARL: 1.0, GOLIATH: 1.0, SKEL_WARSHIPL3: 1.0, SKEL_INTERCEPTORL3: 0.8}

def getBoardingRopeH(shipClass):
    return __boardingRopeHeight.get(shipClass)


__mastStats = {MAINMASTL1: {'maxHp': 400, 'maxArrayHp': [600], 'mass': 0}, MAINMASTL2: {'maxHp': 600, 'maxArrayHp': [800, 400], 'mass': 0}, MAINMASTL3: {'maxHp': 1000, 'maxArrayHp': [1200, 800, 400], 'mass': 0}, MAINMASTL4: {'maxHp': 1000, 'maxArrayHp': [1800, 1200, 600], 'mass': 0}, MAINMASTL5: {'maxHp': 1000, 'maxArrayHp': [2400, 1600, 800], 'mass': 0}, TRIMASTL1: {'maxHp': 600, 'maxArrayHp': [600, 200, 50], 'mass': 0}, TRIMASTL2: {'maxHp': 600, 'maxArrayHp': [900, 500, 50], 'mass': 0}, TRIMASTL3: {'maxHp': 600, 'maxArrayHp': [1200, 800, 50], 'mass': 0}, TRIMASTL4: {'maxHp': 600, 'maxArrayHp': [1800, 1200, 50], 'mass': 0}, TRIMASTL5: {'maxHp': 600, 'maxArrayHp': [2400, 1600, 50], 'mass': 0}, FOREMASTL1: {'maxHp': 200, 'maxArrayHp': [500], 'mass': 0}, FOREMASTL2: {'maxHp': 400, 'maxArrayHp': [1000], 'mass': 0}, FOREMASTL3: {'maxHp': 600, 'maxArrayHp': [2000], 'mass': 0}, AFTMASTL1: {'maxHp': 200, 'maxArrayHp': [500], 'mass': 0}, AFTMASTL2: {'maxHp': 400, 'maxArrayHp': [1000], 'mass': 0}, AFTMASTL3: {'maxHp': 600, 'maxArrayHp': [2000], 'mass': 0}, SKEL_MAINMASTL1_A: {'maxHp': 600, 'maxArrayHp': [800, 400], 'mass': 0}, SKEL_MAINMASTL2_A: {'maxHp': 800, 'maxArrayHp': [1200, 800, 400], 'mass': 0}, SKEL_MAINMASTL3_A: {'maxHp': 1200, 'maxArrayHp': [1600, 1200, 600, 200], 'mass': 0}, SKEL_MAINMASTL4_A: {}, SKEL_MAINMASTL5_A: {}, SKEL_MAINMASTL1_B: {'maxHp': 600, 'maxArrayHp': [800, 400], 'mass': 0}, SKEL_MAINMASTL2_B: {'maxHp': 800, 'maxArrayHp': [1200, 800, 400], 'mass': 0}, SKEL_MAINMASTL3_B: {'maxHp': 1200, 'maxArrayHp': [1600, 1200, 600, 200], 'mass': 0}, SKEL_MAINMASTL4_B: {}, SKEL_MAINMASTL5_B: {}, SKEL_TRIMASTL1: {}, SKEL_TRIMASTL2: {'maxHp': 600, 'maxArrayHp': [800, 400], 'mass': 0}, SKEL_TRIMASTL3: {}, SKEL_TRIMASTL4: {}, SKEL_TRIMASTL5: {}, SKEL_FOREMASTL1: {'maxHp': 200, 'maxArrayHp': [500], 'mass': 0}, SKEL_FOREMASTL2: {'maxHp': 400, 'maxArrayHp': [1000], 'mass': 0}, SKEL_FOREMASTL3: {'maxHp': 600, 'maxArrayHp': [2000], 'mass': 0}, SKEL_AFTMASTL1: {'maxHp': 200, 'maxArrayHp': [500], 'mass': 0}, SKEL_AFTMASTL2: {'maxHp': 400, 'maxArrayHp': [1000], 'mass': 0}, SKEL_AFTMASTL3: {'maxHp': 600, 'maxArrayHp': [2000], 'mass': 0}}

def getMastStats(mastId):
    mastInfo = __mastStats.get(mastId)
    return mastInfo


__sailStats = {MAINSAILL1: {'maxHp': 900, 'maxSp': 300, 'acceleration': 0.05 * defaultAcceleration, 'maxSpeed': 0.05 * defaultMaxSpeed, 'reverseAcceleration': 0.05 * defaultReverseAcceleration, 'maxReverseSpeed': 0.05 * defaultMaxReverseAcceleration, 'turn': 0.05 * defaultTurn, 'maxTurn': 0.05 * defaultMaxTurn, 'mass': 0}, FORESAILL1: {'maxHp': 600, 'maxSp': 200, 'acceleration': 0.05 * defaultAcceleration, 'maxSpeed': 0.05 * defaultMaxSpeed, 'reverseAcceleration': 0.05 * defaultReverseAcceleration, 'maxReverseSpeed': 0.05 * defaultMaxReverseAcceleration, 'turn': 0.05 * defaultTurn, 'maxTurn': 0.05 * defaultMaxTurn, 'mass': 0}, AFTSAILL1: {'maxHp': 600, 'maxSp': 200, 'acceleration': 0.05 * defaultAcceleration, 'maxSpeed': 0.05 * defaultMaxSpeed, 'reverseAcceleration': 0.05 * defaultReverseAcceleration, 'maxReverseSpeed': 0.05 * defaultMaxReverseAcceleration, 'turn': 0.05 * defaultTurn, 'maxTurn': 0.05 * defaultMaxTurn, 'mass': 0}, FLAG: {'maxHp': 100, 'maxSp': 0, 'acceleration': 0.05 * defaultAcceleration, 'maxSpeed': 0.05 * defaultMaxSpeed, 'reverseAcceleration': 0.05 * defaultReverseAcceleration, 'maxReverseSpeed': 0.05 * defaultMaxReverseAcceleration, 'turn': 0.05 * defaultTurn, 'maxTurn': 0.05 * defaultMaxTurn, 'mass': 0}}

def getSailStats(sailId):
    sailInfo = __sailStats.get(sailId)
    return sailInfo


__cabinStats = {WAR_CABINL1A: {'maxHp': 1600, 'mass': 0, 'maxCargo': 0}, WAR_CABINL2A: {'maxHp': 2400, 'mass': 0, 'maxCargo': 0}, WAR_CABINL3A: {'maxHp': 3200, 'mass': 0, 'maxCargo': 0}, MERCH_CABINL1A: {'maxHp': 3200, 'mass': 0, 'maxCargo': 0}, MERCH_CABINL2A: {'maxHp': 4000, 'mass': 0, 'maxCargo': 0}, MERCH_CABINL3A: {'maxHp': 4800, 'mass': 0, 'maxCargo': 0}, INT_CABINL1A: {'maxHp': 800, 'mass': 0, 'maxCargo': 0}, INT_CABINL2A: {'maxHp': 1600, 'mass': 0, 'maxCargo': 0}, INT_CABINL3A: {'maxHp': 2400, 'mass': 0, 'maxCargo': 0}, BLACK_PEARL_CABIN: {'maxHp': 4000, 'mass': 0, 'maxCargo': 0}, GOLIATH_CABIN: {'maxHp': 6000, 'mass': 0, 'maxCargo': 0}, SKEL_WAR_CABINL3A: {'maxHp': 3200, 'mass': 0, 'maxCargo': 0}}

def getCabinStats(cabinId):
    cabinInfo = __cabinStats.get(cabinId)
    return cabinInfo


__prowStats = {SKELETON: {'maxHp': 500, 'mass': 0, 'rammingPower': 50, 'buff': 1}, LADY: {'maxHp': 500, 'mass': 0, 'rammingPower': 0, 'buff': 1}, RAML3: {'maxHp': 500, 'mass': 0, 'rammingPower': 500, 'buff': 0}, SKEL_RAML3: {'maxHp': 500, 'mass': 0, 'rammingPower': 500, 'buff': 0}}

def getProwStats(prowId):
    prowInfo = __prowStats.get(prowId)
    return prowInfo


__decorStats = {1: {'maxHp': 50}, 2: {'maxHp': 50}, 3: {'maxHp': 50}, 50: {'maxHp': 50}, 51: {'maxHp': 50}, 200: {'maxHp': 50}, 201: {'maxHp': 50}, 202: {'maxHp': 50}}

def getDecorStats(decorId):
    decorInfo = __decorStats.get(decorId)
    return decorInfo


__baseShipConfigs = {DINGHY: {'setShipClass': DINGHY, 'setModelClass': DINGHY, 'setMastConfig1': 0, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': 0, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 0, 'setSailLogoIndex': 0, 'setForesailConfig': [], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [], 'setLeftBroadsideConfig': [], 'setRightBroadsideConfig': [], 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [], 'setFloorDecorConfig': [], 'setProwType': 0, 'setRamType': 0, 'setHullTextureIndex': [0], 'setHullColorIndex': [0], 'setHullHilightColorIndex': [0], 'setStripeTextureIndex': [0], 'setStripeColorIndex': [0], 'setStripeHilightColorIndex': [0], 'setPatternTextureIndex': [0], 'setPatternColorIndex': [0], 'setPatternHilightColorIndex': [0], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, WARSHIPL1: {'setShipClass': WARSHIPL1, 'setModelClass': WARSHIPL1, 'setMastConfig1': MAINMASTL1, 'setMastConfig2': MAINMASTL2, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL3] * 8, 'setLeftBroadsideConfig': [CANNONL2] * 5, 'setRightBroadsideConfig': [CANNONL2] * 5, 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [2, 2, 2, 2], 'setFloorDecorConfig': [3] * 20, 'setProwType': 0, 'setRamType': RAML3, 'setHullTextureIndex': [2, 101, 2], 'setHullColorIndex': [0, 0, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [1, 1, 1], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [1, 1], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': WAR_CABINL1A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, WARSHIPL2: {'setShipClass': WARSHIPL2, 'setModelClass': WARSHIPL2, 'setMastConfig1': MAINMASTL2, 'setMastConfig2': MAINMASTL2, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL3] * 10, 'setLeftBroadsideConfig': [CANNONL2] * 7, 'setRightBroadsideConfig': [CANNONL2] * 7, 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [], 'setFloorDecorConfig': [3] * 26, 'setProwType': 0, 'setRamType': RAML3, 'setHullTextureIndex': [2, 101, 2], 'setHullColorIndex': [0, 19, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [1, 1, 1], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [1, 1], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': WAR_CABINL2A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, WARSHIPL3: {'setShipClass': WARSHIPL3, 'setModelClass': WARSHIPL3, 'setMastConfig1': MAINMASTL3, 'setMastConfig2': MAINMASTL3, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [0, FORESAILL1, FORESAILL1], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL3] * 14, 'setLeftBroadsideConfig': [CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2, 0, CANNONL2, CANNONL2, CANNONL2, 0], 'setRightBroadsideConfig': [CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2, 0, CANNONL2, CANNONL2, CANNONL2, 0], 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [200, 200, 200, 200, 200, 202, 200, 200, 200, 200, 200, 202, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 202, 202, 202, 201, 201, 201, 201, 201, 201, 201, 201], 'setFloorDecorConfig': [3] * 26, 'setProwType': 0, 'setRamType': RAML3, 'setHullTextureIndex': [2, 101, 2], 'setHullColorIndex': [0, 19, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [1, 1, 1], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [1, 1], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': WAR_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, MERCHANTL1: {'setShipClass': MERCHANTL1, 'setModelClass': MERCHANTL1, 'setMastConfig1': MAINMASTL2, 'setMastConfig2': MAINMASTL1, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [0, 0, FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 4, 'setLeftBroadsideConfig': [CANNONL2] * 5, 'setRightBroadsideConfig': [CANNONL2] * 5, 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [2, 2, 2], 'setFloorDecorConfig': [3] * 14, 'setProwType': SKELETON, 'setRamType': 0, 'setHullTextureIndex': [2, 101, 2], 'setHullColorIndex': [0, 0, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [1, 1, 1], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [1], 'setPatternColorIndex': [0], 'setPatternHilightColorIndex': [0], 'setCabinType': MERCH_CABINL1A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, MERCHANTL2: {'setShipClass': MERCHANTL2, 'setModelClass': MERCHANTL2, 'setMastConfig1': MAINMASTL1, 'setMastConfig2': MAINMASTL2, 'setMastConfig3': MAINMASTL1, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1], 'setSailConfig3': [MAINSAILL1], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [0, 0, FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 8, 'setLeftBroadsideConfig': [CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2, 0, 0, CANNONL2, CANNONL2, CANNONL2, CANNONL2, 0], 'setRightBroadsideConfig': [CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2, 0, 0, CANNONL2, CANNONL2, CANNONL2, CANNONL2, 0], 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [2] * 5, 'setFloorDecorConfig': [3] * 14, 'setProwType': SKELETON, 'setRamType': 0, 'setHullTextureIndex': [2, 101, 2], 'setHullColorIndex': [0, 0, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [1, 1, 1], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [1], 'setPatternColorIndex': [0], 'setPatternHilightColorIndex': [0], 'setCabinType': MERCH_CABINL2A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, MERCHANTL3: {'setShipClass': MERCHANTL3, 'setModelClass': MERCHANTL3, 'setMastConfig1': MAINMASTL3, 'setMastConfig2': MAINMASTL3, 'setMastConfig3': MAINMASTL3, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [0, FORESAILL1, FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 10, 'setLeftBroadsideConfig': [CANNONL2] * 12, 'setRightBroadsideConfig': [CANNONL2] * 12, 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [2] * 5, 'setFloorDecorConfig': [3] * 14, 'setProwType': SKELETON, 'setRamType': 0, 'setHullTextureIndex': [2, 101, 2], 'setHullColorIndex': [0, 0, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [1, 1, 1], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [1], 'setPatternColorIndex': [0], 'setPatternHilightColorIndex': [0], 'setCabinType': MERCH_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, INTERCEPTORL1: {'setShipClass': INTERCEPTORL1, 'setModelClass': INTERCEPTORL1, 'setMastConfig1': TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL1, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 2, 'setLeftBroadsideConfig': [CANNONL2] * 3, 'setRightBroadsideConfig': [CANNONL2] * 3, 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [2, 2], 'setFloorDecorConfig': [3, 3, 3], 'setProwType': SKELETON, 'setRamType': 0, 'setHullTextureIndex': [255, 255], 'setHullColorIndex': [0, 0], 'setHullHilightColorIndex': [0, 0], 'setStripeTextureIndex': [1, 2, 1], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [1, 1], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, INTERCEPTORL2: {'setShipClass': INTERCEPTORL2, 'setModelClass': INTERCEPTORL2, 'setMastConfig1': TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL1, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 6, 'setLeftBroadsideConfig': [CANNONL1] * 5, 'setRightBroadsideConfig': [CANNONL1] * 5, 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [2, 2, 2, 2], 'setFloorDecorConfig': [3, 3, 3], 'setProwType': SKELETON, 'setRamType': 0, 'setHullTextureIndex': [255, 255], 'setHullColorIndex': [0, 0], 'setHullHilightColorIndex': [0, 0], 'setStripeTextureIndex': [1, 2, 1], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [1, 1], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, INTERCEPTORL3: {'setShipClass': INTERCEPTORL3, 'setModelClass': INTERCEPTORL3, 'setMastConfig1': TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL1, 'setAftmastConfig': AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [FORESAILL1], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 8, 'setLeftBroadsideConfig': [CANNONL1] * 7, 'setRightBroadsideConfig': [CANNONL1] * 7, 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [2, 2, 2, 2], 'setFloorDecorConfig': [3, 3, 3], 'setProwType': SKELETON, 'setRamType': 0, 'setHullTextureIndex': [255, 255], 'setHullColorIndex': [0, 0], 'setHullHilightColorIndex': [0, 0], 'setStripeTextureIndex': [1, 2, 1], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [1, 1], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, BLACK_PEARL: {'setShipClass': BLACK_PEARL, 'setModelClass': BLACK_PEARL, 'setMastConfig1': MAINMASTL3, 'setMastConfig2': MAINMASTL3, 'setMastConfig3': MAINMASTL3, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 200, 'setSailConfig1': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailTextureIndex': 202, 'setSailLogoIndex': 201, 'setForesailConfig': [FORESAILL1, 0, 0], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [BPCANNON] * 14, 'setLeftBroadsideConfig': [BPCANNON] * 9, 'setRightBroadsideConfig': [BPCANNON] * 9, 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [], 'setFloorDecorConfig': [], 'setProwType': 0, 'setRamType': 0, 'setHullTextureIndex': [], 'setHullColorIndex': [], 'setHullHilightColorIndex': [], 'setStripeTextureIndex': [], 'setStripeColorIndex': [], 'setStripeHilightColorIndex': [], 'setPatternTextureIndex': [], 'setPatternColorIndex': [], 'setPatternHilightColorIndex': [], 'setCabinType': BLACK_PEARL_CABIN, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, STUMPY_SHIP: {'setShipClass': INTERCEPTORL1, 'setModelClass': INTERCEPTORL1, 'setMastConfig1': TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL1, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [TUTORIAL_CANNON, 0], 'setLeftBroadsideConfig': [], 'setRightBroadsideConfig': [], 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [2, 2], 'setFloorDecorConfig': [3, 3, 3], 'setProwType': SKELETON, 'setRamType': 0, 'setHullTextureIndex': [2, 101], 'setHullColorIndex': [0, 0], 'setHullHilightColorIndex': [0, 0], 'setStripeTextureIndex': [1, 2, 1], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [1, 1], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, GOLIATH: {'setShipClass': GOLIATH, 'setModelClass': GOLIATH, 'setMastConfig1': MAINMASTL3, 'setMastConfig2': MAINMASTL3, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [0, FORESAILL1, FORESAILL1], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL3] * 14, 'setLeftBroadsideConfig': [CANNONL4] * 9, 'setRightBroadsideConfig': [CANNONL4] * 9, 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonFirebrand, 'setWallDecorConfig': [200, 200, 200, 200, 200, 202, 200, 200, 200, 200, 200, 202, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 202, 202, 202, 201, 201, 201, 201, 201, 201, 201, 201], 'setFloorDecorConfig': [0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3], 'setProwType': 0, 'setRamType': RAML3, 'setHullTextureIndex': [255, 253, 254], 'setHullColorIndex': [15, 15, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [200, 200, 200], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [200, 200], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': GOLIATH_CABIN, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, NAVY_PANTHER: {'setShipClass': NAVY_PANTHER, 'setModelClass': WARSHIPL1, 'setMastConfig1': MAINMASTL1, 'setMastConfig2': MAINMASTL2, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL3] * 6, 'setLeftBroadsideConfig': [CANNONL2] * 4, 'setRightBroadsideConfig': [CANNONL2] * 4, 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [2, 2, 2, 2], 'setFloorDecorConfig': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 'setProwType': 0, 'setRamType': RAML3, 'setHullTextureIndex': [253, 253, 255], 'setHullColorIndex': [15, 15, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [200, 200, 200], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [200, 200], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': WAR_CABINL1A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, NAVY_CENTURION: {'setShipClass': NAVY_CENTURION, 'setModelClass': WARSHIPL2, 'setMastConfig1': MAINMASTL2, 'setMastConfig2': MAINMASTL2, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL3] * 8, 'setLeftBroadsideConfig': [CANNONL2] * 6, 'setRightBroadsideConfig': [CANNONL2] * 6, 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [], 'setFloorDecorConfig': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0, 3, 3], 'setProwType': 0, 'setRamType': RAML3, 'setHullTextureIndex': [253, 253, 254], 'setHullColorIndex': [15, 15, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [200, 200, 200], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [200, 200], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': WAR_CABINL2A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, NAVY_MAN_O_WAR: {'setShipClass': NAVY_MAN_O_WAR, 'setModelClass': WARSHIPL3, 'setMastConfig1': MAINMASTL2, 'setMastConfig2': MAINMASTL3, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [0, FORESAILL1, 0], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL3] * 10, 'setLeftBroadsideConfig': [CANNONL2] * 8, 'setRightBroadsideConfig': [CANNONL2] * 8, 'setBroadsideAmmo': InventoryType.CannonFirebrand, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [200, 200, 200, 200, 200, 202, 200, 200, 200, 200, 200, 202, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 202, 202, 202, 201, 201, 201, 201, 201, 201, 201, 201], 'setFloorDecorConfig': [0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3], 'setProwType': 0, 'setRamType': RAML3, 'setHullTextureIndex': [253, 253, 254], 'setHullColorIndex': [15, 15, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [200, 200, 200], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [200, 200], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': WAR_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, NAVY_DREADNOUGHT: {'setShipClass': NAVY_DREADNOUGHT, 'setModelClass': WARSHIPL3, 'setMastConfig1': MAINMASTL3, 'setMastConfig2': MAINMASTL3, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [0, FORESAILL1, FORESAILL1], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL3] * 14, 'setLeftBroadsideConfig': [CANNONL4] * 9, 'setRightBroadsideConfig': [CANNONL4] * 9, 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonFirebrand, 'setWallDecorConfig': [200, 200, 200, 200, 200, 202, 200, 200, 200, 200, 200, 202, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 202, 202, 202, 201, 201, 201, 201, 201, 201, 201, 201], 'setFloorDecorConfig': [0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3], 'setProwType': 0, 'setRamType': RAML3, 'setHullTextureIndex': [255, 253, 254], 'setHullColorIndex': [15, 15, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [200, 200, 200], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [200, 200], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': WAR_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, NAVY_BULWARK: {'setShipClass': NAVY_BULWARK, 'setModelClass': MERCHANTL1, 'setMastConfig1': MAINMASTL2, 'setMastConfig2': MAINMASTL1, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [0, 0, FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 4, 'setLeftBroadsideConfig': [0, CANNONL2, CANNONL2, CANNONL2, 0], 'setRightBroadsideConfig': [0, CANNONL2, CANNONL2, CANNONL2, 0], 'setBroadsideAmmo': InventoryType.CannonChainShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [2, 2, 2], 'setFloorDecorConfig': [3, 3, 3, 3, 3, 3], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [253, 254, 253], 'setHullColorIndex': [15, 0, 15], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [200, 201, 202], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [200], 'setPatternColorIndex': [0], 'setPatternHilightColorIndex': [0], 'setCabinType': MERCH_CABINL1A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, NAVY_VANGUARD: {'setShipClass': NAVY_VANGUARD, 'setModelClass': MERCHANTL2, 'setMastConfig1': MAINMASTL1, 'setMastConfig2': MAINMASTL2, 'setMastConfig3': MAINMASTL1, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1], 'setSailConfig3': [MAINSAILL1], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [0, 0, FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 6, 'setLeftBroadsideConfig': [CANNONL3] * 5, 'setRightBroadsideConfig': [CANNONL3] * 5, 'setBroadsideAmmo': InventoryType.CannonChainShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [], 'setFloorDecorConfig': [3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [253, 254, 253], 'setHullColorIndex': [15, 0, 15], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [200, 201, 202], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [200], 'setPatternColorIndex': [0], 'setPatternHilightColorIndex': [0], 'setCabinType': MERCH_CABINL2A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, NAVY_MONARCH: {'setShipClass': NAVY_MONARCH, 'setModelClass': MERCHANTL3, 'setMastConfig1': MAINMASTL2, 'setMastConfig2': MAINMASTL2, 'setMastConfig3': MAINMASTL2, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1], 'setSailConfig3': [MAINSAILL1, MAINSAILL1], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [0, 0, FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 8, 'setLeftBroadsideConfig': [0, CANNONL2, CANNONL2, CANNONL2, CANNONL2, 0, 0, 0, CANNONL2, CANNONL2, CANNONL2, 0], 'setRightBroadsideConfig': [0, CANNONL2, CANNONL2, CANNONL2, CANNONL2, 0, 0, 0, CANNONL2, CANNONL2, CANNONL2, 0], 'setBroadsideAmmo': InventoryType.CannonChainShot, 'setCannonAmmo': InventoryType.CannonFirebrand, 'setWallDecorConfig': [], 'setFloorDecorConfig': [3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [253, 254, 254], 'setHullColorIndex': [15, 0, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [200, 201, 202], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [200], 'setPatternColorIndex': [0], 'setPatternHilightColorIndex': [0], 'setCabinType': MERCH_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, NAVY_COLOSSUS: {'setShipClass': NAVY_COLOSSUS, 'setModelClass': MERCHANTL3, 'setMastConfig1': MAINMASTL3, 'setMastConfig2': MAINMASTL3, 'setMastConfig3': MAINMASTL3, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [0, FORESAILL1, FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 10, 'setLeftBroadsideConfig': [CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2, 0, CANNONL2, CANNONL2, CANNONL2, CANNONL2, 0], 'setRightBroadsideConfig': [CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2, 0, CANNONL2, CANNONL2, CANNONL2, CANNONL2, 0], 'setBroadsideAmmo': InventoryType.CannonChainShot, 'setCannonAmmo': InventoryType.CannonFirebrand, 'setWallDecorConfig': [], 'setFloorDecorConfig': [3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [255, 254, 254], 'setHullColorIndex': [15, 0, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [200, 201, 202], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [200], 'setPatternColorIndex': [0], 'setPatternHilightColorIndex': [0], 'setCabinType': MERCH_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, NAVY_FERRET: {'setShipClass': NAVY_FERRET, 'setModelClass': INTERCEPTORL1, 'setMastConfig1': TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL1, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 2, 'setLeftBroadsideConfig': [], 'setRightBroadsideConfig': [], 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [2, 2], 'setFloorDecorConfig': [3, 3, 3], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [253, 254], 'setHullColorIndex': [15, 0], 'setHullHilightColorIndex': [0, 0], 'setStripeTextureIndex': [200, 201, 202], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [200, 200], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, NAVY_GREYHOUND: {'setShipClass': NAVY_GREYHOUND, 'setModelClass': INTERCEPTORL2, 'setMastConfig1': TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL1, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 4, 'setLeftBroadsideConfig': [CANNONL1] * 3, 'setRightBroadsideConfig': [CANNONL1] * 3, 'setBroadsideAmmo': InventoryType.CannonChainShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [2, 2, 2, 2], 'setFloorDecorConfig': [3, 3, 3], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [253, 254], 'setHullColorIndex': [15, 0], 'setHullHilightColorIndex': [0, 0], 'setStripeTextureIndex': [200, 201, 202], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [200, 200], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, NAVY_KINGFISHER: {'setShipClass': NAVY_KINGFISHER, 'setModelClass': INTERCEPTORL3, 'setMastConfig1': TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL1, 'setAftmastConfig': AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [FORESAILL1], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 6, 'setLeftBroadsideConfig': [CANNONL1] * 5, 'setRightBroadsideConfig': [CANNONL1] * 5, 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonFirebrand, 'setWallDecorConfig': [2, 2, 2, 2], 'setFloorDecorConfig': [3, 3, 3], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [253, 254], 'setHullColorIndex': [15, 0], 'setHullHilightColorIndex': [0, 0], 'setStripeTextureIndex': [200, 201, 202], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [200, 200], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, NAVY_PREDATOR: {'setShipClass': NAVY_PREDATOR, 'setModelClass': INTERCEPTORL3, 'setMastConfig1': TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL1, 'setAftmastConfig': AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 0, 'setForesailConfig': [FORESAILL1], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 8, 'setLeftBroadsideConfig': [CANNONL1] * 7, 'setRightBroadsideConfig': [CANNONL1] * 7, 'setBroadsideAmmo': InventoryType.CannonFirebrand, 'setCannonAmmo': InventoryType.CannonFirebrand, 'setWallDecorConfig': [2, 2, 2, 2], 'setFloorDecorConfig': [3, 3, 3], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [255, 255], 'setHullColorIndex': [15, 0], 'setHullHilightColorIndex': [0, 0], 'setStripeTextureIndex': [200, 201, 202], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [200, 200], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, EITC_CORVETTE: {'setShipClass': EITC_CORVETTE, 'setModelClass': WARSHIPL1, 'setMastConfig1': MAINMASTL1, 'setMastConfig2': MAINMASTL2, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 202, 'setForesailConfig': [], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL3] * 6, 'setLeftBroadsideConfig': [CANNONL2] * 5, 'setRightBroadsideConfig': [CANNONL2] * 5, 'setBroadsideAmmo': InventoryType.CannonChainShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [2, 2, 2, 2], 'setFloorDecorConfig': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 'setProwType': 0, 'setRamType': RAML3, 'setHullTextureIndex': [253, 253, 250], 'setHullColorIndex': [17, 18, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [204, 204, 205], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [208, 208], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': WAR_CABINL1A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, EITC_MARAUDER: {'setShipClass': EITC_MARAUDER, 'setModelClass': WARSHIPL2, 'setMastConfig1': MAINMASTL2, 'setMastConfig2': MAINMASTL2, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 202, 'setForesailConfig': [], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL3] * 8, 'setLeftBroadsideConfig': [CANNONL2] * 7, 'setRightBroadsideConfig': [CANNONL2] * 7, 'setBroadsideAmmo': InventoryType.CannonFirebrand, 'setCannonAmmo': InventoryType.CannonChainShot, 'setWallDecorConfig': [], 'setFloorDecorConfig': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0, 3, 3], 'setProwType': 0, 'setRamType': RAML3, 'setHullTextureIndex': [253, 253, 250], 'setHullColorIndex': [17, 18, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [204, 204, 205], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [208, 208], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': WAR_CABINL2A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, EITC_WARLORD: {'setShipClass': EITC_WARLORD, 'setModelClass': WARSHIPL3, 'setMastConfig1': MAINMASTL2, 'setMastConfig2': MAINMASTL3, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 202, 'setForesailConfig': [0, FORESAILL1, 0], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL3] * 12, 'setLeftBroadsideConfig': [CANNONL2] * 9, 'setRightBroadsideConfig': [CANNONL2] * 9, 'setBroadsideAmmo': InventoryType.CannonFirebrand, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [200, 200, 200, 200, 200, 202, 200, 200, 200, 200, 200, 202, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 202, 202, 202, 201, 201, 201, 201, 201, 201, 201, 201], 'setFloorDecorConfig': [0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3], 'setProwType': 0, 'setRamType': RAML3, 'setHullTextureIndex': [253, 253, 250], 'setHullColorIndex': [17, 18, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [204, 204, 205], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [208, 208], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': WAR_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, EITC_JUGGERNAUT: {'setShipClass': EITC_JUGGERNAUT, 'setModelClass': WARSHIPL3, 'setMastConfig1': MAINMASTL3, 'setMastConfig2': MAINMASTL3, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 202, 'setForesailConfig': [0, FORESAILL1, FORESAILL1], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL3] * 14, 'setLeftBroadsideConfig': [CANNONL2] * 10, 'setRightBroadsideConfig': [CANNONL2] * 10, 'setBroadsideAmmo': InventoryType.CannonExplosive, 'setCannonAmmo': InventoryType.CannonFirebrand, 'setWallDecorConfig': [200, 200, 200, 200, 200, 202, 200, 200, 200, 200, 200, 202, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 202, 202, 202, 201, 201, 201, 201, 201, 201, 201, 201], 'setFloorDecorConfig': [0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3], 'setProwType': 0, 'setRamType': RAML3, 'setHullTextureIndex': [253, 253, 250], 'setHullColorIndex': [17, 18, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [204, 204, 205], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [208, 208], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': WAR_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, EITC_SENTINEL: {'setShipClass': EITC_SENTINEL, 'setModelClass': MERCHANTL1, 'setMastConfig1': MAINMASTL2, 'setMastConfig2': MAINMASTL1, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 202, 'setForesailConfig': [0, 0, FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 4, 'setLeftBroadsideConfig': [CANNONL2] * 5, 'setRightBroadsideConfig': [CANNONL2] * 5, 'setBroadsideAmmo': InventoryType.CannonFirebrand, 'setCannonAmmo': InventoryType.CannonChainShot, 'setWallDecorConfig': [2, 2, 2], 'setFloorDecorConfig': [3, 3, 3, 3, 3, 3], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [253, 250, 253], 'setHullColorIndex': [17, 0, 17], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [204, 204, 205], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [208], 'setPatternColorIndex': [0], 'setPatternHilightColorIndex': [0], 'setCabinType': MERCH_CABINL1A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, EITC_IRONWALL: {'setShipClass': EITC_IRONWALL, 'setModelClass': MERCHANTL2, 'setMastConfig1': MAINMASTL1, 'setMastConfig2': MAINMASTL2, 'setMastConfig3': MAINMASTL1, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1], 'setSailConfig3': [MAINSAILL1], 'setSailTextureIndex': 1, 'setSailLogoIndex': 202, 'setForesailConfig': [0, 0, FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 6, 'setLeftBroadsideConfig': [CANNONL3] * 7, 'setRightBroadsideConfig': [CANNONL3] * 7, 'setBroadsideAmmo': InventoryType.CannonRoundShot, 'setCannonAmmo': InventoryType.CannonFirebrand, 'setWallDecorConfig': [], 'setFloorDecorConfig': [3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [253, 250, 253], 'setHullColorIndex': [17, 0, 17], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [204, 204, 205], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [208], 'setPatternColorIndex': [0], 'setPatternHilightColorIndex': [0], 'setCabinType': MERCH_CABINL2A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, EITC_OGRE: {'setShipClass': EITC_OGRE, 'setModelClass': MERCHANTL3, 'setMastConfig1': MAINMASTL2, 'setMastConfig2': MAINMASTL2, 'setMastConfig3': MAINMASTL2, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1], 'setSailConfig3': [MAINSAILL1, MAINSAILL1], 'setSailTextureIndex': 1, 'setSailLogoIndex': 202, 'setForesailConfig': [0, 0, FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 8, 'setLeftBroadsideConfig': [CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2, 0, 0, CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2], 'setRightBroadsideConfig': [CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2, 0, 0, CANNONL2, CANNONL2, CANNONL2, CANNONL2, CANNONL2], 'setBroadsideAmmo': InventoryType.CannonFirebrand, 'setCannonAmmo': InventoryType.CannonFirebrand, 'setWallDecorConfig': [], 'setFloorDecorConfig': [3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [253, 250, 250], 'setHullColorIndex': [17, 0, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [204, 204, 205], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [208], 'setPatternColorIndex': [0], 'setPatternHilightColorIndex': [0], 'setCabinType': MERCH_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, EITC_BEHEMOTH: {'setShipClass': EITC_BEHEMOTH, 'setModelClass': MERCHANTL3, 'setMastConfig1': MAINMASTL3, 'setMastConfig2': MAINMASTL3, 'setMastConfig3': MAINMASTL3, 'setForemastConfig': FOREMASTL2, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailTextureIndex': 1, 'setSailLogoIndex': 202, 'setForesailConfig': [0, FORESAILL1, FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 10, 'setLeftBroadsideConfig': [CANNONL2] * 12, 'setRightBroadsideConfig': [CANNONL2] * 12, 'setBroadsideAmmo': InventoryType.CannonFirebrand, 'setCannonAmmo': InventoryType.CannonExplosive, 'setWallDecorConfig': [], 'setFloorDecorConfig': [3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [253, 250, 250], 'setHullColorIndex': [17, 0, 0], 'setHullHilightColorIndex': [0, 0, 0], 'setStripeTextureIndex': [204, 204, 205], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [208], 'setPatternColorIndex': [0], 'setPatternHilightColorIndex': [0], 'setCabinType': MERCH_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, EITC_SEA_VIPER: {'setShipClass': EITC_SEA_VIPER, 'setModelClass': INTERCEPTORL1, 'setMastConfig1': TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL1, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 202, 'setForesailConfig': [FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 2, 'setLeftBroadsideConfig': [CANNONL1] * 3, 'setRightBroadsideConfig': [CANNONL1] * 3, 'setBroadsideAmmo': InventoryType.CannonChainShot, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [2, 2], 'setFloorDecorConfig': [3, 3, 3], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [253, 255], 'setHullColorIndex': [17, 0], 'setHullHilightColorIndex': [0, 0], 'setStripeTextureIndex': [204, 204, 205], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [208, 208], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, EITC_BLOODHOUND: {'setShipClass': EITC_BLOODHOUND, 'setModelClass': INTERCEPTORL2, 'setMastConfig1': TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL1, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 202, 'setForesailConfig': [FORESAILL1], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 6, 'setLeftBroadsideConfig': [CANNONL1] * 5, 'setRightBroadsideConfig': [CANNONL1] * 5, 'setBroadsideAmmo': InventoryType.CannonFirebrand, 'setCannonAmmo': InventoryType.CannonChainShot, 'setWallDecorConfig': [2, 2, 2, 2], 'setFloorDecorConfig': [3, 3, 3], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [255, 255], 'setHullColorIndex': [17, 0], 'setHullHilightColorIndex': [0, 0], 'setStripeTextureIndex': [204, 204, 205], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [208, 208], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, EITC_BARRACUDA: {'setShipClass': EITC_BARRACUDA, 'setModelClass': INTERCEPTORL3, 'setMastConfig1': TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL1, 'setAftmastConfig': AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 202, 'setForesailConfig': [FORESAILL1], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 6, 'setLeftBroadsideConfig': [CANNONL1] * 7, 'setRightBroadsideConfig': [CANNONL1] * 7, 'setBroadsideAmmo': InventoryType.CannonFirebrand, 'setCannonAmmo': InventoryType.CannonChainShot, 'setWallDecorConfig': [2, 2, 2, 2], 'setFloorDecorConfig': [3, 3, 3], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [253, 255], 'setHullColorIndex': [17, 0], 'setHullHilightColorIndex': [0, 0], 'setStripeTextureIndex': [204, 204, 205], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [208, 208], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, EITC_CORSAIR: {'setShipClass': EITC_CORSAIR, 'setModelClass': INTERCEPTORL3, 'setMastConfig1': TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': FOREMASTL1, 'setAftmastConfig': AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 1, 'setSailLogoIndex': 202, 'setForesailConfig': [FORESAILL1], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [CANNONL1] * 8, 'setLeftBroadsideConfig': [CANNONL1] * 7, 'setRightBroadsideConfig': [CANNONL1] * 7, 'setBroadsideAmmo': InventoryType.CannonExplosive, 'setCannonAmmo': InventoryType.CannonFirebrand, 'setWallDecorConfig': [2, 2, 2, 2], 'setFloorDecorConfig': [3, 3, 3], 'setProwType': LADY, 'setRamType': 0, 'setHullTextureIndex': [255, 255], 'setHullColorIndex': [17, 0], 'setHullHilightColorIndex': [0, 0], 'setStripeTextureIndex': [204, 204, 205], 'setStripeColorIndex': [0, 0, 0], 'setStripeHilightColorIndex': [0, 0, 0], 'setPatternTextureIndex': [208, 208], 'setPatternColorIndex': [0, 0], 'setPatternHilightColorIndex': [0, 0], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, SKEL_PHANTOM: {'setShipClass': SKEL_PHANTOM, 'setModelClass': SKEL_WARSHIPL3, 'setMastConfig1': SKEL_MAINMASTL3_A, 'setMastConfig2': SKEL_MAINMASTL3_B, 'setMastConfig3': 0, 'setForemastConfig': SKEL_FOREMASTL2, 'setAftmastConfig': SKEL_AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 0, 'setSailLogoIndex': 0, 'setForesailConfig': [FORESAILL1, FORESAILL1], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [SKEL_CANNON_L3] * 6, 'setLeftBroadsideConfig': [0, SKEL_CANNON_L2, SKEL_CANNON_L2, SKEL_CANNON_L2, SKEL_CANNON_L2, SKEL_CANNON_L2, 0], 'setRightBroadsideConfig': [0, SKEL_CANNON_L2, SKEL_CANNON_L2, SKEL_CANNON_L2, SKEL_CANNON_L2, SKEL_CANNON_L2, 0], 'setBroadsideAmmo': InventoryType.CannonThunderbolt, 'setCannonAmmo': InventoryType.CannonChainShot, 'setWallDecorConfig': [], 'setFloorDecorConfig': [], 'setProwType': 0, 'setRamType': SKEL_RAML3, 'setHullTextureIndex': [], 'setHullColorIndex': [], 'setHullHilightColorIndex': [], 'setStripeTextureIndex': [], 'setStripeColorIndex': [], 'setStripeHilightColorIndex': [], 'setPatternTextureIndex': [], 'setPatternColorIndex': [], 'setPatternHilightColorIndex': [], 'setCabinType': SKEL_WAR_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, SKEL_REVENANT: {'setShipClass': SKEL_REVENANT, 'setModelClass': SKEL_WARSHIPL3, 'setMastConfig1': SKEL_MAINMASTL3_A, 'setMastConfig2': SKEL_MAINMASTL3_B, 'setMastConfig3': 0, 'setForemastConfig': SKEL_FOREMASTL2, 'setAftmastConfig': SKEL_AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 0, 'setSailLogoIndex': 0, 'setForesailConfig': [FORESAILL1, FORESAILL1], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [SKEL_CANNON_L3] * 6, 'setLeftBroadsideConfig': [SKEL_CANNON_L2] * 6, 'setRightBroadsideConfig': [SKEL_CANNON_L2] * 6, 'setBroadsideAmmo': InventoryType.CannonFury, 'setCannonAmmo': InventoryType.CannonRoundShot, 'setWallDecorConfig': [], 'setFloorDecorConfig': [], 'setProwType': 0, 'setRamType': SKEL_RAML3, 'setHullTextureIndex': [], 'setHullColorIndex': [], 'setHullHilightColorIndex': [], 'setStripeTextureIndex': [], 'setStripeColorIndex': [], 'setStripeHilightColorIndex': [], 'setPatternTextureIndex': [], 'setPatternColorIndex': [], 'setPatternHilightColorIndex': [], 'setCabinType': SKEL_WAR_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, SKEL_STORM_REAPER: {'setShipClass': SKEL_STORM_REAPER, 'setModelClass': SKEL_WARSHIPL3, 'setMastConfig1': SKEL_MAINMASTL3_A, 'setMastConfig2': SKEL_MAINMASTL3_B, 'setMastConfig3': 0, 'setForemastConfig': SKEL_FOREMASTL2, 'setAftmastConfig': SKEL_AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 0, 'setSailLogoIndex': 0, 'setForesailConfig': [FORESAILL1, FORESAILL1], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [SKEL_CANNON_L3] * 6, 'setLeftBroadsideConfig': [SKEL_CANNON_L2] * 7, 'setRightBroadsideConfig': [SKEL_CANNON_L2] * 7, 'setBroadsideAmmo': InventoryType.CannonThunderbolt, 'setCannonAmmo': InventoryType.CannonThunderbolt, 'setWallDecorConfig': [], 'setFloorDecorConfig': [], 'setProwType': 0, 'setRamType': SKEL_RAML3, 'setHullTextureIndex': [], 'setHullColorIndex': [], 'setHullHilightColorIndex': [], 'setStripeTextureIndex': [], 'setStripeColorIndex': [], 'setStripeHilightColorIndex': [], 'setPatternTextureIndex': [], 'setPatternColorIndex': [], 'setPatternHilightColorIndex': [], 'setCabinType': SKEL_WAR_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, SKEL_BLACK_HARBINGER: {'setShipClass': SKEL_BLACK_HARBINGER, 'setModelClass': SKEL_WARSHIPL3, 'setMastConfig1': SKEL_MAINMASTL3_A, 'setMastConfig2': SKEL_MAINMASTL3_B, 'setMastConfig3': 0, 'setForemastConfig': SKEL_FOREMASTL2, 'setAftmastConfig': SKEL_AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 0, 'setSailLogoIndex': 0, 'setForesailConfig': [FORESAILL1, FORESAILL1], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [SKEL_CANNON_L3] * 6, 'setLeftBroadsideConfig': [SKEL_CANNON_L2] * 7, 'setRightBroadsideConfig': [SKEL_CANNON_L2] * 7, 'setBroadsideAmmo': InventoryType.CannonFury, 'setCannonAmmo': InventoryType.CannonFury, 'setWallDecorConfig': [], 'setFloorDecorConfig': [], 'setProwType': 0, 'setRamType': SKEL_RAML3, 'setHullTextureIndex': [], 'setHullColorIndex': [], 'setHullHilightColorIndex': [], 'setStripeTextureIndex': [], 'setStripeColorIndex': [], 'setStripeHilightColorIndex': [], 'setPatternTextureIndex': [], 'setPatternColorIndex': [], 'setPatternHilightColorIndex': [], 'setCabinType': SKEL_WAR_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, SKEL_DEATH_OMEN: {'setShipClass': SKEL_DEATH_OMEN, 'setModelClass': SKEL_WARSHIPL3, 'setMastConfig1': SKEL_MAINMASTL3_A, 'setMastConfig2': SKEL_MAINMASTL3_B, 'setMastConfig3': 0, 'setForemastConfig': SKEL_FOREMASTL2, 'setAftmastConfig': SKEL_AFTMASTL2, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig2': [MAINSAILL1, MAINSAILL1, MAINSAILL1], 'setSailConfig3': [], 'setSailTextureIndex': 0, 'setSailLogoIndex': 0, 'setForesailConfig': [FORESAILL1, FORESAILL1], 'setAftsailConfig': [AFTSAILL1], 'setPanelArmorConfig': [], 'setCannonConfig': [SKEL_CANNON_L3] * 6, 'setLeftBroadsideConfig': [SKEL_CANNON_L2] * 7, 'setRightBroadsideConfig': [SKEL_CANNON_L2] * 7, 'setBroadsideAmmo': InventoryType.CannonFury, 'setCannonAmmo': InventoryType.CannonThunderbolt, 'setWallDecorConfig': [], 'setFloorDecorConfig': [], 'setProwType': 0, 'setRamType': SKEL_RAML3, 'setHullTextureIndex': [], 'setHullColorIndex': [], 'setHullHilightColorIndex': [], 'setStripeTextureIndex': [], 'setStripeColorIndex': [], 'setStripeHilightColorIndex': [], 'setPatternTextureIndex': [], 'setPatternColorIndex': [], 'setPatternHilightColorIndex': [], 'setCabinType': SKEL_WAR_CABINL3A, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, SKEL_SHADOW_CROW_FR: {'setShipClass': SKEL_SHADOW_CROW_FR, 'setModelClass': SKEL_INTERCEPTORL3, 'setMastConfig1': SKEL_TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': 0, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 0, 'setSailLogoIndex': 0, 'setForesailConfig': [], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [SKEL_CANNON_L3] * 5, 'setLeftBroadsideConfig': [SKEL_CANNON_L2] * 5, 'setRightBroadsideConfig': [SKEL_CANNON_L2] * 5, 'setBroadsideAmmo': InventoryType.CannonChainShot, 'setCannonAmmo': InventoryType.CannonFury, 'setWallDecorConfig': [], 'setFloorDecorConfig': [], 'setProwType': 0, 'setRamType': 0, 'setHullTextureIndex': [], 'setHullColorIndex': [], 'setHullHilightColorIndex': [], 'setStripeTextureIndex': [], 'setStripeColorIndex': [], 'setStripeHilightColorIndex': [], 'setPatternTextureIndex': [], 'setPatternColorIndex': [], 'setPatternHilightColorIndex': [], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, SKEL_HELLHOUND_FR: {'setShipClass': SKEL_HELLHOUND_FR, 'setModelClass': SKEL_INTERCEPTORL3, 'setMastConfig1': SKEL_TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': 0, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 0, 'setSailLogoIndex': 0, 'setForesailConfig': [], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [SKEL_CANNON_L3] * 5, 'setLeftBroadsideConfig': [SKEL_CANNON_L2] * 5, 'setRightBroadsideConfig': [SKEL_CANNON_L2] * 5, 'setBroadsideAmmo': InventoryType.CannonExplosive, 'setCannonAmmo': InventoryType.CannonFirebrand, 'setWallDecorConfig': [], 'setFloorDecorConfig': [], 'setProwType': 0, 'setRamType': 0, 'setHullTextureIndex': [], 'setHullColorIndex': [], 'setHullHilightColorIndex': [], 'setStripeTextureIndex': [], 'setStripeColorIndex': [], 'setStripeHilightColorIndex': [], 'setPatternTextureIndex': [], 'setPatternColorIndex': [], 'setPatternHilightColorIndex': [], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, SKEL_BLOOD_SCOURGE_FR: {'setShipClass': SKEL_BLOOD_SCOURGE_FR, 'setModelClass': SKEL_INTERCEPTORL3, 'setMastConfig1': SKEL_TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': 0, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 0, 'setSailLogoIndex': 0, 'setForesailConfig': [], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [SKEL_CANNON_L3] * 5, 'setLeftBroadsideConfig': [SKEL_CANNON_L2] * 5, 'setRightBroadsideConfig': [SKEL_CANNON_L2] * 5, 'setBroadsideAmmo': InventoryType.CannonFirebrand, 'setCannonAmmo': InventoryType.CannonThunderbolt, 'setWallDecorConfig': [], 'setFloorDecorConfig': [], 'setProwType': 0, 'setRamType': 0, 'setHullTextureIndex': [], 'setHullColorIndex': [], 'setHullHilightColorIndex': [], 'setStripeTextureIndex': [], 'setStripeColorIndex': [], 'setStripeHilightColorIndex': [], 'setPatternTextureIndex': [], 'setPatternColorIndex': [], 'setPatternHilightColorIndex': [], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, SKEL_SHADOW_CROW_SP: {'setShipClass': SKEL_SHADOW_CROW_SP, 'setModelClass': SKEL_INTERCEPTORL3, 'setMastConfig1': SKEL_TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': 0, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 0, 'setSailLogoIndex': 0, 'setForesailConfig': [], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [SKEL_CANNON_L3] * 5, 'setLeftBroadsideConfig': [SKEL_CANNON_L2] * 5, 'setRightBroadsideConfig': [SKEL_CANNON_L2] * 5, 'setBroadsideAmmo': InventoryType.CannonChainShot, 'setCannonAmmo': InventoryType.CannonFury, 'setWallDecorConfig': [], 'setFloorDecorConfig': [], 'setProwType': 0, 'setRamType': 0, 'setHullTextureIndex': [], 'setHullColorIndex': [], 'setHullHilightColorIndex': [], 'setStripeTextureIndex': [], 'setStripeColorIndex': [], 'setStripeHilightColorIndex': [], 'setPatternTextureIndex': [], 'setPatternColorIndex': [], 'setPatternHilightColorIndex': [], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, SKEL_HELLHOUND_SP: {'setShipClass': SKEL_HELLHOUND_SP, 'setModelClass': SKEL_INTERCEPTORL3, 'setMastConfig1': SKEL_TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': 0, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 0, 'setSailLogoIndex': 0, 'setForesailConfig': [], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [SKEL_CANNON_L3] * 5, 'setLeftBroadsideConfig': [SKEL_CANNON_L2] * 5, 'setRightBroadsideConfig': [SKEL_CANNON_L2] * 5, 'setBroadsideAmmo': InventoryType.CannonExplosive, 'setCannonAmmo': InventoryType.CannonFirebrand, 'setWallDecorConfig': [], 'setFloorDecorConfig': [], 'setProwType': 0, 'setRamType': 0, 'setHullTextureIndex': [], 'setHullColorIndex': [], 'setHullHilightColorIndex': [], 'setStripeTextureIndex': [], 'setStripeColorIndex': [], 'setStripeHilightColorIndex': [], 'setPatternTextureIndex': [], 'setPatternColorIndex': [], 'setPatternHilightColorIndex': [], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}, SKEL_BLOOD_SCOURGE_SP: {'setShipClass': SKEL_BLOOD_SCOURGE_SP, 'setModelClass': SKEL_INTERCEPTORL3, 'setMastConfig1': SKEL_TRIMASTL2, 'setMastConfig2': 0, 'setMastConfig3': 0, 'setForemastConfig': 0, 'setAftmastConfig': 0, 'setMastTextureIndex': 0, 'setSailConfig1': [MAINSAILL1, MAINSAILL1], 'setSailConfig2': [], 'setSailConfig3': [], 'setSailTextureIndex': 0, 'setSailLogoIndex': 0, 'setForesailConfig': [], 'setAftsailConfig': [], 'setPanelArmorConfig': [], 'setCannonConfig': [SKEL_CANNON_L3] * 5, 'setLeftBroadsideConfig': [SKEL_CANNON_L2] * 5, 'setRightBroadsideConfig': [SKEL_CANNON_L2] * 5, 'setBroadsideAmmo': InventoryType.CannonFirebrand, 'setCannonAmmo': InventoryType.CannonThunderbolt, 'setWallDecorConfig': [], 'setFloorDecorConfig': [], 'setProwType': 0, 'setRamType': 0, 'setHullTextureIndex': [], 'setHullColorIndex': [], 'setHullHilightColorIndex': [], 'setStripeTextureIndex': [], 'setStripeColorIndex': [], 'setStripeHilightColorIndex': [], 'setPatternTextureIndex': [], 'setPatternColorIndex': [], 'setPatternHilightColorIndex': [], 'setCabinType': 0, 'setCabinMastConfig': [], 'setCabinSailConfig': [], 'setCabinCannonConfig': [], 'setCabinWallDecorConfig': [], 'setCabinFloorDecorConfig': [], 'setCabinWindowConfig': []}}

def getBaseShipConfig(hullId):
    hullInfo = __baseShipConfigs.get(hullId)
    return hullInfo


def getMastInfo(hullId):
    hullInfo = getBaseShipConfig(hullId)
    mastNames = ['setMastConfig1', 'setMastConfig2', 'setMastConfig3', 'setForemastConfig', 'setAftmastConfig']
    sailNames = [
     'setSailConfig1', 'setSailConfig2', 'setSailConfig3', 'setForesailConfig', 'setAftsailConfig']
    mastInfo = []
    for x, (mastName, sailName) in enumerate(zip(mastNames, sailNames)):
        mastType = hullInfo[mastName]
        if mastType:
            sailTypes = hullInfo[sailName]
            mastInfo.append((mastType, x, sailTypes))

    return mastInfo


__shipAttributes = [
 'setShipClass']
__hullAttributes = [
 'setShipClass', 'setCannonConfig', 'setLeftBroadsideConfig', 'setRightBroadsideConfig', 'setBroadsideAmmo', 'setWallDecorConfig', 'setFloorDecorConfig', 'setProwType', 'setRamType', 'setHullTextureIndex', 'setHullColorIndex', 'setHullHilightColorIndex', 'setStripeTextureIndex', 'setStripeColorIndex', 'setStripeHilightColorIndex', 'setPatternTextureIndex', 'setPatternColorIndex', 'setPatternHilightColorIndex']
__cabinAttributes = [
 'setShipClass', 'setCabinType', 'setCannonConfig', 'setWallDecorConfig', 'setFloorDecorConfig', 'setWindowConfig', 'setHullTextureIndex', 'setHullColorIndex', 'setHullHilightColorIndex', 'setStripeTextureIndex', 'setStripeColorIndex', 'setStripeHilightColorIndex', 'setPatternTextureIndex', 'setPatternColorIndex', 'setPatternHilightColorIndex']
__mastAttributes = {0: ['setShipClass', 'setMastConfig1', 'setSailConfig1', 'setMastTextureIndex'], 1: ['setShipClass', 'setMastConfig2', 'setSailConfig2', 'setMastTextureIndex'], 2: ['setShipClass', 'setMastConfig3', 'setSailConfig3', 'setMastTextureIndex'], 3: ['setShipClass', 'setForemastConfig', 'setForesailConfig', 'setMastTextureIndex'], 4: ['setShipClass', 'setAftmastConfig', 'setAftsailConfig', 'setMastTextureIndex']}
__sailAttributes = {0: ['setMastConfig1', 'setSailConfig1', 'setSailTextureIndex', 'setSailLogoIndex'], 1: ['setMastConfig2', 'setSailConfig2', 'setSailTextureIndex', 'setSailLogoIndex'], 2: ['setMastConfig3', 'setSailConfig3', 'setSailTextureIndex', 'setSailLogoIndex'], 3: ['setForemastConfig', 'setForesailConfig', 'setSailTextureIndex', 'setSailLogoIndex'], 4: ['setAftmastConfig', 'setAftsailConfig', 'setSailTextureIndex', 'setSailLogoIndex']}
__prowAttributes = [
 'setProwType']
__ramAttributes = [
 'setRamType']
__wallDecorAttributes = [
 'setWallDecorConfig']
__floorDecorAttributes = ['setFloorDecorConfig']
__shipDNAdata = [
 'setShipClass', 'setOwnerId']
__hullDNAdata = [
 'setShipClass', 'setCannonConfig', 'setLeftBroadsideConfig', 'setRightBroadsideConfig', 'setBroadsideAmmo', 'setWallDecorConfig', 'setFloorDecorConfig', 'setProwType', 'setRamType', 'setHullTextureIndex', 'setHullColorIndex', 'setHullHilightColorIndex', 'setStripeTextureIndex', 'setStripeColorIndex', 'setStripeHilightColorIndex', 'setPatternTextureIndex', 'setPatternColorIndex', 'setPatternHilightColorIndex']
__cabinDNAdata = [
 'setShipClass', 'setCabinType', 'setCannonConfig', 'setWallDecorConfig', 'setFloorDecorConfig', 'setWindowConfig', 'setHullTextureIndex', 'setHullColorIndex', 'setHullHilightColorIndex', 'setStripeTextureIndex', 'setStripeColorIndex', 'setStripeHilightColorIndex', 'setPatternTextureIndex', 'setPatternColorIndex', 'setPatternHilightColorIndex']
__mastDNAdata = [
 'setShipClass', 'setMastType', 'setSailConfig', 'setTextureIndex', 'setPosIndex']
__sailDNAdata = [
 'setMastType', 'setSailType', 'setTextureIndex', 'setLogoIndex', 'setPosIndex']
__prowDNAdata = [
 'setProwType', 'setOwnerId']
__decorDNAdata = [
 'setDecorType', 'setPosIndex', 'setOwnerId']

def getModelClass(shipClass):
    shipData = getBaseShipConfig(shipClass)
    if shipData:
        return shipData['setModelClass']
    return 0


def getShipConfigAll(shipClass):
    shipData = getBaseShipConfig(shipClass)
    return shipData


def getShipConfig(shipClass):
    shipData = getBaseShipConfig(shipClass)
    if shipData is None:
        return
    newData = {}
    for i in range(len(__shipAttributes)):
        if __shipAttributes[i] in shipData:
            newData[__shipDNAdata[i]] = shipData[__shipAttributes[i]]

    partStats = getHullStats(shipClass)
    newData['setMaxHp'] = partStats['maxHp']
    newData['setHp'] = partStats['maxHp']
    newData['setMaxCrew'] = partStats['maxCrew']
    for i in newData:
        newData[i] = [
         newData[i]]

    return newData


def getHullConfig(shipClass):
    shipData = getBaseShipConfig(shipClass)
    newData = {}
    for i in range(len(__hullAttributes)):
        if __hullAttributes[i] in shipData:
            newData[__hullDNAdata[i]] = shipData[__hullAttributes[i]]

    partStats = getHullStats(shipClass)
    newData['setMaxArrayHp'] = partStats['maxArrayHp']
    newData['setArrayHp'] = partStats['maxArrayHp']
    newData['setMaxCargo'] = partStats['maxCargo']
    newData['setMaxSp'] = partStats['maxSp']
    newData['setSp'] = partStats['maxSp']
    for i in newData:
        newData[i] = [
         newData[i]]

    return newData


def getCabinConfig(shipClass):
    shipData = getBaseShipConfig(shipClass)
    newData = {}
    for i in range(len(__cabinAttributes)):
        if __cabinAttributes[i] in shipData:
            newData[__cabinDNAdata[i]] = shipData[__cabinAttributes[i]]

    partStats = getCabinStats(newData['setCabinType'])
    newData['setMaxHp'] = partStats['maxHp']
    newData['setHp'] = partStats['maxHp']
    newData['setMaxCargo'] = partStats['maxCargo']
    for i in newData:
        newData[i] = [
         newData[i]]

    return newData


def getMastConfig(shipClass, index):
    shipData = getBaseShipConfig(shipClass)
    mastAttrib = __mastAttributes.get(index)
    newData = {}
    for i in range(len(mastAttrib)):
        if mastAttrib[i] in shipData:
            newData[__mastDNAdata[i]] = shipData[mastAttrib[i]]

    newData['setPosIndex'] = index
    partStats = getMastStats(newData['setMastType'])
    newData['setMaxArrayHp'] = partStats['maxArrayHp']
    newData['setArrayHp'] = partStats['maxArrayHp']
    for i in newData:
        newData[i] = [
         newData[i]]

    return newData


def getSailConfig(shipClass, mastIndex, sailIndex):
    shipData = getBaseShipConfig(shipClass)
    sailAttrib = __sailAttributes.get(mastIndex)
    newData = {}
    for i in range(len(sailAttrib)):
        if sailAttrib[i] in shipData:
            if __sailDNAdata[i] == 'setSailType':
                newData[__sailDNAdata[i]] = shipData[sailAttrib[i]][sailIndex]
            else:
                newData[__sailDNAdata[i]] = shipData[sailAttrib[i]]

    newData['setMastPosIndex'] = mastIndex
    newData['setPosIndex'] = sailIndex
    partStats = getSailStats(newData['setSailType'])
    newData['setMaxHp'] = partStats['maxHp']
    newData['setHp'] = partStats['maxHp']
    newData['setMaxSp'] = partStats['maxSp']
    newData['setSp'] = partStats['maxSp']
    for i in newData:
        newData[i] = [
         newData[i]]

    return newData


def getProwConfig(shipClass):
    shipData = getBaseShipConfig(shipClass)
    newData = {}
    for i in range(len(__prowAttributes)):
        if __prowAttributes[i] in shipData:
            newData[__prowDNAdata[i]] = shipData[__prowAttributes[i]]

    partStats = getProwStats(newData['setProwType'])
    newData['setMaxHp'] = partStats['maxHp']
    newData['setHp'] = partStats['maxHp']
    for i in newData:
        newData[i] = [
         newData[i]]

    return newData


def getRamConfig(shipClass):
    shipData = getBaseShipConfig(shipClass)
    newData = {}
    for i in range(len(__ramAttributes)):
        if __ramAttributes[i] in shipData:
            newData[__prowDNAdata[i]] = shipData[__ramAttributes[i]]

    partStats = getProwStats(newData['setProwType'])
    newData['setMaxHp'] = partStats['maxHp']
    newData['setHp'] = partStats['maxHp']
    for i in newData:
        newData[i] = [
         newData[i]]

    return newData


def getDecorConfig(shipClass, placement, decorIndex):
    shipData = getBaseShipConfig(shipClass)
    if placement == 'wall':
        decorAttrib = __wallDecorAttributes
    else:
        decorAttrib = __floorDecorAttributes
    newData = {}
    for i in range(len(decorAttrib)):
        if decorAttrib[i] in shipData:
            if __decorDNAdata[i] == 'setDecorType':
                newData[__decorDNAdata[i]] = shipData[decorAttrib[i]][decorIndex]
            else:
                newData[__decorDNAdata[i]] = shipData[decorAttrib[i]]

    newData['setPosIndex'] = decorIndex
    partStats = getDecorStats(newData['setDecorType'])
    newData['setMaxHp'] = partStats['maxHp']
    newData['setHp'] = partStats['maxHp']
    for i in newData:
        newData[i] = [
         newData[i]]

    return newData


__shipRepairCostMultiplier = {DINGHY: 1.0, INTERCEPTORL1: 0.15, MERCHANTL1: 0.2, WARSHIPL1: 0.25, INTERCEPTORL2: 0.15, MERCHANTL2: 0.2, WARSHIPL2: 0.25, INTERCEPTORL3: 0.15, MERCHANTL3: 0.2, WARSHIPL3: 0.25, INTERCEPTORL4: 0.15, MERCHANTL4: 0.2, WARSHIPL4: 0.25, GOLIATH: 0.25, BLACK_PEARL: 0.25, SKEL_WARSHIPL3: 0.25, SKEL_INTERCEPTORL3: 0.25}

def getRepairCostMult(modelClass):
    return __shipRepairCostMultiplier.get(modelClass)


def getRepairCost(ship, hull=None, cabin=None, masts=[], sails=[], prow=None, ram=None):
    return calcRepairCost(ship.maxHp, ship.Hp, ship.maxSp, ship.Sp, ship.modelClass)


def calcRepairCost(maxHp, Hp, maxSp, Sp, modelClass):
    totalCost = 0
    totalCost += maxHp - Hp + (maxSp - Sp) / 2
    if Hp <= 0:
        totalCost = totalCost * SUNK_REPAIR_COST_MULTIPLIER
    mult = getRepairCostMult(modelClass)
    if mult:
        totalCost *= mult
    totalCost = totalCost / 100.0
    return int(math.ceil(totalCost))


INVALID_TEAM = -1
PLAYER_TEAM = 0
UNDEAD_TEAM = 1
NAVY_TEAM = 2
TRADING_CO_TEAM = 3
FRENCH_UNDEAD_TEAM = 7
SPANISH_UNDEAD_TEAM = 8
LEVEL_INDEX = 0
TEAM_INDEX = 1
ENABLED_INDEX = 2
shipData = {NAVY_FERRET: [2, NAVY_TEAM, 1], NAVY_BULWARK: [6, NAVY_TEAM, 1], NAVY_PANTHER: [9, NAVY_TEAM, 1], NAVY_GREYHOUND: [12, NAVY_TEAM, 1], NAVY_VANGUARD: [16, NAVY_TEAM, 1], NAVY_CENTURION: [19, NAVY_TEAM, 1], NAVY_KINGFISHER: [22, NAVY_TEAM, 1], NAVY_MONARCH: [26, NAVY_TEAM, 1], NAVY_MAN_O_WAR: [29, NAVY_TEAM, 1], NAVY_PREDATOR: [32, NAVY_TEAM, 1], NAVY_COLOSSUS: [36, NAVY_TEAM, 1], NAVY_DREADNOUGHT: [39, NAVY_TEAM, 1], GOLIATH: [40, NAVY_TEAM, 1], BLACK_PEARL: [30, PLAYER_TEAM, 1], EITC_SEA_VIPER: [7, TRADING_CO_TEAM, 1], EITC_SENTINEL: [11, TRADING_CO_TEAM, 1], EITC_CORVETTE: [14, TRADING_CO_TEAM, 1], EITC_BLOODHOUND: [17, TRADING_CO_TEAM, 1], EITC_IRONWALL: [21, TRADING_CO_TEAM, 1], EITC_MARAUDER: [24, TRADING_CO_TEAM, 1], EITC_BARRACUDA: [27, TRADING_CO_TEAM, 1], EITC_OGRE: [31, TRADING_CO_TEAM, 1], EITC_WARLORD: [34, TRADING_CO_TEAM, 1], EITC_CORSAIR: [37, TRADING_CO_TEAM, 1], EITC_BEHEMOTH: [41, TRADING_CO_TEAM, 1], EITC_JUGGERNAUT: [44, TRADING_CO_TEAM, 1], SKEL_PHANTOM: [18, UNDEAD_TEAM, 1], SKEL_REVENANT: [26, UNDEAD_TEAM, 1], SKEL_STORM_REAPER: [31, UNDEAD_TEAM, 1], SKEL_BLACK_HARBINGER: [36, UNDEAD_TEAM, 1], SKEL_DEATH_OMEN: [42, UNDEAD_TEAM, 1], SKEL_SHADOW_CROW_FR: [18, FRENCH_UNDEAD_TEAM, 1], SKEL_HELLHOUND_FR: [21, FRENCH_UNDEAD_TEAM, 1], SKEL_BLOOD_SCOURGE_FR: [28, FRENCH_UNDEAD_TEAM, 1], SKEL_SHADOW_CROW_SP: [18, SPANISH_UNDEAD_TEAM, 1], SKEL_HELLHOUND_SP: [21, SPANISH_UNDEAD_TEAM, 1], SKEL_BLOOD_SCOURGE_SP: [28, SPANISH_UNDEAD_TEAM, 1]}

def getRandomShipLevel(shipClass):
    baselevel = getShipLevel(shipClass) - 1
    baselevel += random.randint(0, 2)
    baselevel = min(len(list(__shipLevelStatMultiplier.keys())) - 1, baselevel)
    return baselevel


def getShipLevel(shipClass):
    if shipClass in shipData:
        return shipData[shipClass][LEVEL_INDEX]
    else:
        return 2


def getShipTeam(shipClass):
    if shipClass in shipData:
        return shipData[shipClass][TEAM_INDEX]
    else:
        return PLAYER_TEAM


shipGeoms = {}

def preprocessHull(name):
    geom = loader.loadModel('models/shipparts/%s-geometry_High' % name)
    geom.flattenStrong()
    allPanels = geom.findAllMatches('**/panel_High_*')
    for panel in allPanels:
        for mn in panel.findAllMatches('**/+ModelNode'):
            if mn.getNumChildren() < 2:
                if mn.getNumChildren() > 0:
                    gn = mn.find('+GeomNode')
                    if gn.isEmpty():
                        gn = mn.getChild(0)

                    gn.setName(mn.getName())
                    gn.reparentTo(mn.getParent())
                    mn.detachNode()

        panel.reparentTo(geom)
        panel.stash()

    for mn in geom.findAllMatches('**/+ModelNode'):
        if mn.getNumChildren() < 2:
            if mn.getNumChildren() > 0:
                gn = mn.find('+GeomNode')
                if gn.isEmpty():
                    gn = mn.getChild(0)

                gn.setName(mn.getName())
                gn.reparentTo(mn.getParent())
                mn.detachNode()

    geomStatic = NodePath('static')
    geom.getChild(0).reparentTo(geomStatic)
    for panel in allPanels:
        panel.unstash()

    highGeom = geom.copyTo(hidden)
    highGeom.detachNode()
    highPanels = highGeom.findAllMatches('**/panel_High_*')
    flashPanelsHigh = []
    for panel in highPanels:
        panel.reparentTo(highGeom)

    medGeom = geom.copyTo(hidden)
    medGeom.detachNode()
    medPanels = medGeom.findAllMatches('**/panel_High_*')
    flashPanelsMed = []
    projections = []
    for panel in medPanels:
        ps = ProjectionScreen()
        ps.setTexcoordName('uvHole')
        psnp = medGeom.attachNewNode(ps)
        panel.reparentTo(psnp)

    lowGeom = geom.copyTo(hidden)
    lowGeom.detachNode()
    geomStatic.copyTo(lowGeom)
    shipGeoms['models/shipparts/%s-geometry_High' % name] = [
     highGeom, geomStatic]
    shipGeoms['models/shipparts/%s-geometry_Medium' % name] = [medGeom, geomStatic]
    shipGeoms['models/shipparts/%s-geometry_Low' % name] = [lowGeom]


def preprocessHullMed(name):
    geom = loader.loadModel('models/shipparts/%s-geometry_Med' % name)
    geom.flattenStrong()
    allPanels = geom.findAllMatches('**/panel_High_*')
    for panel in allPanels:
        for mn in panel.findAllMatches('**/+ModelNode'):
            if mn.getNumChildren() < 2:
                if mn.getNumChildren() > 0:
                    gn = mn.find('+GeomNode')
                    if gn.isEmpty():
                        gn = mn.getChild(0)

                    gn.setName(mn.getName())
                    gn.reparentTo(mn.getParent())
                    mn.detachNode()

        panel.reparentTo(geom)
        panel.stash()

    for mn in geom.findAllMatches('**/+ModelNode'):
        if mn.getNumChildren() < 2:
            if mn.getNumChildren() > 0:
                gn = mn.find('+GeomNode')
                if gn.isEmpty():
                    gn = mn.getChild(0)

                gn.setName(mn.getName())
                gn.reparentTo(mn.getParent())
                mn.detachNode()

    geomStatic = NodePath('static')
    geom.getChild(0).reparentTo(geomStatic)
    for panel in allPanels:
        panel.unstash()

    mediumGeom = geom.copyTo(hidden)
    mediumGeom.detachNode()
    medPanels = mediumGeom.findAllMatches('**/panel_High_*')
    flashPanelsMed = []
    projections = []
    for panel in medPanels:
        ps = ProjectionScreen()
        ps.setTexcoordName('uvHole')
        psnp = mediumGeom.attachNewNode(ps)
        panel.reparentTo(psnp)

    shipGeoms['models/shipparts/%s-geometry_Medium' % name] = [mediumGeom, geomStatic]


def preprocessHullLow(name, inFix='', isSkelShip=False):
    geom = loader.loadModel('models/shipparts/%s-geometry_Low' % name)
    geom.flattenStrong()
    for mn in geom.findAllMatches('**/+ModelNode'):
        if mn.getNumChildren() < 2:
            if mn.getNumChildren() > 0:
                gn = mn.find('+GeomNode')
                if gn.isEmpty():
                    gn = mn.getChild(0)

                gn.setName(mn.getName())
                gn.reparentTo(mn.getParent())
                mn.detachNode()

    geom.findAllMatches('**/+ModelNode').reparentTo(geom)
    lowGeom = geom.copyTo(hidden)
    lowGeom.detachNode()
    if isSkelShip:
        shipGeoms['models/shipparts/%s%s-geometry_Low' % (name, inFix)] = [
         lowGeom]
    else:
        shipGeoms['models/shipparts/%s%sL1-geometry_Low' % (name, inFix)] = [
         lowGeom]
        shipGeoms['models/shipparts/%s%sL2-geometry_Low' % (name, inFix)] = [lowGeom]
        shipGeoms['models/shipparts/%s%sL3-geometry_Low' % (name, inFix)] = [lowGeom]


def preprocessHulls():
    preprocessHull('warshipL1')
    preprocessHullMed('warshipL1')
    preprocessHull('warshipL2')
    preprocessHullMed('warshipL2')
    preprocessHull('warshipL3')
    preprocessHullMed('warshipL3')
    preprocessHullLow('warship')
    preprocessHull('warCabinAL1')
    preprocessHullMed('warCabinAL1')
    preprocessHull('warCabinAL2')
    preprocessHullMed('warCabinAL2')
    preprocessHull('warCabinAL3')
    preprocessHullMed('warCabinAL3')
    preprocessHullLow('warCabin', inFix='A')
    preprocessHull('skeletonWarshipL3')
    preprocessHullMed('skeletonWarshipL3')
    preprocessHullLow('skeletonWarshipL3', isSkelShip=True)
    preprocessHull('skeletonWarCabinAL3')
    preprocessHullMed('skeletonWarCabinAL3')
    preprocessHullLow('skeletonWarCabinAL3', inFix='', isSkelShip=True)
    preprocessHull('merchantL1')
    preprocessHullMed('merchantL1')
    preprocessHull('merchantL2')
    preprocessHullMed('merchantL2')
    preprocessHull('merchantL3')
    preprocessHullMed('merchantL3')
    preprocessHullLow('merchant')
    preprocessHull('merchantCabinAL1')
    preprocessHullMed('merchantCabinAL1')
    preprocessHull('merchantCabinAL2')
    preprocessHullMed('merchantCabinAL2')
    preprocessHull('merchantCabinAL3')
    preprocessHullMed('merchantCabinAL3')
    preprocessHullLow('merchantCabin', inFix='A')
    preprocessHull('interceptorL1')
    preprocessHullMed('interceptorL1')
    preprocessHull('interceptorL2')
    preprocessHullMed('interceptorL2')
    preprocessHull('interceptorL3')
    preprocessHullMed('interceptorL3')
    preprocessHullLow('interceptor')


def preprocessPhase5Ships(task=0):
    preprocessHull('skeletonInterceptorL3')
    preprocessHullMed('skeletonInterceptorL3')
    preprocessHullLow('skeletonInterceptorL3', isSkelShip=True)
    for i in range(5):
        preprocessMast('models/char/mainmastA_tri_ghost', 2, i)

    return Task.done


def preprocessBlackPearl(task=0):
    preprocessHull('blackpearl')
    preprocessHull('blackpearlCabin')
    return Task.done


def preprocessGoliath(task=0):
    preprocessHull('goliath')
    preprocessHull('goliathCabinA')
    return Task.done


def preprocessCannon(name):
    cannon = Actor.Actor()
    cannon.setLODNode()
    cannon.addLOD('hi', 100, 0)
    cannon.addLOD('med', 200, 100)
    cannon.addLOD('low', 400, 200)
    cannon.loadModel('%s%s' % (name, '_hi'), lodName='hi')
    cannon.loadModel('%s%s' % (name, '_med'), lodName='med')
    cannon.loadModel('%s%s' % (name, '_low'), lodName='low')
    cannon.loadAnims({'zero': '%s%s' % (name, '_zero')}, lodName='all')
    cannon.findAllMatches('**/+ModelNode').detach()
    shipGeoms[name] = cannon


BroadsideAnimDict = (
 (
  'zero', '_zero'), ('Fire', '_fire'), ('Open', '_open'), ('Close', '_close'))

def preprocessBroadside(name):
    anims = {}
    for anim in BroadsideAnimDict:
        anims[anim[0]] = name + anim[1]

    cannon = Actor.Actor()
    cannon.setLODNode()
    cannon.addLOD('hi', 100, 0)
    cannon.addLOD('med', 200, 100)
    cannon.addLOD('low', 400, 200)
    cannon.loadModel('%s%s' % (name, '_hi'), lodName='hi')
    cannon.loadModel('%s%s' % (name, '_med'), lodName='med')
    cannon.loadModel('%s%s' % (name, '_low'), lodName='low')
    cannon.loadAnims(anims, lodName='all')
    cannon.findAllMatches('**/+ModelNode').detach()
    shipGeoms[name] = cannon


def preprocessIntroCannon():
    preprocessCannon('models/shipparts/cannon')


def preprocessCannons():
    preprocessCannon('models/shipparts/GP_cannon')
    preprocessCannon('models/shipparts/cannon_bp')
    preprocessBroadside('models/shipparts/cannon_port')
    preprocessBroadside('models/shipparts/GP_cannonPort')
    preprocessBroadside('models/shipparts/cannon_bp_port')


def preprocessSprit(name):
    sprit = Actor.Actor()
    sprit.setLODNode()
    sprit.addLOD('low', 5000, 1400)
    sprit.addLOD('medium', 1400, 400)
    sprit.addLOD('high', 400, 0)
    sprit.loadModel(name, 'modelRoot', 'high')
    sprit.loadModel(name, 'modelRoot', 'medium')
    sprit.findAllMatches('**/+ModelNode').detach()
    shipGeoms[name] = sprit


def preprocessSprits():
    preprocessSprit('models/shipparts/prow_skeleton_zero')
    preprocessSprit('models/shipparts/prow_female_zero')
    preprocessSprit('models/shipparts/ram_spike_zero')
    preprocessSprit('models/shipparts/skel_ram_spike_zero')


def preprocessMast(name, maxHeight, index):
    mast = Actor.Actor()
    mast.setLODNode()
    mast.addLOD('high', 100, 0)
    mast.addLOD('medium', 200, 100)
    mast.addLOD('low', 1000, 200)
    animNames = ['break0A', 'break1A', 'break2A', 'break3A'][:maxHeight]
    anims = {}
    for animName in animNames:
        anims[animName] = '%s_%s_new' % (name, animName)

    anims['Idle'] = '%s_idle_new' % name
    anims['Hidden'] = '%s_hidden_new' % name
    mast.loadModel('%s_h' % name, 'modelRoot', 'high')
    mast.loadModel('%s_m' % name, 'modelRoot', 'medium')
    mast.loadModel('%s_l' % name, 'modelRoot', 'low')
    mast.loadAnims(anims, 'modelRoot', 'all')
    riggingAttrib = CullBinAttrib.make('ShipRigging', 0)
    geomNodeList = mast.findAllMatches('**/+GeomNode')
    for i in range(geomNodeList.getNumPaths()):
        gn = geomNodeList[i].node()
        for j in range(gn.getNumGeoms()):
            geomState = gn.getGeomState(j)
            texAttrib = geomState.getAttrib(TextureAttrib.getClassType())
            for k in range(texAttrib.getNumOnStages()):
                stage = texAttrib.getOnStage(k)
                tex = texAttrib.getOnTexture(stage)
                if tex.getName() == 'ab_ship_rigging_alpha':
                    gn.setGeomState(j, geomState.addAttrib(riggingAttrib))
                    continue

    for j in range(maxHeight):
        excludedJoint = [
         'def_sail_%d_a_1' % j, 'def_sail_%d_b_1' % j, 'def_sail_%d_c_1' % j]
        if j < maxHeight - 1:
            excludedJoint.append('def_mast_%d' % (j + 1))
        else:
            excludedJoint = []
        mast.makeSubpart('mast_%d_%d' % (j, index), ['def_mast_' + str(j)], excludedJoint)

    mast.setSubpartsComplete(True)
    mast.findAllMatches('**/+ModelNode').detach()
    locators = loader.loadModel('%s_zero_locators' % name)
    tallestMast = Actor.Actor()
    tallestMast.copyActor(mast, 1)
    shipGeoms['%s_%s_%s' % (name, maxHeight, index)] = [tallestMast, locators]
    for i in range(1, maxHeight):
        height = maxHeight - i
        if height < 3:
            mast.freezeJoint('mast_%d_%d' % (height, index), 'def_mast_%s' % height, scale=Vec3(0.001, 0.001, 0.001))
        newMast = Actor.Actor()
        newMast.copyActor(mast, 1)
        shipGeoms['%s_%s_%s' % (name, height, index)] = [newMast, locators]


def preprocessRigging(name, indices):
    for i in indices:
        rig = loader.loadModel('%s_%s' % (name, i))
        rig.flattenStrong()
        rigNodePath = NodePath('rigging')
        rigNodePath.setBin('ShipRigging', 0)
        rig.findAllMatches('**/+GeomNode').reparentTo(rigNodePath)
        shipGeoms['%s_%s' % (name, i)] = rigNodePath


def preprocessMasts():
    for i in range(5):
        preprocessMast('models/char/mainmast_square', 3, i)
        preprocessMast('models/char/mainmast_tri', 3, i)
        preprocessMast('models/char/foremast_tri', 1, i)
        preprocessMast('models/char/foremast_multi', 1, i)
        preprocessMast('models/char/aftmast_tri', 1, i)
        preprocessMast('models/char/mainmastA_ghost', 4, i)
        preprocessMast('models/char/mainmastB_ghost', 4, i)
        preprocessMast('models/char/aftmastA_ghost', 2, i)
        preprocessMast('models/char/foremastA_ghost', 1, i)

    preprocessRigging('models/char/interceptorL1-rigging', [0])
    preprocessRigging('models/char/interceptorL2-rigging', [0])
    preprocessRigging('models/char/interceptorL3-rigging', [0])
    preprocessRigging('models/char/merchantL1-rigging', [0, 1])
    preprocessRigging('models/char/merchantL2-rigging', [0, 1, 2])
    preprocessRigging('models/char/merchantL3-rigging', [0, 1, 2])
    preprocessRigging('models/char/warshipL1-rigging', [0, 1])
    preprocessRigging('models/char/warshipL2-rigging', [0, 1])
    preprocessRigging('models/char/warshipL3-rigging', [0, 1])


def preprocessPhase3ShipParts():
    preprocessHulls()
    preprocessCannons()
    preprocessMasts()


def getShipGeom(filename):
    data = shipGeoms.get(filename)
    if data:
        return (1, data)
    else:
        return (
         0, loader.loadModel(filename))


def getActor(filename):
    cannon = shipGeoms.get(filename)
    if cannon:
        newCannon = Actor.Actor()
        newCannon.copyActor(cannon)
        return (
         1, newCannon)
    else:
        return (0, None)
    return


def getMast(filename):
    try:
        mast, locators = shipGeoms.get(filename)
    except:
        base.notify.error('Mast helper function from ShipGlobals encountered an error trying to load %s' % filename)

    newMast = Actor.Actor()
    newMast.copyActor(mast, 1)
    newLocators = locators.copyTo(hidden)
    newLocators.detachNode()
    return (
     newMast, newLocators)


def getRigging(filename):
    rig = shipGeoms.get(filename)
    if rig:
        rig = rig.copyTo(hidden)
        rig.detachNode()
        return rig
    else:
        return
    return


__enemyAIShipSpeed = {WARSHIPL1: ([50, 100, 115, 135], [10, 10]), WARSHIPL2: ([50, 100, 115, 135], [10, 10]), WARSHIPL3: ([50, 100, 115, 135], [10, 10]), WARSHIPL4: ([50, 100, 115, 135], [10, 10]), MERCHANTL1: ([45, 90, 105, 125], [6, 6]), MERCHANTL2: ([45, 90, 105, 125], [6, 6]), MERCHANTL3: ([45, 90, 105, 125], [6, 6]), MERCHANTL4: ([45, 90, 105, 125], [6, 6]), INTERCEPTORL1: ([55, 110, 125, 145], [16, 16]), INTERCEPTORL2: ([55, 110, 125, 145], [16, 16]), INTERCEPTORL3: ([55, 110, 125, 145], [16, 16]), INTERCEPTORL4: ([55, 110, 125, 145], [16, 16]), STUMPY_SHIP: ([8, 8, 8, 8], [6, 6]), BLACK_PEARL: ([50, 100, 150, 200], [14, 14]), GOLIATH: ([50, 100, 150, 200], [14, 14]), NAVY_PANTHER: ([25, 60, 105, 125], [7, 7]), NAVY_CENTURION: ([30, 65, 110, 130], [8, 8]), NAVY_MAN_O_WAR: ([35, 70, 115, 135], [9, 9]), NAVY_DREADNOUGHT: ([35, 70, 115, 135], [9, 9]), NAVY_BULWARK: ([20, 50, 95, 115], [5, 5]), NAVY_VANGUARD: ([25, 55, 100, 120], [6, 6]), NAVY_MONARCH: ([30, 60, 105, 125], [7, 7]), NAVY_COLOSSUS: ([30, 60, 105, 125], [7, 7]), NAVY_FERRET: ([30, 70, 115, 135], [10, 10]), NAVY_GREYHOUND: ([35, 75, 120, 140], [11, 11]), NAVY_KINGFISHER: ([40, 80, 125, 145], [12, 12]), NAVY_PREDATOR: ([40, 80, 125, 145], [12, 12]), EITC_CORVETTE: ([25, 60, 105, 125], [7, 7]), EITC_MARAUDER: ([30, 65, 110, 130], [8, 8]), EITC_WARLORD: ([35, 70, 115, 135], [9, 9]), EITC_JUGGERNAUT: ([35, 70, 115, 135], [9, 9]), EITC_SENTINEL: ([20, 50, 95, 115], [5, 5]), EITC_IRONWALL: ([25, 55, 100, 120], [6, 6]), EITC_OGRE: ([30, 60, 105, 125], [7, 7]), EITC_BEHEMOTH: ([30, 60, 105, 125], [7, 7]), EITC_SEA_VIPER: ([30, 70, 115, 135], [10, 10]), EITC_BLOODHOUND: ([35, 75, 120, 140], [11, 11]), EITC_BARRACUDA: ([40, 80, 125, 145], [12, 12]), EITC_CORSAIR: ([40, 80, 125, 145], [12, 12]), SKEL_PHANTOM: ([35, 70, 115, 135], [10, 10]), SKEL_REVENANT: ([35, 70, 115, 135], [11, 11]), SKEL_STORM_REAPER: ([40, 75, 120, 140], [11, 11]), SKEL_BLACK_HARBINGER: ([40, 75, 120, 140], [12, 12]), SKEL_DEATH_OMEN: ([45, 80, 125, 145], [12, 12]), SKEL_SHADOW_CROW_FR: ([40, 80, 125, 145], [12, 12]), SKEL_HELLHOUND_FR: ([40, 80, 125, 145], [13, 13]), SKEL_BLOOD_SCOURGE_FR: ([45, 85, 130, 150], [14, 14]), SKEL_SHADOW_CROW_SP: ([40, 80, 125, 145], [12, 12]), SKEL_HELLHOUND_SP: ([40, 80, 125, 145], [13, 13]), SKEL_BLOOD_SCOURGE_SP: ([45, 85, 130, 150], [14, 14])}

def getAIShipSpeed(shipClass):
    speedList = __enemyAIShipSpeed.get(shipClass)
    if speedList:
        return speedList
    else:
        return ([], [])


ShipFlatScales = {1: Vec3(0.6, 0.6, 0.6), 2: Vec3(1, 1, 1), 3: Vec3(1.3, 1.3, 1.3), 11: Vec3(0.6, 0.6, 0.6), 12: Vec3(1, 1, 1), 13: Vec3(1.3, 1.3, 1.3), 21: Vec3(0.5, 0.5, 0.5), 22: Vec3(0.75, 0.75, 0.75), 23: Vec3(1, 1, 1), 53: Vec3(2, 2, 2)}
ShipFlatOffsets = {1: Vec3(0, 7, -2), 2: Vec3(0, 0, 0), 3: Vec3(0, 0, -5), 11: Vec3(0, 0, 0), 12: Vec3(0, 0, 0), 13: Vec3(0, 0, 0), 21: Vec3(0, 0, 0), 22: Vec3(0, 0, 0), 23: Vec3(0, 0, 0), 53: Vec3(0, 0, 0)}
KrakenLocators = {INTERCEPTORL1: ((Point3(40, 20, -5), 0.5, Point3(0), 0.9), (Point3(40, -40, -5), 0.5, Point3(0), 0.9)), INTERCEPTORL2: ((Point3(50, 40, -5), 0.75, Point3(0), 0.9), (Point3(50, -70, -5), 0.75, Point3(0), 0.9)), INTERCEPTORL3: ((Point3(60, 80, 0), 0.8, Point3(0), 0.9), (Point3(60, -30, 0), 0.8, Point3(0), 0.9)), MERCHANTL1: ((Point3(30, 50, -5), 0.6, Point3(0), 0.9), (Point3(40, -10, -5), 0.6, Point3(0), 0.9), (Point3(40, -70, -5), 0.6, Point3(0), 0.9)), MERCHANTL2: ((Point3(50, 50, 0), 0.8, Point3(0), 0.9), (Point3(50, -10, 0), 0.8, Point3(0), 0.9), (Point3(50, -70, 0), 0.8, Point3(0), 0.9)), MERCHANTL3: ((Point3(60, 50, 0), 1, Point3(0), 0.9), (Point3(70, -10, 0), 1, Point3(0), 0.9), (Point3(70, -120, 0), 1, Point3(0), 0.9)), WARSHIPL1: ((Point3(30, 50, -15), 0.6, Point3(0, 22, 0), 0.7), (Point3(40, -10, -15), 0.6, Point3(0), 0.8), (Point3(40, -70, -15), 0.6, Point3(0), 0.8)), WARSHIPL2: ((Point3(40, 90, -15), 0.8, Point3(10, 25, 0), 0.8), (Point3(50, 10, -15), 0.8, Point3(0), 0.9), (Point3(50, -70, -15), 0.8, Point3(0), 0.9)), WARSHIPL3: ((Point3(50, 90, -15), 1, Point3(-20, 15, 0), 0.6), (Point3(60, 10, -15), 1, Point3(0), 0.8), (Point3(60, -120, -15), 1, Point3(0), 0.9))}
__shipSplitOffsets = {DINGHY: (0.0, 0), INTERCEPTORL1: (10.0, 0), INTERCEPTORL2: (2.0, 0), INTERCEPTORL3: (5.0, 0), INTERCEPTORL4: (0.0, -1), MERCHANTL1: (13.0, -1), MERCHANTL2: (0.0, 1), MERCHANTL3: (5.0, 0), MERCHANTL4: (0.0, -1), WARSHIPL1: (5.0, -1), WARSHIPL2: (-5.0, -1), WARSHIPL3: (0.0, -1), WARSHIPL4: (0.0, -1), BLACK_PEARL: (0.0, -1), GOLIATH: (0.0, -1)}

def getShipSplitOffset(shipClass):
    offset = __shipSplitOffsets.get(shipClass)
    if offset:
        return offset[0]
    else:
        return 0.0


def getShipBreakMast(shipClass):
    hasMast = __shipSplitOffsets.get(shipClass)
    if hasMast:
        return hasMast[1]
    else:
        return -1
# okay decompiling .\pirates\ship\ShipGlobals.pyc
