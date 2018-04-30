from pirates.world.ClientAreaBuilderAI import ClientAreaBuilderAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.leveleditor import ObjectList
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.interact.DistributedSearchableContainerAI import DistributedSearchableContainerAI
from pirates.treasuremap.DistributedBuriedTreasureAI import DistributedBuriedTreasureAI
from pirates.treasuremap.DistributedSurfaceTreasureAI import DistributedSurfaceTreasureAI

class GameAreaBuilderAI(ClientAreaBuilderAI):
    notify = directNotify.newCategory('GameAreaBuilderAI')

    def __init__(self, air, parent):
        ClientAreaBuilderAI.__init__(self, air, parent)

        self.wantBuildingExteriors = config.GetBool('want-building-exteriors', True)
        self.wantDoorLocatorNodes = config.GetBool('want-door-locator-nodes', True)
        self.wantSearchables = config.GetBool('want-searchables', True)
        self.wantSpawnNodes = config.GetBool('want-spawn-nodes', True)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        newObj = None

        if objType == 'Building Exterior' and self.wantBuildingExteriors:
            newObj = self.__createBuildingExterior(parent, parentUid, objKey, objectData)
        elif objType == ObjectList.DOOR_LOCATOR_NODE and self.wantDoorLocatorNodes:
            newObj = self.__createDoorLocatorNode(parent, parentUid, objKey, objectData)
        elif objType == 'Searchable Container' and self.wantSearchables:
            newObj = self.__createSearchableContainer(parent, parentUid, objKey, objectData)
        elif objType in ['Animal', 'Townsperson', 'Spawn Node', 'Dormant NPC Spawn Node', 'Skeleton', 'NavySailor', 'Creature']:
            newObj = self.air.enemySpawner.createObject(objType, objectData, parent, parentUid, objKey, dynamic)
        elif objType == 'Object Spawn Node' and self.wantSpawnNodes:
            newObj = self.__createObjectSpawnNode(parent, parentUid, objKey, objectData)

        return newObj

    def __createBuildingExterior(self, parent, parentUid, objKey, objectData):
        from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
        from pirates.world.DistributedJailInteriorAI import DistributedJailInteriorAI

        parent = parent.getParentObj()

        if not parent:
            self.notify.warning('Cannot create building exterior %s, current parent %s, has no parent object!' % (
                objKey, parentUid))

            return

        exteriorUid = objectData.get('ExtUid')

        if not exteriorUid:
            self.notify.warning('Cannot create building exterior %s, no exterior uid found!' % (
                objKey))

            return

        interiorFile = objectData.get('File')

        if not interiorFile:
            self.notify.debug('Cannot create building exterior %s, no interior file found!' % (
                objKey))

            return

        modelPath = self.air.worldCreator.getModelPathFromFile(interiorFile)

        if not modelPath:
            self.notify.warning('Cannot create building exterior %s, no model path found for file %s!' % (
                objKey, interiorFile))

            return

        interiorClass = DistributedJailInteriorAI if 'Jail' in interiorFile else DistributedGAInteriorAI
        interior = interiorClass(self.air)
        interior.setUniqueId(exteriorUid)
        interior.setName(PLocalizer.LocationNames.get(objKey, ''))
        interior.setModelPath(modelPath)
        interior.setPos(objectData.get('Pos', (0, 0, 0)))
        interior.setHpr(objectData.get('Hpr', (0, 0, 0)))
        interior.setScale(objectData.get('Scale', (1, 1, 1)))

        parent.generateChildWithRequired(interior, self.air.allocateZone())
        parent.builder.addObject(interior, uniqueId=objKey)

        self.air.worldCreator.loadObjectDict(objectData.get('Objects', {}), self.parent, objKey, True)
        self.air.worldCreator.loadObjectsFromFile(interiorFile + '.py', interior)

        return interior

    def __createDoorLocatorNode(self, parent, parentUid, objKey, objectData):
        from pirates.world.DistributedBuildingDoorAI import DistributedBuildingDoorAI

        parent = parent.getParentObj()

        if not parent:
            self.notify.warning('Cannot create door locator node %s, current parent %s, has no parent object!' % (
                objKey, parentUid))

            return

        interior = parent.uidMgr.justGetMeMeObject(parentUid)

        if not interior or parentUid == self.parent.getUniqueId():
            self.notify.debug('Cannot create door locator node %s, interior not found!' % (
                objKey))

            return

        doorLocatorNode = DistributedBuildingDoorAI(self.air)
        doorLocatorNode.setUniqueId(objKey)
        doorLocatorNode.setPos(objectData.get('Pos', (0, 0, 0)))
        doorLocatorNode.setHpr(objectData.get('Hpr', (0, 0, 0)))
        doorLocatorNode.setScale(objectData.get('Scale', (1, 1, 1)))
        doorLocatorNode.setBuildingUid(parentUid)
        doorLocatorNode.setInteriorId(interior.doId, interior.getUniqueId(),
            interior.parentId, interior.zoneId)

        if not interior.getExteriorFrontDoor():
            interior.setExteriorFrontDoor(doorLocatorNode)
        else:
            doorLocatorNode.setDoorIndex(1)
            interior.setExteriorBackDoor(doorLocatorNode)

        self.setObjectTruePosHpr(doorLocatorNode, objKey, parentUid, objectData)

        zoneId = self.parent.getZoneFromXYZ(doorLocatorNode.getPos())
        self.parent.generateChildWithRequired(doorLocatorNode, zoneId)
        self.parentObjectToCell(doorLocatorNode, zoneId)

        self.addObject(doorLocatorNode)

        return doorLocatorNode

    def __createSearchableContainer(self, parent, parentUid, objKey, objectData):
        container = DistributedSearchableContainerAI(self.air)
        container.setUniqueId(objKey)
        container.setPos(objectData.get('Pos', (0, 0, 0)))
        container.setHpr(objectData.get('Hpr', (0, 0, 0)))
        container.setScale(objectData.get('Scale', (1, 1, 1)))
        container.setType(objectData.get('type', 'Crate'))

        if 'Visual' in objectData and 'Color' in objectData['Visual']:
            container.setContainerColor(objectData['Visual'].get('Color', (1.0, 1.0, 1.0, 1.0)))

        container.setSearchTime(float(objectData.get('searchTime', '6.0')))
        container.setSphereScale(float(objectData.get('Aggro Radius', 1.0)))

        zoneId = self.parent.getZoneFromXYZ(container.getPos())
        parent.generateChildWithRequired(container, zoneId)
        self.parentObjectToCell(container, zoneId)

        self.addObject(container)

        return container

    def __createObjectSpawnNode(self, parent, parentUid, objKey, objectData):
        spawnClass = DistributedSurfaceTreasureAI if objectData['Spawnables'] == 'Surface Treasure' \
            else DistributedBuriedTreasureAI

        spawnNode = spawnClass(self.air)

        spawnNode.setPos(objectData.get('Pos', (0, 0, 0)))
        spawnNode.setHpr(objectData.get('Hpr', (0, 0, 0)))
        spawnNode.setScale(objectData.get('Scale', (1, 1, 1)))
        spawnNode.setStartingDepth(int(objectData.get('startingDepth', 10)))
        spawnNode.setCurrentDepth(spawnNode.getStartingDepth())

        zoneId = self.parent.getZoneFromXYZ(spawnNode.getPos())
        parent.generateChildWithRequired(spawnNode, zoneId)
        self.parentObjectToCell(spawnNode, zoneId)

        self.addObject(spawnNode)

        return spawnNode
