# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.web.PiratesSettingsMgrBase
from pirates.pvp import PVPGlobals
from pirates.ship import ShipBalance


class PiratesSettingsMgrBase:
    

    def _initSettings(self):
        self._addSettings(PVPGlobals.WantIslandRegen, PVPGlobals.WantShipRepairSpots, PVPGlobals.WantShipRepairKit, PVPGlobals.ShipRegenRadiusScale, PVPGlobals.ShipRegenHps, PVPGlobals.ShipRegenSps, PVPGlobals.ShipRegenPeriod, PVPGlobals.RepairRate, PVPGlobals.RepairRateMultipliers, PVPGlobals.RepairAcceleration, PVPGlobals.RepairAccelerationMultipliers, PVPGlobals.RepairKitHp, PVPGlobals.RepairKitSp, PVPGlobals.MainWorldInvulnerabilityDuration, PVPGlobals.MainWorldInvulnerabilityWantCutoff, PVPGlobals.MainWorldInvulnerabilityCutoffRadiusScale, PVPGlobals.SinkHpBonusPercent, ShipBalance.RepairRate, ShipBalance.RepairPeriod, ShipBalance.FalloffShift, ShipBalance.FalloffMultiplier, ShipBalance.SpeedModifier, ShipBalance.ArmorAbsorb, ShipBalance.ArmorBounce, ShipBalance.NPCArmorModifier, ShipBalance.NPCDamageIn, ShipBalance.NPCDamageOut, PVPGlobals.SinkStreakPeriod, PVPGlobals.MaxPrivateerShipsPerTeam)
        self._addSettings(*PVPGlobals.ShipClass2repairLocators.values())
# okay decompiling .\pirates\web\PiratesSettingsMgrBase.pyc
