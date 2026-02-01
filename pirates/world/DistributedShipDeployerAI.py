import random
import math

from panda3d.core import *

from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.distributed.ClockDelta import *

from pirates.piratesbase import PiratesGlobals


class ShipDeployerOperationFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipDeployerOperationFSM')

    def __init__(self, air, shipDeployer, avatar, callback=None):
        FSM.__init__(self, self.__class__.__name__)

        self.air = air
        self.shipDeployer = shipDeployer
        self.avatar = avatar
        self.callback = callback

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterStart(self):
        pass

    def exitStart(self):
        pass

    def cleanup(self, *args, **kwargs):
        del self.shipDeployer.avatar2fsm[self.avatar.doId]
        self.ignoreAll()
        self.demand('Off')

        if self.callback:
            self.callback(*args, **kwargs)


class DeployShipFSM(ShipDeployerOperationFSM):

    def enterStart(self, shipId):
        self.shipId = shipId
        if not self.shipId:
            self.notify.warning('Cannot deploy ship for avatar %d, '
                'invalid shipId specified!' % self.avatar.doId)

            self.cleanup(False)
            return

        self.island = self.air.doId2do.get(self.shipDeployer.parentId)
        self.islandParentObj = self.island.getParentObj()
        self.oceanGrid = self.islandParentObj.oceanGrid

        deployerSphere = self.shipDeployer.getRandomSphere()
        self.spawnPoint = self.getSpawnPointFromSphere(*deployerSphere)
        self.zoneId = self.oceanGrid.getZoneFromXYZ(self.spawnPoint)

        ship = self.air.doId2do.get(self.shipId)
        if ship is None:
            self.acceptOnce('generate-%d' % self.shipId, self.shipArrivedCallback)
            self.air.sendSetObjectLocation(self.shipId, self.oceanGrid.doId, self.zoneId)
        else:
            ship.b_setLocation(self.oceanGrid.doId, self.zoneId)
            self.shipArrivedCallback(ship)

    def getSpawnPointFromSphere(self, sx, sy, sz):
        radius = self.shipDeployer.getSpacing() / 2.0
        x = random.uniform(sx - radius, sx + radius)
        y = random.uniform(sy - radius, sy + radius)
        return Point3(x, y, sz)

    def shipArrivedCallback(self, ship):
        self.ship = ship
        if not self.ship:
            self.notify.warning('Cannot deploy ship %d for avatar %d, '
                'ship is not present on the AI!' % (self.shipId, self.avatar.doId))

            self.cleanup(False)
            return

        # set the ship's captain
        self.ship.b_setCaptainId(self.avatar.doId)

        # move the ship to it's appropriate locations
        self.ship.setPos(self.oceanGrid, *self.spawnPoint)
        self.oceanGrid.addObjectToOceanGrid(self.ship)

        # only send our current position to initially position the ship,
        # the client will take over and control the ship beyond this point...
        self.ship.sendCurrentPosition()
        self.ship.b_setGameState('Docked', 0)

        self.inventory = self.air.doId2do.get(self.ship.inventoryId)
        if not self.inventory:
            self.notify.warning('Cannot deploy ship %d for avatar %d, '
                'ship has no inventory!' % (self.shipId, self.avatar.doId))

            self.cleanup(False)
            return

        self.shipMainpartsDoIdList = list(self.inventory.getShipMainpartsDoIdList())
        if not self.shipMainpartsDoIdList:
            self.notify.warning('Cannot deploy ship %d for avatar %d, '
                'ship has no main-shipparts!' % (self.shipId, self.avatar.doId))

            self.cleanup(False)
            return

        for shippartDoId in list(self.shipMainpartsDoIdList):
            shippart = self.air.doId2do.get(shippartDoId)
            if shippart is None:
                self.acceptOnce('generate-%d' % shippartDoId, self.shippartArrivedCallback)
                self.air.sendSetObjectLocation(shippartDoId, self.ship.doId, PiratesGlobals.ShipZoneSilhouette)
            else:
                shippart.b_setLocation(self.ship.doId, PiratesGlobals.ShipZoneSilhouette)
                self.shippartArrivedCallback(shippart)

    def _finalizeDeploy(self):
        # the ship has been successfully deployed, mark it as deployed,
        # this will allow anyone who wants to join the ship to be able to do so...
        self.ship.setDeploy(True)

        # add the ship to the ship manager's list of `deployed` ships,
        # the ship will be removed by the PlayerShipAI class when delete is called.
        self.air.shipManager.addPlayerShip(self.ship)

    def shippartArrivedCallback(self, shippart):
        self.shipMainpartsDoIdList.remove(shippart.doId)
        if not self.shipMainpartsDoIdList:
            self._finalizeDeploy()
            self.cleanup(True)

    def exitStart(self):
        pass


class DistributedShipDeployerAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipDeployerAI')

    def __init__(self, air, island):
        DistributedNodeAI.__init__(self, air)

        self.island = island

        self.minRadius = 0
        self.maxRadius = 0
        self.spacing = 0
        self.heading = 0

        self.deploySpheres = []
        self.avatar2fsm = {}

    def setMinRadius(self, minRadius):
        self.minRadius = minRadius

    def d_setMinRadius(self, minRadius):
        self.sendUpdate('setMinRadius', [minRadius])

    def b_setMinRadius(self, minRadius):
        self.setMinRadius(minRadius)
        self.d_setMinRadius(minRadius)

    def getMinRadius(self):
        return self.minRadius

    def setMaxRadius(self, maxRadius):
        self.maxRadius = maxRadius

    def d_setMaxRadius(self, maxRadius):
        self.sendUpdate('setMaxRadius', [maxRadius])

    def b_setMaxRadius(self, maxRadius):
        self.setMaxRadius(maxRadius)
        self.d_setMaxRadius(maxRadius)

    def getMaxRadius(self):
        return self.maxRadius

    def setSpacing(self, spacing):
        self.spacing = spacing

    def d_setSpacing(self, spacing):
        self.sendUpdate('setSpacing', [spacing])

    def b_setSpacing(self, spacing):
        self.setSpacing(spacing)
        self.d_setSpacing(spacing)

    def getSpacing(self):
        return self.spacing

    def setHeading(self, heading):
        self.heading = heading

    def d_setHeading(self, heading):
        self.sendUpdate('setHeading', [heading])

    def b_setHeading(self, heading):
        self.setHeading(heading)
        self.d_setHeading(heading)

    def getHeading(self):
        return self.heading

    def generate(self):
        DistributedNodeAI.generate(self)
        self.createDeploySpheres()

    def createDeploySpheres(self):
        deployRingRadius = self.minRadius + self.spacing / 2.0
        C = 2 * math.pi * deployRingRadius
        numSpheres = int(C / self.spacing)
        stepAngle = 360.0 / numSpheres

        def getSpherePos(sphereId):
            h = sphereId * stepAngle + 90.0 + self.heading
            angle = h * math.pi / 180.0
            pos = Point3(math.cos(angle), math.sin(angle), 0) * deployRingRadius
            return pos

        for x in range(numSpheres):
            ax, ay, az = getSpherePos(x)
            bx, by = self.island.sphereCenter
            cx, cy = bx + ax, by + ay
            #cSphere = CollisionSphere(pos[0], pos[1], 0, self.spacing / 2.0)
            #cSphere.setTangible(0)
            #cSphereNode = CollisionNode(self.uniqueName('ShipDeploySphere'))
            #cSphereNode.addSolid(cSphere)
            #sphere = self.attachNewNode(cSphereNode)
            #sphere.setTag('deploySphereId', `x`)
            self.deploySpheres.append((cx, cy, az))

    def getSphere(self, index):
        return self.deploySpheres[index]

    def getRandomSphere(self):
        return random.choice(self.deploySpheres)

    def runShipDeployerFSM(self, fsmtype, avatar, *args, **kwargs):
        if avatar.doId in self.avatar2fsm:
            self.notify.debug('Failed to run ship deployer FSM for avatar %d, '
                'an inventory FSM is already running!' % avatar.doId)

            return

        callback = kwargs.pop('callback', None)

        self.avatar2fsm[avatar.doId] = fsmtype(self.air, self, avatar, callback)
        self.avatar2fsm[avatar.doId].request('Start', *args, **kwargs)

    def deployShip(self, avatar, shipId, callback=None):
        self.runShipDeployerFSM(DeployShipFSM, avatar, shipId, callback=callback)
