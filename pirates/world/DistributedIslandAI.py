from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.directnotify import DirectNotifyGlobal

from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.battle.Teamable import Teamable
from pirates.world import WorldGlobals
from pirates.world.IslandAreaBuilderAI import IslandAreaBuilderAI
from pirates.piratesbase import PiratesGlobals
from pirates.treasuremap.DistributedTreasureMapInstanceAI import DistributedTreasureMapInstanceAI
from pirates.world.DistributedShipDeployerAI import DistributedShipDeployerAI
from pirates.ship.DistributedShipAI import DistributedShipAI


class DistributedIslandAI(DistributedCartesianGridAI, DistributedGameAreaAI, Teamable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedIslandAI')

    def __init__(self, air, gridSize):
        startingZone = WorldGlobals.ISLAND_GRID_STARTING_ZONE
        cellWidth = WorldGlobals.ISLAND_CELL_SIZE
        gridRadius = WorldGlobals.ISLAND_GRID_RADIUS

        DistributedCartesianGridAI.__init__(self, air, startingZone, gridSize, gridRadius, cellWidth, style='CartesianStated')
        DistributedGameAreaAI.__init__(self, air)
        Teamable.__init__(self)

        self.islandTransform = [0, 0, 0, 0]
        self.sphereRadii = [0, 0, 0]
        self.sphereCenter = [0, 0]
        self.islandModel = ''
        self.undockable = False
        self.collisionSpheres = []
        self.feastFireEnabled = False

        self.shipDeployer = None
        self.builder = IslandAreaBuilderAI(self.air, self)

    def announceGenerate(self):
        DistributedCartesianGridAI.announceGenerate(self)
        DistributedGameAreaAI.announceGenerate(self)

    def generate(self):
        DistributedCartesianGridAI.generate(self)
        DistributedGameAreaAI.generate(self)

        self.accept('HolidayStarted', self.holidayStart)
        self.accept('HolidayEnded', self.holidayEnded)

        # Process startup holidays
        for holidayId in self.air.newsManager.holidayList:
            self.holidayStart(holidayId)

        self.shipDeployer = DistributedShipDeployerAI(self.air)
        maxRadius = self.sphereRadii[2]
        minRadius = self.sphereRadii[1]
        spacing = maxRadius - minRadius

        self.shipDeployer.setMaxRadius(maxRadius)
        self.shipDeployer.setMinRadius(minRadius)
        self.shipDeployer.setSpacing(spacing)

        self.generateChildWithRequired(self.shipDeployer, PiratesGlobals.IslandShipDeployerZone)

    def holidayStart(self, holidayId):
        if self.uniqueId == '1156207188.95dzlu' and holidayId == PiratesGlobals.FOUNDERSFEAST:
            if self.getFeastFireEnabled():
                return

            self.b_setFeastFireEnabled(True)

    def holidayEnded(self, holidayId):
        if self.uniqueId == '1156207188.95dzlu' and holidayId == PiratesGlobals.FOUNDERSFEAST:
            if not self.getFeastFireEnabled():
                return

            self.b_setFeastFireEnabled(False)

    def setIslandTransform(self, x, y, z, h):
        self.islandTransform = [x, y, z, h]

    def d_setIslandTransform(self, x, y, z, h):
        self.sendUpdate('setIslandTransform', [x, y, z, h])

    def b_setIslandTransform(self, x, y, z, h):
        self.setIslandTransform(x, y, z, h)
        self.d_setIslandTransform(x, y, z, h)

    def getIslandTransform(self):
        return self.islandTransform

    def setZoneSphereSize(self, rad0, rad1, rad2):
        self.sphereRadii = [rad0, rad1, rad2]

    def d_setZoneSphereSize(self, rad0, rad1, rad2):
        self.sendUpdate('setZoneSphereSize', [rad0, rad1, rad2])

    def b_setZoneSphereSize(self, rad0, rad1, rad2):
        self.setZoneSphereSize(rad0, rad1, rad2)
        self.d_setZoneSphereSize(rad0, rad1, rad2)

    def getZoneSphereSize(self):
        return self.sphereRadii

    def setZoneSphereCenter(self, x, y):
        self.sphereCenter = [x, y]

    def d_setZoneSphereCenter(self, x, y):
        self.sendUpdate('setZoneSphereCenter', [x, y])

    def b_setZoneSphereCenter(self, x, y):
        self.setZoneSphereCenter(x, y)
        self.d_setZoneSphereCenter(x, y)

    def getZoneSphereCenter(self):
        return self.sphereCenter

    def setIslandModel(self, islandModel):
        self.islandModel = islandModel

    def d_setIslandModel(self, islandModel):
        self.sendUpdate('setIslandModel', [islandModel])

    def b_setIslandModel(self, islandModel):
        self.setIslandModel(islandModel)
        self.d_setIslandModel(islandModel)

    def getIslandModel(self):
        return self.islandModel

    def setUndockable(self, undockable):
        self.undockable = undockable

    def d_setUndockable(self, undockable):
        self.sendUpdate('setUndockable', [undockable])

    def b_setUndockable(self, undockable):
        self.setUndockable(undockable)
        self.d_setUndockable(undockable)

    def getUndockable(self):
        return self.undockable

    def setPortCollisionSpheres(self, collisionSpheres):
        self.collisionSpheres = collisionSpheres

    def d_setPortCollisionSpheres(self, collisionSpheres):
        self.sendUpdate('setPortCollisionSpheres', [collisionSpheres])

    def b_setPortCollisionSpheres(self, collisionSpheres):
        self.setPortCollisionSpheres(collisionSpheres)
        self.d_setPortCollisionSpheres(collisionSpheres)

    def getPortCollisionSpheres(self):
        return self.collisionSpheres

    def requestEntryToIsland(self):
        pass

    def d_deniedEntryToIsland(self, avatarId):
        self.sendUpdateToAvatarId(avatarId, 'deniedEntryToIsland', [])

    def setFeastFireEnabled(self, feastFireEnabled):
        self.feastFireEnabled = feastFireEnabled

    def d_setFeastFireEnabled(self, feastFireEnabled):
        self.sendUpdate('setFeastFireEnabled', [feastFireEnabled])

    def b_setFeastFireEnabled(self, feastFireEnabled):
        self.setFeastFireEnabled(feastFireEnabled)
        self.d_setFeastFireEnabled(feastFireEnabled)

    def getFeastFireEnabled(self):
        return self.feastFireEnabled

    def delete(self):
        self.ignore('HolidayStarted')
        self.ignore('HolidayEnded')

        DistributedCartesianGridAI.delete(self)
        DistributedGameAreaAI.delete(self)
