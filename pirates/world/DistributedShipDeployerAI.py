import random
import math

from panda3d.core import *

from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.distributed.ClockDelta import *

from pirates.battle import WeaponGlobals
from pirates.piratesbase import FreebooterAI
from pirates.piratesbase import PiratesGlobals

# how long a freshly deployed ship is covered by the protection dome (C_SPAWN):
SPAWN_PROTECTION_DURATION = ConfigVariableDouble('ship-spawn-protection-duration', 30.0).getValue()

# the spacing used when an island's zone spheres leave no room
# between the min (reef) and max (barrier) deploy radius:
DEFAULT_DEPLOY_SPACING = 500.0

# sphere ids are sent by the client as an uint8 (shipEnteredSphere/shipExitedSphere):
MAX_DEPLOY_SPHERES = 255


def getDeploySpacing(minRadius, maxRadius):
    # the deploy spheres fill the band between the island's reef (min radius)
    # and deploy barrier (max radius)...
    spacing = maxRadius - minRadius
    if spacing <= 0:
        spacing = DEFAULT_DEPLOY_SPACING

    # keep the number of spheres the client builds within the range of a sphere id,
    # numSpheres = 2 * pi * (minRadius + spacing / 2) / spacing...
    minSpacing = (2 * math.pi * minRadius) / (MAX_DEPLOY_SPHERES - math.pi)
    return max(spacing, math.ceil(minSpacing))


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

    def enterStart(self, shipId, preferredPos=None, allowSunk=False):
        self.shipId = shipId
        self.allowSunk = allowSunk
        if not self.shipId:
            self.notify.warning('Cannot deploy ship for avatar %d, '
                'invalid shipId specified!' % self.avatar.doId)

            self.cleanup(False)
            return

        self.island = self.air.doId2do.get(self.shipDeployer.parentId)
        self.islandParentObj = self.island.getParentObj()
        self.oceanGrid = self.islandParentObj.oceanGrid

        ship = self.air.doId2do.get(self.shipId)
        self.shipWasActive = ship is not None
        if ship is not None and not self.canDeployShip(ship):
            self.cleanup(False)
            return

        # deploy the ship into a free sphere around the island, preferring the one
        # closest to where the avatar asked for it (the dinghy they used)...
        self.sphereId = self.shipDeployer.chooseDeploySphere(self.oceanGrid,
            preferredPos=preferredPos, excludeShipId=self.shipId)

        self.spawnPoint = self.shipDeployer.getOceanSpawnPoint(self.sphereId)
        self.spawnHeading = self.shipDeployer.getOceanSpawnHeading(self.sphereId)
        self.zoneId = self.oceanGrid.getZoneFromXYZ(self.spawnPoint)

        if ship is None:
            self.acceptOnce('generate-%d' % self.shipId, self.shipArrivedCallback)
            self.air.sendSetObjectLocation(self.shipId, self.oceanGrid.doId, self.zoneId)
        else:
            ship.b_setLocation(self.oceanGrid.doId, self.zoneId)
            self.shipArrivedCallback(ship)

    def canDeployShip(self, ship):
        # a sunk ship has to be repaired by a shipwright before it can be deployed again,
        # the client greys these ships out (see ShipFrameDeploy.enableStatsOV)...
        if ship.getHp() <= 0 and not self.allowSunk:
            self.notify.warning('Cannot deploy ship %d for avatar %d, '
                'the ship is sunk!' % (ship.doId, self.avatar.doId))

            return False

        # a Freebooter may only captain the free ship classes,
        # see ShipFrameDeploy.enableStats...
        if not FreebooterAI.canUseShipClass(self.avatar, ship.getShipClass()):
            self.notify.warning('Cannot deploy ship %d for freebooter %d, '
                'ship class %d requires Unlimited Access!' % (ship.doId, self.avatar.doId, ship.getShipClass()))

            return False

        return True

    def shipArrivedCallback(self, ship):
        self.ship = ship
        if not self.ship:
            self.notify.warning('Cannot deploy ship %d for avatar %d, '
                'ship is not present on the AI!' % (self.shipId, self.avatar.doId))

            self.cleanup(False)
            return

        if not self.canDeployShip(self.ship):
            # the ship was only brought onto the AI to be deployed, put it back...
            if not self.shipWasActive:
                self.ship.b_setLocation(0, 0)

            self.cleanup(False)
            return

        if self.ship.getHp() <= 0:
            # siege ships are always deployed at full health:
            self.ship.repairShip()

        # set the ship's captain
        self.ship.b_setCaptainId(self.avatar.doId)

        # move the ship to it's deploy sphere, facing out to sea...
        self.ship.setPos(self.oceanGrid, *self.spawnPoint)
        self.ship.setHpr(self.oceanGrid, self.spawnHeading, 0, 0)
        self.oceanGrid.addObjectToOceanGrid(self.ship)
        self.shipDeployer.addShipToSphere(self.sphereId, self.ship.doId)

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
        # this will allow anyone who wants to join the ship to be able to do so.
        # The client fades the ship in with the deploy fog once its parts are built...
        self.ship.b_setDeploy(1)

        # newly deployed ships are covered by the protection dome for a short window,
        # so they cannot be attacked before the captain has made it to the wheel...
        self.shipDeployer.protectShip(self.ship)

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
        self.sphere2shipIds = {}
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
        # mirrors DistributedShipDeployer.createDeploySpheres, sphere centers are
        # local to the deployer node which sits at the island's zone sphere center...
        self.deploySpheres = []
        if self.spacing <= 0 or self.minRadius < 0:
            return

        deployRingRadius = self.minRadius + self.spacing / 2.0
        C = 2 * math.pi * deployRingRadius
        numSpheres = max(1, int(C / self.spacing))
        stepAngle = 360.0 / numSpheres

        def getSpherePos(sphereId):
            h = sphereId * stepAngle + 90.0 + self.heading
            angle = h * math.pi / 180.0
            return Point3(math.cos(angle), math.sin(angle), 0) * deployRingRadius

        for x in range(numSpheres):
            pos = getSpherePos(x)
            self.deploySpheres.append((pos[0], pos[1], pos[2]))

    def getNumSpheres(self):
        if not self.deploySpheres:
            self.createDeploySpheres()

        return len(self.deploySpheres)

    def getSphere(self, index):
        return self.deploySpheres[index]

    def getSphereRadius(self):
        return self.spacing / 2.0

    def getIslandSpherePos(self, sphereId):
        # the sphere's center relative to the island:
        sx, sy, sz = self.getSphere(sphereId)
        return Point3(self.getX() + sx, self.getY() + sy, sz)

    def getSphereHeading(self, sphereId):
        # each sphere sits at (sphereId * stepAngle + 90 + heading) degrees around the ring,
        # a ship with a heading 90 degrees less than that points directly out to sea...
        return sphereId * (360.0 / self.getNumSpheres()) + self.heading

    def localToOceanPoint(self, localX, localY, localZ=0.0):
        # the island's ocean pose is carried by setIslandTransform,
        # not by the DistributedNode position fields...
        ix, iy, iz, ih = self.island.getIslandTransform()
        angle = math.radians(ih)
        cosH = math.cos(angle)
        sinH = math.sin(angle)
        worldX = ix + localX * cosH - localY * sinH
        worldY = iy + localX * sinH + localY * cosH
        return Point3(worldX, worldY, iz + localZ)

    def getOceanSpawnPoint(self, sphereId):
        pos = self.getIslandSpherePos(sphereId)

        # ships always float at sea level:
        spawnPoint = self.localToOceanPoint(pos[0], pos[1])
        spawnPoint.setZ(0)
        return spawnPoint

    def getOceanSpawnHeading(self, sphereId):
        return (self.island.getIslandTransform()[3] + self.getSphereHeading(sphereId)) % 360.0

    def addShipToSphere(self, sphereId, shipId):
        self.removeShipFromSpheres(shipId)
        self.sphere2shipIds.setdefault(sphereId, set()).add(shipId)

    def removeShipFromSphere(self, sphereId, shipId):
        shipIds = self.sphere2shipIds.get(sphereId)
        if not shipIds:
            return

        shipIds.discard(shipId)
        if not shipIds:
            del self.sphere2shipIds[sphereId]

    def removeShipFromSpheres(self, shipId):
        for sphereId in list(self.sphere2shipIds.keys()):
            self.removeShipFromSphere(sphereId, shipId)

    def isSphereOccupied(self, sphereId, oceanGrid, excludeShipId=0):
        # ships reported in the sphere by their captain's client:
        for shipId in list(self.sphere2shipIds.get(sphereId, ())):
            if shipId == excludeShipId:
                continue

            if shipId not in self.air.doId2do:
                self.removeShipFromSphere(sphereId, shipId)
                continue

            return True

        # any other ship that is sitting within the sphere right now:
        center = self.getOceanSpawnPoint(sphereId)
        radius = self.getSphereRadius()
        shipManager = self.air.shipManager
        for ship in shipManager.getPlayerShips() + shipManager.getShips():
            if ship.doId == excludeShipId or ship.isEmpty():
                continue

            if ship.getParentObj() is not oceanGrid:
                continue

            pos = ship.getPos(oceanGrid)
            if (Vec3(pos[0], pos[1], 0) - Vec3(center[0], center[1], 0)).length() < radius:
                return True

        return False

    def chooseDeploySphere(self, oceanGrid, preferredPos=None, excludeShipId=0):
        numSpheres = self.getNumSpheres()
        if not numSpheres:
            return 0

        candidates = [sphereId for sphereId in range(numSpheres)
            if not self.isSphereOccupied(sphereId, oceanGrid, excludeShipId)]

        if not candidates:
            # every sphere is taken, the deploy fog will have to sort it out...
            candidates = list(range(numSpheres))

        if preferredPos is None:
            return random.choice(candidates)

        def getDistance(sphereId):
            pos = self.getIslandSpherePos(sphereId)
            return (pos[0] - preferredPos[0]) ** 2 + (pos[1] - preferredPos[1]) ** 2

        return min(candidates, key=getDistance)

    def protectShip(self, ship):
        ship.addSkillEffect(WeaponGlobals.C_SPAWN, int(SPAWN_PROTECTION_DURATION), ship.doId)

    def unprotectShip(self, ship):
        if not ship.hasSpawnBuff():
            return

        ship.removeSkillEffect(WeaponGlobals.C_SPAWN, ship.doId)

    def _getReportedShip(self, shipId, fieldName):
        avatarId = self.air.getAvatarIdFromSender()
        ship = self.air.doId2do.get(shipId)
        if ship is None or not hasattr(ship, 'getClientController'):
            self.notify.debug('Avatar %d sent %s for unknown ship %d!' % (avatarId, fieldName, shipId))
            return None

        # the deploy spheres are only enabled for the ship the client is steering:
        if avatarId != ship.getClientController() and avatarId not in ship.getCrew():
            self.air.writeServerEvent('suspicious', avId=avatarId,
                issue='Sent %s for ship %d which they are not aboard!' % (fieldName, shipId))

            return None

        return ship

    def shipEnteredSphere(self, shipId, sphereId):
        ship = self._getReportedShip(shipId, 'shipEnteredSphere')
        if not ship:
            return

        if sphereId >= self.getNumSpheres():
            self.air.writeServerEvent('suspicious', avId=self.air.getAvatarIdFromSender(),
                issue='Sent shipEnteredSphere for invalid sphere %d!' % sphereId)

            return

        self.sphere2shipIds.setdefault(sphereId, set()).add(shipId)

    def shipExitedSphere(self, shipId, sphereId):
        ship = self._getReportedShip(shipId, 'shipExitedSphere')
        if not ship:
            return

        self.removeShipFromSphere(sphereId, shipId)

    def shipExitedBarrier(self, shipId):
        ship = self._getReportedShip(shipId, 'shipExitedBarrier')
        if not ship:
            return

        # the ship has sailed out of the island's deploy area, the deploy protection ends here...
        self.removeShipFromSpheres(shipId)
        self.unprotectShip(ship)

    def runShipDeployerFSM(self, fsmtype, avatar, *args, **kwargs):
        callback = kwargs.pop('callback', None)
        if avatar.doId in self.avatar2fsm:
            self.notify.debug('Failed to run ship deployer FSM for avatar %d, '
                'an inventory FSM is already running!' % avatar.doId)

            if callback:
                callback(False)

            return

        self.avatar2fsm[avatar.doId] = fsmtype(self.air, self, avatar, callback)
        self.avatar2fsm[avatar.doId].request('Start', *args, **kwargs)

    def deployShip(self, avatar, shipId, callback=None, preferredPos=None, allowSunk=False):
        self.runShipDeployerFSM(DeployShipFSM, avatar, shipId, preferredPos, allowSunk,
            callback=callback)
