from panda3d.core import *

from direct.showbase.DirectObject import DirectObject
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.GridParent import GridParent

from pirates.quest.QuestConstants import LocationIds
from pirates.leveleditor import ObjectList
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.world import WorldGlobals


class ClientAreaBuilderAI(DirectObject):
    notify = directNotify.newCategory('ClientAreaBuilderAI')

    def __init__(self, air, parent):
        self.air = air
        self.parent = parent
        self.objectList = {}

    def getIslands(self):
        from pirates.world.DistributedIslandAI import DistributedIslandAI
        return self.findObjectsOfClass(DistributedIslandAI)

    def findObjectsOfClass(self, objectClass):
        objects = []
        for object in self.objectList.values():
            if isinstance(object, objectClass):
                objects.append(object)

        return objects

    def addObject(self, object, uniqueId=None):
        self.air.uidMgr.addUid(uniqueId or object.getUniqueId(), object.doId)
        self.objectList[object.doId] = object

    def removeObject(self, object, uniqueId=None):
        self.air.uidMgr.removeUid(uniqueId or object.getUniqueId())
        del self.objectList[object.doId]

    def getObject(self, doId=None, uniqueId=None):
        for object in self.objectList.values():
            if object.doId == doId or object.getUniqueId() == uniqueId:
                return object

        return None

    def deleteObject(self, doId):
        object = self.objectList.get(doId)
        if not object:
            return

        self.removeObject(object)
        object.requestDelete()

    def broadcastObjectPosition(self, object):
        if not object:
            return

        object.d_setPos(*object.getPos())
        object.d_setHpr(*object.getHpr())

    def parentObjectToCell(self, object, zoneId=None, parent=None):
        if not object:
            return

        parent = parent or self.parent
        if zoneId is None:
            zoneId = parent.getZoneFromXYZ(object.getPos())

        cell = GridParent.getCellOrigin(parent, zoneId)
        originalPos = object.getPos()

        object.reparentTo(cell)
        object.setPos(parent, originalPos)

        self.broadcastObjectPosition(object)

    def isChildObject(self, objKey, parentUid):
        return self.air.worldCreator.getObjectParentUid(objKey) != parentUid

    def setObjectTruePosHpr(self, object, objKey, parentUid, objectData):
        objectPos = objectData.get('Pos', Point3(0, 0, 0))
        objectHpr = objectData.get('Hpr', Point3(0, 0, 0))

        if not self.isChildObject(objKey, parentUid):
            object.setPos(objectPos)
            object.setHpr(objectHpr)
            return object

        parentData = self.air.worldCreator.getObjectDataByUid(parentUid)
        if parentData['Type'] == 'Island':
            object.setPos(objectPos)
            object.setHpr(objectHpr)
            return object

        parentObject = NodePath('psuedo-%s' % parentUid)
        parentObject.setPos(parentData.get('Pos', Point3(0, 0, 0)))
        parentObject.setHpr(parentData.get('Hpr', Point3(0, 0, 0)))

        object.setPos(parentObject, objectPos)
        object.setHpr(parentObject, objectHpr)

        return object

    def getObjectTruePosAndParent(self, objKey, parentUid, objectData):
        if self.isChildObject(objKey, parentUid):
            parentData = self.air.worldCreator.getObjectDataByUid(parentUid)
            if parentData['Type'] == 'Island':
                return objectData.get('Pos'), NodePath('')

            parentObject = NodePath('psuedo-%s' % parentUid)
            if not 'GridPos' in objectData:
                parentObject.setPos(parentData.get('Pos', Point3(0, 0, 0)))

            parentObject.setHpr(parentData.get('Hpr', Point3(0, 0, 0)))
            objectPos = objectData.get('GridPos', objectData.get('Pos', Point3(0, 0, 0)))
            return objectPos, parentObject

        return objectData.get('Pos'), NodePath('')

    def getIslandGridSize(self, objKey):
        if objKey == LocationIds.PORT_ROYAL_ISLAND:
            gridSize = WorldGlobals.LARGE_ISLAND_GRID_SIZE
        elif objKey == LocationIds.TORTUGA_ISLAND:
            gridSize = WorldGlobals.MED_ISLAND_GRID_SIZE
        elif objKey == LocationIds.DEL_FUEGO_ISLAND:
            gridSize = WorldGlobals.LARGE_ISLAND_GRID_SIZE
        elif objKey == LocationIds.ANVIL_ISLAND:
            gridSize = WorldGlobals.ISLAND_GRID_SIZE
        elif objKey == LocationIds.DRIFTWOOD_ISLAND:
            gridSize = WorldGlobals.MED_ISLAND_GRID_SIZE
        elif objKey == LocationIds.RUMRUNNER_ISLE:
            gridSize = WorldGlobals.MED_ISLAND_GRID_SIZE
        elif objKey == LocationIds.PERDIDA_PORT:
            gridSize = WorldGlobals.ISLAND_GRID_SIZE
        elif objKey == LocationIds.CUBA_ISLAND:
            gridSize = WorldGlobals.MED_ISLAND_GRID_SIZE
        elif objKey == LocationIds.KINGSHEAD_ISLAND:
            gridSize = WorldGlobals.LARGE_ISLAND_GRID_SIZE
        elif objKey == LocationIds.ISLA_CANGREJOS:
            gridSize = WorldGlobals.MED_ISLAND_GRID_SIZE
        elif objKey == LocationIds.CUTTHROAT_ISLAND:
            gridSize = WorldGlobals.MED_ISLAND_GRID_SIZE
        elif objKey == LocationIds.OUTCAST_ISLE:
            gridSize = WorldGlobals.ISLAND_GRID_SIZE
        elif objKey == LocationIds.ISLA_TORMENTA:
            gridSize = WorldGlobals.ISLAND_GRID_SIZE
        else:
            gridSize = WorldGlobals.ISLAND_GRID_SIZE

        return gridSize

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        newObj = None

        if objType == ObjectList.AREA_TYPE_ISLAND:
            newObj = self.createIsland(objectData, parent, parentUid, objKey, dynamic)
        else:
            if not parent or not hasattr(parent, 'builder'):
                parent = self.air.uidMgr.justGetMeMeObject(parentUid)

                if not parent or parent == self.parent:
                    return newObj

            newObj = parent.builder.createObject(objType, objectData, parent,
                parentUid, objKey, dynamic)

        return newObj

    def createIsland(self, objectData, parent, parentUid, objKey, dynamic):
        from pirates.world.DistributedIslandAI import DistributedIslandAI
        islandWorldData = self.air.worldCreator.getIslandWorldDataByUid(objKey)

        if not islandWorldData:
            self.notify.warning('Failed to generate island: %s' % objKey)
            return

        (x, y, z) = islandWorldData.get('Pos', (0, 0, 0))
        (h, p, r) = islandWorldData.get('Hpr', (0, 0, 0))

        island = DistributedIslandAI(self.air, self.getIslandGridSize(objKey))
        island.setUniqueId(objKey)
        island.setName(PLocalizer.LocationNames.get(objKey, ''))
        island.setFileName(islandWorldData.get('File', ''))
        island.setIslandTransform(x, y, z, h)
        island.setModelPath(islandWorldData['Visual']['Model'])
        island.setScale(objectData.get('Scale', (1, 1, 1)))
        island.setUndockable(objectData.get('Undockable', False))

        if 'Objects' in islandWorldData:
            for obj in islandWorldData['Objects'].values():
                if obj['Type'] == 'LOD Sphere':
                    sphereCenter = obj['Pos']
                    island.setZoneSphereSize(*obj['Radi'])
                    island.setZoneSphereCenter(sphereCenter[0], sphereCenter[1])

        self.notify.debug('Generated island %s (%s)' % (island.getName(), objKey))
        self.parent.generateChildWithRequired(island, PiratesGlobals.IslandAvailableZoneStart)
        self.addObject(island)
        self.air.worldCreator.linkManager.registerLinkData(objKey)
        self.air.worldCreator.movementLinkManager.registerMovementLinkData(objKey)
        return island
