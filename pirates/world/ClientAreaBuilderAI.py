from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.GridParent import GridParent
from pirates.leveleditor import ObjectList
from pirates.piratesbase import PiratesGlobals, PLocalizer

class ClientAreaBuilderAI(DirectObject):
    notify = directNotify.newCategory('ClientAreaBuilderAI')

    def __init__(self, air, parent):
        self.air = air
        self.parent = parent
        self.objectList = {}

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        newObj = None

        if objType == ObjectList.AREA_TYPE_ISLAND:
            newObj = self.__createIsland(objectData, parent, parentUid,
                objKey, dynamic)
        elif objType == ObjectList.AREA_TYPE_ISLAND_REGION:
            newObj = self.__createGameArea(objectData, parent, parentUid,
                objKey, dynamic)
        elif objType == ObjectList.AREA_TYPE_BUILDING_INTERIOR:
            newObj = self.__createInterior(objectData, parent, parentUid,
                objKey, dynamic)
        else:
            if not parent or not hasattr(parent, 'builder'):
                areaParent = self.air.worldCreator.world.uidMgr.justGetMeMeObject(
                    parentUid)

                if not areaParent:
                    return newObj
            else:
                areaParent = parent

            newObj = areaParent.builder.createObject(objType, objectData, parent,
                parentUid, objKey, dynamic)

        return newObj

    def parentObjectToCell(self, object, zoneId=None, parent=None):
        if not object:
            self.notify.warning('Failed to parent to cell for non-existant object!')
            return

        parent = parent or self.parent

        if zoneId is None:
            zoneId = parent.getZoneFromXYZ(object.getPos())

        cell = GridParent.getCellOrigin(parent, zoneId)
        originalPos = object.getPos()

        object.reparentTo(cell)
        object.setPos(parent, originalPos)

        self.broadcastObjectPosition(object)

    def __createIsland(self, objectData, parent, parentUid, objKey, dynamic):
        from pirates.world.DistributedIslandAI import DistributedIslandAI

        worldIsland = self.air.worldCreator.getIslandWorldDataByUid(objKey)

        island = DistributedIslandAI(self.air)
        island.setUniqueId(objKey)
        island.setName(PLocalizer.LocationNames.get(objKey, ''))
        island.setModelPath(worldIsland['Visual']['Model'])
        island.setPos(worldIsland.get('Pos', (0, 0, 0)))
        island.setHpr(worldIsland.get('Hpr', (0, 0, 0)))
        island.setScale(objectData.get('Scale', (1, 1, 1)))
        island.setUndockable(objectData.get('Undockable', False))

        if 'Objects' in worldIsland:
            for obj in worldIsland['Objects'].values():
                if obj['Type'] == 'LOD Sphere':
                    island.setZoneSphereSize(*obj['Radi'])

        self.parent.generateChildWithRequired(island, PiratesGlobals.IslandAvailableZoneStart)
        self.addObject(island)

        return island

    def __createGameArea(self, objectData, parent, parentUid, objKey, dynamic):
        from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI

        gameArea = DistributedGAInteriorAI(self.air)
        gameArea.setUniqueId(objKey)
        gameArea.setName(PLocalizer.LocationNames.get(objKey, ''))
        gameArea.setModelPath(objectData['Visual']['Model'])
        gameArea.setPos(objectData.get('Pos', (0, 0, 0)))
        gameArea.setHpr(objectData.get('Hpr', (0, 0, 0)))
        gameArea.setScale(objectData.get('Scale', (1, 1, 1)))

        self.parent.generateChildWithRequired(gameArea, self.air.allocateZone())
        self.addObject(gameArea)

        return gameArea

    def __createInterior(self, objectData, parent, parentUid, objKey, dynamic):
        from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI

        interior = DistributedGAInteriorAI(self.air)
        interior.setUniqueId(objKey)
        interior.setName(PLocalizer.LocationNames.get(objKey, ''))
        interior.setModelPath(objectData['Visual']['Model'])
        interior.setPos(objectData.get('Pos', (0, 0, 0)))
        interior.setHpr(objectData.get('Hpr', (0, 0, 0)))
        interior.setScale(objectData.get('Scale', (1, 1, 1)))

        self.parent.generateChildWithRequired(interior, self.air.allocateZone())
        self.addObject(interior)

        return interior

    def addObject(self, object, uniqueId=None):
        if not object:
            self.notify.warning('Cannot add an invalid object!')
            return

        if object.doId in self.objectList:
            self.notify.warning('Cannot add an already existing object %d!' % object.doId)
            return

        self.parent.uidMgr.addUid(uniqueId or object.getUniqueId(), object.doId)
        self.objectList[object.doId] = object

    def removeObject(self, object, uniqueId=None):
        if not object:
            self.notify.warning('Cannot remove an invalid object!')
            return

        if object.doId not in self.objectList:
            self.notify.warning('Cannot remove a non-existant object %d!' % object.doId)
            return

        self.parent.uidMgr.removeUid(uniqueId or object.getUniqueId())
        del self.objectList[object.doId]

    def getObject(self, doId=None, uniqueId=None):
        for object in self.objectList:
            if object.doId == doId or object.getUniqueId() == uniqueId:
                return object

        return None

    def deleteObject(self, doId):
        object = self.objectList.get(doId)

        if not object:
            self.notify.warning('Cannot delete an invalid object!')
            return

        self.removeObject(object)
        object.requestDelete()

    def broadcastObjectPosition(self, object):
        if not object:
            self.notify.warning('Failed to broadcast position for non-existant object!')
            return

        object.d_setPos(*object.getPos())
        object.d_setHpr(*object.getHpr())
