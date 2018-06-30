from panda3d.core import *
from direct.distributed.DistributedCartesianGrid import DistributedCartesianGrid
from direct.showbase.PythonUtil import report
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.seapatch.Reflection import Reflection
from pirates.seapatch.SeaPatch import SeaPatch
from pirates.world.OceanGridBase import OceanGridBase
from pirates.world import WorldGlobals


class DistributedOceanGrid(DistributedCartesianGrid, OceanGridBase):

    def __init__(self, cr):
        DistributedCartesianGrid.__init__(self, cr)
        OceanGridBase.__init__(self)
        self.islandGrids = {}

    def generate(self):
        DistributedCartesianGrid.generate(self)
        r = Reflection.getGlobalReflection()
        saintPatricksDay = base.saintPatricksDay
        water = SeaPatch(self, reflection=r, saintPatricksDay=saintPatricksDay)
        water.loadSeaPatchFile('out.spf')
        self.water = water
        self.setupShipBarrier()

    def setLocation(self, parentId, zoneId):
        DistributedCartesianGrid.setLocation(self, parentId, zoneId)
        world = self.cr.doId2do.get(self.parentId)
        if parentId not in (0, self.cr.getGameDoId()):
            pass

    def disable(self):
        DistributedCartesianGrid.disable(self)
        if hasattr(base, 'localAvatar') and base.localAvatar is not None:
            self.removeObjectFromGrid(base.localAvatar)
        self.shipBarrierNP.removeNode()
        self.ignore('enter' + self.cName)

    def delete(self):
        self.water.delete()
        self.water = None
        DistributedCartesianGrid.delete(self)

    def setupShipBarrier(self):
        worldRadius = WorldGlobals.OCEAN_GRID_SIZE * WorldGlobals.OCEAN_CELL_SIZE / 2.0 - 50
        shipBarrier = CollisionInvSphere(0.0, 0.0, 0.0, worldRadius)
        shipBarrier.setTangible(1)
        self.cName = self.uniqueName('ShipBarrier')
        cSphereNode = CollisionNode(self.cName)
        cSphereNode.setIntoCollideMask(PiratesGlobals.ShipCollideBitmask)
        cSphereNode.addSolid(shipBarrier)
        self.shipBarrierNP = self.attachNewNode(cSphereNode)
        self.accept('enter' + self.cName, self.handleEdgeOfWorld)

    def handleEdgeOfWorld(self, event):
        localAvatar.guiMgr.messageStack.addTextMessage(
            PLocalizer.EdgeOfWorldWarning)

    def reparentLocalAvatarToWorld(self, parent=None):
        if parent:
            parent.addObjectToGrid(base.localAvatar)
        elif len(self.islandGrids) > 0:
            islandIds = self.islandGrids.keys()
            island = self.islandGrids[islandIds[0]]
            island.addObjectToGrid(base.localAvatar)
        else:
            self.addObjectToGrid(base.localAvatar)

    oceanAreas = {}

    def addOceanArea(self, pos1, pos2, name, uid):
        ul = Point3(
            min(pos2.getX(), pos1.getX()), max(pos2.getY(), pos1.getY()), 0)
        lr = Point3(
            max(pos2.getX(), pos1.getX()), min(pos2.getY(), pos1.getY()), 0)
        if name in self.oceanAreas:
            pos1, pos2 = self.oceanAreas[name][0:2]
            ul = Point3(
                min(ul.getX(), pos1.getX()), max(ul.getY(), pos1.getY()), 0)
            lr = Point3(
                max(lr.getX(), pos2.getX()), min(lr.getY(), pos2.getY()), 0)
        self.oceanAreas[name] = [ul, lr, uid]

    def addOceanAreasToMap(self):
        mapPage = base.localAvatar.guiMgr.mapPage
        areaNames = self.oceanAreas.keys()
        for name in areaNames:
            mapPage.addOceanArea(name, self.oceanAreas[name][2],
                                 self.oceanAreas[name][0],
                                 self.oceanAreas[name][1])

    def addIslandGrid(self, island):
        self.islandGrids[island.doId] = island
        self.updateLocalAvatarParent(island)

    def removeIslandGrid(self, island):
        islandId = island.doId
        if self.islandGrids.get(islandId):
            del self.islandGrids[islandId]
        self.updateLocalAvatarParent()

    def updateLocalAvatarParent(self, parent=None):
        if base.localAvatar.ship:
            return
        self.reparentLocalAvatarToWorld(parent)

    def turnOff(self):
        DistributedCartesianGrid.turnOff(self)
        self.stash()
        self.water.disable()

    def turnOn(self, av):
        DistributedCartesianGrid.turnOn(self, av)
        self.unstash()
        self.water.enable()

    @report(
        types=['deltaStamp', 'avLocation', 'args'],
        dConfigParam=['want-connector-report', 'want-shipboard-report'])
    def stopProcessVisibility(self, *args, **kw):
        DistributedCartesianGrid.stopProcessVisibility(self, *args, **kw)

    def getTeleportDestPosH(self, index=0):
        return (0, 0, 0, 0)
