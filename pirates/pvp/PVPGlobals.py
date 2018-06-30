from direct.fsm.StatePush import FunctionCall
from otp.web.Setting import StateVarSetting
from pandac.PandaModules import Vec4
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PLocalizer
from pirates.ship import ShipGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

RulesDuration = 12.0
ReadyTimeout = 120.0
ReadyBarrierTimeout = RulesDuration + ReadyTimeout
MainWorldAvRespawnDelay = 3.0
MainWorldInvulnerabilityDuration = StateVarSetting(
    'pvp.invulnerability.duration', 180.0)
MainWorldInvulnerabilityWantCutoff = StateVarSetting(
    'pvp.invulnerability.wantCutoff', 1)
MainWorldInvulnerabilityCutoffRadiusScale = StateVarSetting(
    'pvp.invulnerability.cutoffSphereRadiusScale', 1.1)
WantIslandRegen = StateVarSetting(
    'pvp.shipHeal.WantIslandRegen',
    getBase().config.GetBool('want-pvp-island-regeneration', 0))
WantShipRepairSpots = StateVarSetting(
    'pvp.shipHeal.WantShipRepairSpots',
    getBase().config.GetBool('want-ship-repair-spots', 1))
WantShipRepairKit = StateVarSetting(
    'pvp.shipHeal.WantShipRepairKit',
    getBase().config.GetBool('want-ship-repair-kit', 0))
ShipRegenRadiusScale = StateVarSetting('pvp.shipHeal.island.sphereRadiusScale',
                                       1.0)
ShipRegenHps = StateVarSetting('pvp.shipHeal.island.healPerSecHP', 50)
ShipRegenSps = StateVarSetting('pvp.shipHeal.island.healPerSecSP', 50)
ShipRegenPeriod = StateVarSetting('pvp.shipHeal.island.healPeriodSecs', 2)
RepairRate = StateVarSetting('pvp.shipHeal.repairSpots.repairRate', 10.0)
RepairRateMultipliers = StateVarSetting(
    'pvp.shipHeal.repairSpots.repairRateMultipliers', [1.0, 2.0, 3.0, 4.0])
RepairAcceleration = StateVarSetting(
    'pvp.shipHeal.repairSpots.repairAcceleration', 2)
RepairAccelerationMultipliers = StateVarSetting(
    'pvp.shipHeal.repairSpots.repairAccelerationMultipliers',
    [1.0, 1.0, 1.0, 1.0])
RepairKitHp = StateVarSetting(
    'pvp.shipHeal.repairKit.HP',
    WeaponGlobals.getAttackHullHP(InventoryType.ShipRepairKit))
RepairKitSp = StateVarSetting(
    'pvp.shipHeal.repairKit.SP',
    WeaponGlobals.getAttackSailHP(InventoryType.ShipRepairKit))
SinkHpBonusPercent = StateVarSetting('pvp.sinkBonus.hp.percent', 0.8)
SinkStreakPeriod = StateVarSetting('pvp.announcements.sinkStreakPeriod', 5)


def updateRepairKitHp(hp):
    WeaponGlobals.__skillInfo[InventoryType.ShipRepairKit][
        WeaponGlobals.HULL_HP_INDEX] = hp


def updateRepairKitSp(sp):
    WeaponGlobals.__skillInfo[InventoryType.ShipRepairKit][
        WeaponGlobals.SAIL_HP_INDEX] = sp


UpdateRepairKitHp = FunctionCall(updateRepairKitHp, RepairKitHp)
UpdateRepairKitSp = FunctionCall(updateRepairKitSp, RepairKitSp)
RepairSpotLocatorNames = [
    'repair_spot_0', 'repair_spot_1', 'repair_spot_2', 'repair_spot_3'
]
repairSpotNamePrefix = 'pvp.shipHeal.repairSpots.spots.'
ShipClass2repairLocators = {
    ShipGlobals.INTERCEPTORL1:
    StateVarSetting(repairSpotNamePrefix + 'interceptorL1', [0, 1, 2, 3]),
    ShipGlobals.INTERCEPTORL2:
    StateVarSetting(repairSpotNamePrefix + 'interceptorL2', [0, 1, 2, 3]),
    ShipGlobals.INTERCEPTORL3:
    StateVarSetting(repairSpotNamePrefix + 'interceptorL3', [0, 1, 2, 3]),
    ShipGlobals.MERCHANTL1:
    StateVarSetting(repairSpotNamePrefix + 'merchantL1', [0, 1, 2, 3]),
    ShipGlobals.MERCHANTL2:
    StateVarSetting(repairSpotNamePrefix + 'merchantL2', [0, 1, 2, 3]),
    ShipGlobals.MERCHANTL3:
    StateVarSetting(repairSpotNamePrefix + 'merchantL3', [0, 1, 2, 3]),
    ShipGlobals.WARSHIPL1:
    StateVarSetting(repairSpotNamePrefix + 'warshipL1', [0, 1, 2, 3]),
    ShipGlobals.WARSHIPL2:
    StateVarSetting(repairSpotNamePrefix + 'warshipL2', [0, 1, 2, 3]),
    ShipGlobals.WARSHIPL3:
    StateVarSetting(repairSpotNamePrefix + 'warshipL3', [0, 1, 2, 3])
}
del repairSpotNamePrefix
INSTANCE_PVP_CTL = 0
INSTANCE_PVP_STB = 1
WIN_COND_SCORE = 1
WIN_COND_TIME = 2
WIN_COND_CAPTURE = 3
ID = 0
NAME = 1
SCORE = 2
KILLS = 3
DEATHS = 4
RANK = 5
TEAM = 6
BOUNTY = 7
TOO_LOW_LEVEL = 12
GOOD_MATCH = 2
PLAYER_SCORE = 0
SHIP_SCORE = 1
TEAM_SCORE = 2
siegeTeamNames = {
    1: PLocalizer.ShipPVPQuestFrench,
    2: PLocalizer.ShipPVPQuestSpanish
}
MaxPrivateerShipsPerTeam = StateVarSetting(
    'pvp.maxShipsPerTeam',
    getBase().config.GetInt('max-ships-per-privateer-team', 10))
statText = {
    SCORE: PLocalizer.PVPScore,
    KILLS: PLocalizer.PVPEnemiesDefeated,
    DEATHS: PLocalizer.PVPTimesDefeated,
    BOUNTY: PLocalizer.PVPBounty
}
TEAM_COLOR = [
    Vec4(1.0, 0.4, 0.4, 1.0),
    Vec4(0.4, 0.4, 1.0, 1.0),
    Vec4(0.4, 1.0, 0.4, 1.0),
    Vec4(0.4, 1.0, 1.0, 1.0),
    Vec4(1.0, 0.4, 1.0, 1.0),
    Vec4(1.0, 1.0, 0.4, 1.0),
    Vec4(0.0, 0.0, 0.0, 1.0),
    Vec4(0.5, 0.5, 0.5, 1.0),
    Vec4(1.0, 1.0, 1.0, 1.0),
    Vec4(0.2, 0.4, 0.4, 1.0),
    Vec4(0.4, 0.2, 0.4, 1.0),
    Vec4(0.4, 0.4, 0.2, 1.0)
]


def getTeamColor(team, TEAM_COLOR=TEAM_COLOR):
    return TEAM_COLOR[(team - 1) % len(TEAM_COLOR)]


SIEGE_TEAM_COLOR = [Vec4(0.1, 0.33, 0.7, 1.0), Vec4(1.0, 0.8, 0.0, 1.0)]


def getSiegeColor(team, SIEGE_TEAM_COLOR=SIEGE_TEAM_COLOR):
    return SIEGE_TEAM_COLOR[(team - 1) % len(SIEGE_TEAM_COLOR)]


EventDefeat = 0
TeamBalanceValues = ScratchPad()
TeamBalanceValues.Player = 2
TeamBalanceValues.Ships = {
    ShipGlobals.INTERCEPTORL1: 5,
    ShipGlobals.INTERCEPTORL2: 8,
    ShipGlobals.INTERCEPTORL3: 12,
    ShipGlobals.MERCHANTL1: 13,
    ShipGlobals.MERCHANTL2: 18,
    ShipGlobals.MERCHANTL3: 22,
    ShipGlobals.WARSHIPL1: 12,
    ShipGlobals.WARSHIPL2: 15,
    ShipGlobals.WARSHIPL3: 20
}
RenownWorthValues = {
    ShipGlobals.INTERCEPTORL1: 2,
    ShipGlobals.INTERCEPTORL2: 4,
    ShipGlobals.INTERCEPTORL3: 6,
    ShipGlobals.MERCHANTL1: 4,
    ShipGlobals.MERCHANTL2: 7,
    ShipGlobals.MERCHANTL3: 10,
    ShipGlobals.WARSHIPL1: 5,
    ShipGlobals.WARSHIPL2: 8,
    ShipGlobals.WARSHIPL3: 10
}
RenownIconsSea = {
    0: 'sail_come_about',
    1: 'sail_come_about',
    2: 'sail_come_about',
    3: 'sail_come_about',
    4: 'sail_come_about',
    5: 'sail_come_about',
    6: 'sail_come_about',
    7: 'sail_come_about',
    8: 'sail_come_about',
    9: 'sail_come_about',
    10: 'sail_come_about'
}
RenownIconsLand = {
    0: 'sail_come_about',
    1: 'sail_come_about',
    2: 'sail_come_about',
    3: 'sail_come_about',
    4: 'sail_come_about',
    5: 'sail_come_about',
    6: 'sail_come_about',
    7: 'sail_come_about',
    8: 'sail_come_about',
    9: 'sail_come_about',
    10: 'sail_come_about'
}


class ShipDescription:

    def __init__(self, shipClass):
        self.shipClass = shipClass


def getTeamBalanceValue(obj):
    if hasattr(obj, 'shipClass'):
        return TeamBalanceValues.Ships[obj.shipClass]
    return TeamBalanceValues.Player


RenownBreakpointsLand = [0, 50, 150, 350, 650, 1200, 2500, 10000]
RenownBreakpointsSea = [0, 50, 150, 350, 650, 1200, 2500, 10000]


def getRankLand(expPoints):
    high = 0
    for testValue in RenownBreakpointsLand:
        if testValue > expPoints:
            return high - 1
        high += 1

    return high - 1


def getRankSea(expPoints):
    high = 0
    for testValue in RenownBreakpointsSea:
        if testValue > expPoints:
            return high - 1
        high += 1

    return high - 1


def getMaxRankLand():
    return len(RenownBreakpointsLand) - 1


def getMaxRankSea():
    return len(RenownBreakpointsSea) - 1


def getShipInfamyWorth(shipClass):
    if shipClass:
        if shipClass in RenownWorthValues:
            return RenownWorthValues.get(shipClass)
        return 1
    return 0


BountyRanks = [50, 100, 250, 500, 1000]
BountyRankLevels = len(BountyRanks)
