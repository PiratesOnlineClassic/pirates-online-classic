import random

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *

from pirates.battle.DistributedWeaponAI import DistributedWeaponAI
from pirates.ship import ShipGlobals
from pirates.ship import ShipBalance


class DistributedShipBroadsideAI(DistributedWeaponAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipBroadsideAI')

    CannonballSpeed = 500.0
    CannonballDamage = 50
    BaseAccuracy = 0.7

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

        if not ship.isSailable():
            return

        if side not in (ShipGlobals.BROADSIDE_LEFT, ShipGlobals.BROADSIDE_RIGHT):
            return

        # the broadside is fired by the helmsman's broadside skill, which
        # recharges between each broadside (see DistributedShipAI.useShipSkill)...
        if not ship.consumeBroadside(side):
            self.notify.debug('Avatar %d requested broadside %d of ship %d without using '
                'the broadside skill!' % (avatar.doId, side, ship.doId))

            return

        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        self.sendUpdate('doBroadside', [side, delays, hitPosList, zoneId, flightTime, timestamp])

    def requestCannonEnabledState(self, side, index, state):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        # clients may only report a cannon port as being knocked out by a projectile,
        # the cannon ports are only ever re-enabled by repairing the ship...
        if state:
            self.air.writeServerEvent('suspicious', avId=avatar.doId,
                issue='Tried to enable cannon port %d:%d on broadside %d!' % (side, index, self.doId))

            return

        if side == ShipGlobals.BROADSIDE_LEFT:
            enabledState = list(self.leftBroadsideEnabledState)
        elif side == ShipGlobals.BROADSIDE_RIGHT:
            enabledState = list(self.rightBroadsideEnabledState)
        else:
            return

        if index >= len(enabledState) or not enabledState[index]:
            return

        enabledState[index] = 0
        if side == ShipGlobals.BROADSIDE_LEFT:
            self.b_setLeftBroadsideEnabledState(enabledState)
        else:
            self.b_setRightBroadsideEnabledState(enabledState)

    def setCannonAnim(self, index, side, anim, timestamp):
        # this field is relayed between the clients by the state server,
        # there is nothing for the AI to do with it...
        pass

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

    def d_doBroadside(self, side, delays, hitPosList, zoneId, flightTime):
        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        self.sendUpdate('doBroadside', [side, delays, hitPosList, zoneId, flightTime, timestamp])

    def fireAtTarget(self, targetShip, side):
        # NPC ships fire their broadsides from the AI, the shots are shown to
        # the clients and the damage is applied once the cannonballs land...
        ship = self.getShip()
        if not ship or not targetShip:
            return False

        numCannons = len(self.leftBroadside if side == ShipGlobals.BROADSIDE_LEFT else self.rightBroadside)
        if not numCannons:
            return False

        # the target is parented to it's ocean grid cell, the shots land
        # relative to the cell of the ocean grid the target is in:
        oceanGrid = ship.getParentObj()
        targetPos = targetShip.getPos(oceanGrid)
        zoneId = oceanGrid.getZoneFromXYZ(targetPos)
        zonePos = oceanGrid.getZoneCellOrigin(zoneId)

        delays = []
        hitPosList = []
        for _ in range(numCannons):
            delays.append(random.uniform(0, 0.5))
            hitPosList.append((targetPos[0] - zonePos[0] + random.gauss(0, 25),
                targetPos[1] - zonePos[1] + random.gauss(0, 25),
                targetPos[2] - zonePos[2] + random.gauss(0, 10)))

        distance = ship.getDistance(targetShip)
        flightTime = max(1.0, distance / self.CannonballSpeed)
        self.d_doBroadside(side, delays, hitPosList, zoneId, flightTime)

        taskMgr.doMethodLater(flightTime, self.__broadsideLanded,
            self.uniqueName('broadside-damage-%d' % targetShip.doId),
            extraArgs=[targetShip, numCannons, distance])

        return True

    def __broadsideLanded(self, targetShip, numCannons, distance):
        ship = self.getShip()
        if not ship or targetShip.isEmpty() or targetShip.hasSpawnBuff():
            return

        # the further away the target is the less accurate and
        # less damaging the broadside will be:
        rangeRatio = distance / ShipGlobals.BROADSIDE_MAX_AUTOAIM_DIST
        hitChance = self.BaseAccuracy * max(0.3, 1.0 - rangeRatio * 0.4)
        damage = self.CannonballDamage * ShipBalance.NPCDamageOut.getValue() * max(0.3, 1.0 - rangeRatio * 0.5)
        totalDamage = int(sum(damage for _ in range(numCannons) if random.random() < hitChance))
        if not totalDamage:
            return

        if hasattr(targetShip, 'takeDamage'):
            targetShip.takeDamage(totalDamage, ship.doId, applyModifiers=False)
        else:
            targetShip.handleShipDamage(-totalDamage, ship)
