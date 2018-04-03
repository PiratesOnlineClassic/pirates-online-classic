# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.ship.ShipBalance
from otp.web.Setting import StateVarSetting

RepairRate = StateVarSetting('ship.repair.rate', 500)
RepairPeriod = StateVarSetting('ship.repair.period', 2)
FalloffShift = StateVarSetting('ship.falloff.shift', 500)
FalloffMultiplier = StateVarSetting('ship.falloff.multiplier', 0.000339683)
SpeedModifier = StateVarSetting('ship.speed', 1.0)
ArmorAbsorb = StateVarSetting('ship.armor.absorb', 0.7)
ArmorBounce = StateVarSetting('ship.armor.bounce', 0.2)
NPCArmorModifier = StateVarSetting('ship.NPC.armor', 0.5)
NPCDamageIn = StateVarSetting('ship.NPC.damage.incoming', 2.6)
NPCDamageOut = StateVarSetting('ship.NPC.damage.outgoing', 1.8)
# okay decompiling .\pirates\ship\ShipBalance.pyc
