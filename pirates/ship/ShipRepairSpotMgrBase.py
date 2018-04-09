# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.ship.ShipRepairSpotMgrBase
from direct.fsm.StatePush import AttrSetter, FunctionCall, StateVar
from pirates.pvp import PVPGlobals


class ShipRepairSpotMgrBase:
    

    def __init__(self):
        self._state = DestructiveScratchPad(hp=StateVar(0), maxHp=StateVar(0), sp=StateVar(0), maxSp=StateVar(0), shipClass=StateVar(0), pvpTeam=StateVar(0), siegeTeam=StateVar(0), fullHealth=StateVar(False), validShipClass=StateVar(False), hasTeam=StateVar(False))
        self._statePushes = []

    def destroy(self):
        for statePush in self._statePushes:
            statePush.destroy()

        del self._statePushes
        self._state.destroy()

    def _onShipReady(self):
        self._statePushes.extend([
         FunctionCall(self._evalFullHealth, self._state.hp, self._state.maxHp, self._state.sp, self._state.maxSp), FunctionCall(self._evalValidShipClass, self._state.shipClass), FunctionCall(self._evalHasTeam, self._state.pvpTeam, self._state.siegeTeam)])

    def updateHp(self, hp):
        self._state.hp.set(hp)

    def updateMaxHp(self, maxHp):
        self._state.maxHp.set(maxHp)

    def updateSp(self, sp):
        self._state.sp.set(sp)

    def updateMaxSp(self, maxSp):
        self._state.maxSp.set(maxSp)

    def updateShipClass(self, shipClass):
        self._state.shipClass.set(shipClass)

    def updatePVPTeam(self, team):
        self._state.pvpTeam.set(team)

    def updateSiegeTeam(self, team):
        self._state.siegeTeam.set(team)

    def _evalFullHealth(self, hp, maxHp, sp, maxSp):
        self._state.fullHealth.set(hp >= maxHp and sp >= maxSp)

    def _evalValidShipClass(self, shipClass):
        self._state.validShipClass.set(shipClass in PVPGlobals.ShipClass2repairLocators)

    def _evalHasTeam(self, pvpTeam, siegeTeam):
        self._state.hasTeam.set(pvpTeam or siegeTeam)
# okay decompiling .\pirates\ship\ShipRepairSpotMgrBase.pyc
