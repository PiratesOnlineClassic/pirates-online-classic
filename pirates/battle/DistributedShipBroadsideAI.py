from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *

from pirates.battle.DistributedWeaponAI import DistributedWeaponAI


class DistributedShipBroadsideAI(DistributedWeaponAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipBroadsideAI')

    def __init__(self, air):
        DistributedWeaponAI.__init__(self, air)

        self.shipId = 0
        self.geomParentId = 0

        self.leftBroadside = []
        self.rightBroadside = []

        self.leftBroadsideEnabledState = []
        self.rightBroadsideEnabledState = []

        self.baseTeam = 0
        self.ammoType = 0

    def requestBroadside(self, side, delays, hitPosList, zoneId, flightTime):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        ship = self.air.doId2do.get(self.shipId)
        if not ship:
            self.notify.warning('Cannot request broadside for unknown ship with doId: %d' % self.shipId)
            return

        if avatar.doId != ship.clientControllerDoId:
            return

        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        self.sendUpdate('doBroadside', [side, delays, hitPosList, zoneId, flightTime, timestamp])

    def setShipId(self, shipId):
        self.shipId = shipId

    def d_setShipId(self, shipId):
        self.sendUpdate('setShipId', [shipId])

    def b_setShipId(self, shipId):
        self.setShipId(shipId)
        self.d_setShipId(shipId)

    def getShipId(self):
        return self.shipId

    def getShip(self):
        return self.air.doId2do.get(self.shipId)

    def setGeomParentId(self, geomParentId):
        self.geomParentId = geomParentId

    def d_setGeomParentId(self, geomParentId):
        self.sendUpdate('setGeomParentId', [geomParentId])

    def b_setGeomParentId(self, geomParentId):
        self.setGeomParentId(geomParentId)
        self.d_setGeomParentId(geomParentId)

    def getGeomParentId(self):
        return self.geomParentId

    def setLeftBroadside(self, leftBroadside):
        self.leftBroadside = leftBroadside

    def getLeftBroadside(self):
        return self.leftBroadside

    def setRightBroadside(self, rightBroadside):
        self.rightBroadside = rightBroadside

    def getRightBroadside(self):
        return self.rightBroadside

    def setLeftBroadsideEnabledState(self, leftBroadsideEnabledState):
        self.leftBroadsideEnabledState = leftBroadsideEnabledState

    def d_setLeftBroadsideEnabledState(self, leftBroadsideEnabledState):
        self.sendUpdate('setLeftBroadsideEnabledState', [leftBroadsideEnabledState])

    def b_setLeftBroadsideEnabledState(self, leftBroadsideEnabledState):
        self.setLeftBroadsideEnabledState(leftBroadsideEnabledState)
        self.d_setLeftBroadsideEnabledState(leftBroadsideEnabledState)

    def getLeftBroadsideEnabledState(self):
        return self.leftBroadsideEnabledState

    def setRightBroadsideEnabledState(self, rightBroadsideEnabledState):
        self.rightBroadsideEnabledState = rightBroadsideEnabledState

    def d_setRightBroadsideEnabledState(self, rightBroadsideEnabledState):
        self.sendUpdate('setRightBroadsideEnabledState', [rightBroadsideEnabledState])

    def b_setRightBroadsideEnabledState(self, rightBroadsideEnabledState):
        self.setRightBroadsideEnabledState(rightBroadsideEnabledState)
        self.d_setRightBroadsideEnabledState(rightBroadsideEnabledState)

    def getRightBroadsideEnabledState(self):
        return self.rightBroadsideEnabledState

    def setBaseTeam(self, baseTeam):
        self.baseTeam = baseTeam

    def getBaseTeam(self):
        return self.baseTeam

    def setAmmoType(self, ammoType):
        self.ammoType = ammoType

    def getAmmoType(self):
        return self.ammoType
