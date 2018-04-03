# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.ship.ShipRepairSpotMgr
from direct.fsm.StatePush import FunctionCall, StateVar
from pirates.pvp import PVPGlobals
from pirates.ship.ShipRepairSpotMgrBase import ShipRepairSpotMgrBase

class ShipRepairSpotMgr(ShipRepairSpotMgrBase):
    __module__ = __name__

    def __init__(self, cr, shipId):
        ShipRepairSpotMgrBase.__init__(self)
        self.cr = cr
        self._ship = self.cr.doId2do[shipId]
        self._state.add(needModels=StateVar(False), needHoles=StateVar(False))
        self._ship.registerMainBuiltFunction(self._onShipReady)

    def destroy(self):
        self._state.needHoles.set(False)
        self._state.needModels.set(False)
        ShipRepairSpotMgrBase.destroy(self)
        del self._ship
        del self.cr

    def _onShipReady(self):
        ShipRepairSpotMgrBase._onShipReady(self)
        self._statePushes.extend([FunctionCall(self._evalNeedModels, self._state.validShipClass, self._state.hasTeam), FunctionCall(self._evalNeedHoles, self._state.fullHealth, self._state.needModels), FunctionCall(self._needModelsChanged, self._state.needModels), FunctionCall(self._needHolesChanged, self._state.needHoles),
         FunctionCall(self._handleRepairSpotIndicesChanged, PVPGlobals.ShipClass2repairLocators[self._ship.shipClass])])

    def _evalNeedModels(self, validShipClass, hasTeam):
        self._state.needModels.set(validShipClass and hasTeam)

    def _evalNeedHoles(self, fullHealth, needModels):
        self._state.needHoles.set(needModels and not fullHealth)

    def _needModelsChanged(self, needModels):
        if needModels:
            self._ship._addRepairSpotModels()
        else:
            self._ship._removeRepairSpotModels()

    def _needHolesChanged(self, needHoles):
        if needHoles:
            self._ship._addRepairSpotHoles()
        else:
            self._ship._removeRepairSpotHoles()

    def _handleRepairSpotIndicesChanged(self, indices):
        if self._state.needModels.get():
            self._state.needModels.set(False)
            self._state.needModels.set(True)
# okay decompiling .\pirates\ship\ShipRepairSpotMgr.pyc
