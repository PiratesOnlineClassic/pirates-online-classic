from direct.directnotify.DirectNotifyGlobal import directNotify

from pirates.world.ClientAreaBuilderAI import ClientAreaBuilderAI
from pirates.leveleditor import ObjectList
from pirates.leveleditor import WorldDataGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.interact.DistributedSearchableContainerAI import DistributedSearchableContainerAI
from pirates.interact.DistributedInteractivePropAI import DistributedInteractivePropAI
from pirates.treasuremap.DistributedBuriedTreasureAI import DistributedBuriedTreasureAI
from pirates.treasuremap.DistributedSurfaceTreasureAI import DistributedSurfaceTreasureAI
from pirates.holiday.DistributedHolidayBonfireAI import DistributedHolidayBonfireAI
from pirates.holiday.DistributedHolidayPigAI import DistributedHolidayPigAI


class GameAreaBuilderAI(ClientAreaBuilderAI):
    notify = directNotify.newCategory('GameAreaBuilderAI')

    def __init__(self, air, parent):
        ClientAreaBuilderAI.__init__(self, air, parent)

        self.wantBuildingExteriors = config.GetBool('want-building-exteriors', True)
        self.wantDoorLocatorNodes = config.GetBool('want-door-locator-nodes', True)
        self.wantConnectorLocatorNodes = config.GetBool('want-connector-locator-nodes', True)
        self.wantConnectorTunnels = config.GetBool('want-connector-tunnels', True)
        self.wantSearchables = config.GetBool('want-searchables', True)
        self.wantSpawnNodes = config.GetBool('want-spawn-nodes', True)
        self.wantInteractives = config.GetBool('want-interactive-props', True)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        newObj = None
        if objType == 'Player Spawn Node':
            newObj = self.createPlayerSpawnNode(parent, parentUid, objKey, objectData)
        elif objType == 'Building Exterior' and self.wantBuildingExteriors:
            newObj = self.createBuildingExterior(parent, parentUid, objKey, objectData)
        elif objType == ObjectList.DOOR_LOCATOR_NODE and self.wantDoorLocatorNodes:
            newObj = self.createDoorLocatorNode(parent, parentUid, objKey, objectData)
        elif objType == ObjectList.LOCATOR_NODE and self.wantConnectorLocatorNodes:
            newObj = self.createConnectorLocatorNode(parent, parentUid, objKey, objectData)
        elif objType == ObjectList.CONNECTOR_TUNNEL and self.wantConnectorTunnels:
            newObj = self.createConnectorTunnel(parent, parentUid, objKey, objectData)
        elif objType == 'Searchable Container' and self.wantSearchables:
            newObj = self.createSearchableContainer(parent, parentUid, objKey, objectData)
        elif objType in ['Animal', 'Townsperson', 'Spawn Node', 'Dormant NPC Spawn Node', 'Skeleton', 'NavySailor', 'Creature']:
            newObj = self.air.enemySpawner.createObject(objType, objectData, parent, parentUid, objKey, dynamic)
        elif objType == 'Object Spawn Node' and self.wantSpawnNodes:
            newObj = self.createObjectSpawnNode(parent, parentUid, objKey, objectData)
        elif objType == 'Interactive Prop' and self.wantInteractives:
            newObj = self.createInteractiveProp(parent, parentUid, objKey, objectData)
        elif objType == 'Holiday Object' and self.wantInteractives:
            newObj = self.createHolidayProp(parent, parentUid, objKey, objectData)

        return newObj

    def createPlayerSpawnNode(self, parent, parentUid, objKey, objectData):
        from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
        from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI

        parent = self.parent.getParentObj()
        if isinstance(parent, DistributedGameAreaAI):
            parent = parent.getParentObj()

        if not parent or not isinstance(parent, DistributedInstanceBaseAI):
            self.notify.warning('Cannot setup player spawn point for %r!' % parent)
            return None

        # the index value is a string by default for some reason,
        # so we'll have to change the value type...
        index = objectData.get('Index')
        if index:
            index = int(index)

        x, y, z = objectData.get('Pos', (0, 0, 0))
        h, p, r = objectData.get('Hpr', (0, 0, 0))

        parent.addSpawnPt(self.parent.getUniqueId(), (x, y, z, h), index)

    def createBuildingExterior(self, parent, parentUid, objKey, objectData):
        from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
        from pirates.world.DistributedJailInteriorAI import DistributedJailInteriorAI

        parent = parent.getParentObj()
        if not parent:
            self.notify.warning('Cannot create building exterior %s, '
                'current parent %s, has no parent object!' % (objKey, parentUid))

            return

        interiorFile = objectData.get('File')
        if not interiorFile:
            self.notify.debug('Cannot create building exterior %s, '
                'no interior file found!' % objKey)

            return

        exteriorUid = objectData.get('ExtUid')
        if not exteriorUid:
            self.notify.warning('Cannot create building exterior %s, '
                'no exterior uid found!' % objKey)

            return

        modelPath = self.air.worldCreator.getModelPathFromFile(interiorFile)
        if not modelPath:
            self.notify.warning('Cannot create building exterior %s, '
                'no model path found for file %s!' % (objKey, interiorFile))

            return

        # create a new instance object that lays under the main world instance
        # this allows us to load the interior file data and set the correct values...
        parent = self.air.worldCreator.createWorldInstance({}, self.air.worldCreator.world, '', objKey, False)
        if 'jail' in objectData['Visual']['Model']:
            interior = DistributedJailInteriorAI(self.air)
            self.parent.setJailInterior(interior)
        else:
            interior = DistributedGAInteriorAI(self.air, True)

        interior.setUniqueId(exteriorUid)
        interior.setName(interiorFile)
        interior.setModelPath(modelPath)
        interior.setScale(objectData.get('Scale', (1, 1, 1)))
        parent.generateChildWithRequired(interior, self.air.allocateZone())

        # add the interior object to the list of objects by uid's,
        # as both the exterior uid and the object key so we can listen
        # in on uid callback events...
        parent.builder.addObject(interior)
        parent.builder.addObject(interior, uniqueId=objKey)

        objectList = objectData.get('Objects', {})
        if not objectList:
            exteriorLocatorNode = self.createDoorLocatorNode(self.parent, objKey, exteriorUid, objectData, wantTruePosHpr=False)
            interiorLocatorNode = interior.builder.createDoorLocatorNode(self.parent, objKey, objKey, objectData)
        else:
            self.air.worldCreator.loadObjectDict(objectList, self.parent, objKey, True)

        self.air.worldCreator.loadObjectsFromFile(interiorFile + '.py', interior)
        return interior

    def createDoorLocatorNode(self, parent, parentUid, objKey, objectData, wantTruePosHpr=True):
        from pirates.world.DistributedBuildingDoorAI import DistributedBuildingDoorAI

        parent = parent.getParentObj()
        if not parent:
            self.notify.warning('Cannot create door locator node %s, '
                'current parent %s, has no parent object!' % (objKey, parentUid))

            return

        interior = self.air.uidMgr.justGetMeMeObject(parentUid)
        if not interior or parentUid == self.parent.getUniqueId():
            self.notify.debug('Cannot create door locator node %s, '
                'interior not found!' % objKey)

            return

        doorLocatorNode = DistributedBuildingDoorAI(self.air)
        doorLocatorNode.setUniqueId(objKey)
        doorLocatorNode.setPos(objectData.get('Pos', (0, 0, 0)))
        doorLocatorNode.setHpr(objectData.get('Hpr', (0, 0, 0)))
        doorLocatorNode.setScale(objectData.get('Scale', (1, 1, 1)))
        doorLocatorNode.setBuildingUid(parentUid)
        doorLocatorNode.setInteriorId(interior.doId, interior.getUniqueId(), interior.parentId, interior.zoneId)

        if not interior.getExteriorFrontDoor():
            doorLocatorNode.setDoorIndex(0)
            interior.setExteriorFrontDoor(doorLocatorNode)
        else:
            doorLocatorNode.setDoorIndex(1)
            interior.setExteriorBackDoor(doorLocatorNode)

        if wantTruePosHpr:
            self.setObjectTruePosHpr(doorLocatorNode, objKey, parentUid, objectData)

        zoneId = self.parent.getZoneFromXYZ(doorLocatorNode.getPos())
        self.parent.generateChildWithRequired(doorLocatorNode, zoneId)
        self.addObject(doorLocatorNode)
        return doorLocatorNode

    def createConnectorLocatorNode(self, parent, parentUid, objKey, objectData):
        locatorName = objectData.get('Name', '')
        if 'exterior' not in locatorName:
            return

        self.air.worldCreator.locatorManager.addLocator(parentUid, objKey, objectData)

    def createConnectorTunnel(self, parent, parentUid, objKey, objectData):
        from pirates.world.DistributedGATunnelAI import DistributedGATunnelAI

        modelPath = objectData.get('Visual', {}).get('Model', '')
        if not modelPath:
            self.notify.warning('Failed to generate connector tunnel %s, '
                'no model path found!' % objKey)

            return

        objects = objectData.get('Objects', {})
        if not objects:
            return

        def createConnectorLocatorNode(objKey, objectData):
            locatorName = objectData.get('Name', '')
            if 'connector' not in locatorName:
                return

            otherLinkUid = self.air.worldCreator.linkManager.getOtherLinkUid(objKey)
            if not otherLinkUid:
                return

            otherLocator = self.air.worldCreator.locatorManager.getLocator(otherLinkUid)
            if not otherLocator:
                self.air.worldCreator.locatorManager.addLocatorCallback(otherLinkUid,
                    createConnectorLocatorNode, objKey, objectData)

                return

            otherLocatorData = otherLocator.objectData
            if not otherLocatorData:
                return

            gameArea = self.air.uidMgr.justGetMeMeObject(otherLocator.parentUid)
            if not gameArea:
                return

            instance = parent.getParentObj()
            if not instance:
                return

            self.air.worldCreator.connectorManager.addConnector(
                parentUid, objKey, objectData)

            locatorNode = DistributedGATunnelAI(self.air)
            locatorNode.setUniqueId(objKey)
            locatorNode.setModelPath(modelPath)
            locatorNode.setName(objectData['Name'])
            locatorNode.setNodeName(otherLocatorData['Name'])

            # get the other connectors UID which is located on the other
            # side or the other game area...
            connectorUids = list(objects.keys())
            if connectorUids.index(objKey) == 0:
                locatorNode.setOtherLinkUid(connectorUids[1])
            else:
                locatorNode.setOtherLinkUid(connectorUids[0])

            locatorNode.setPos(objectData.get('Pos', (0, 0, 0)))
            locatorNode.setHpr(objectData.get('Hpr', (0, 0, 0)))
            locatorNode.setScale(objectData.get('Scale', (1, 1, 1)))

            zoneId = gameArea.getZoneFromXYZ(locatorNode.getPos())
            gameArea.generateChildWithRequired(locatorNode, zoneId)
            gameArea.builder.addObject(locatorNode)

            # update the game area's links
            links = gameArea.getLinks()
            links.append(['', locatorNode.doId, '', locatorNode.parentId, locatorNode.zoneId, '', 0, 0])
            gameArea.b_setLinks(links)

            # update our locator node's links
            isExterior, exteriorUid, links = locatorNode.getLinks()
            links.append([locatorNode.getName(), gameArea.doId, gameArea.getUniqueId(), 0, 0,
                locatorNode.getNodeName(), instance.doId, gameArea.zoneId])

            locatorNode.b_setLinks('exterior' in locatorNode.getNodeName(), gameArea.getUniqueId(), links)

        def linkOtherLocatorNode(locatorNode, otherLocatorNode):
            gameArea = otherLocatorNode.getParentObj()
            if not gameArea:
                return

            instance = gameArea.getParentObj()
            if not instance:
                return

            # update our locator node's links
            isExterior, exteriorUid, links = locatorNode.getLinks()
            links.append([otherLocatorNode.getName(), gameArea.doId, gameArea.getUniqueId(), 0, 0,
                otherLocatorNode.getNodeName(), instance.doId, gameArea.zoneId])

            locatorNode.b_setLinks('exterior' in otherLocatorNode.getNodeName(), gameArea.getUniqueId(), links)

        def locatorNodeArrivedCallback(doId):
            locatorNode = self.air.doId2do.get(doId)
            if not locatorNode:
                return

            otherLocatorNode = self.air.uidMgr.justGetMeMeObject(
                locatorNode.getOtherLinkUid())

            if not otherLocatorNode:
                return

            # this locator node has finally arrived, attempt to link it...
            linkOtherLocatorNode(locatorNode, otherLocatorNode)
            linkOtherLocatorNode(otherLocatorNode, locatorNode)

        for objKey, objectData in objects.items():
            if objectData['Type'] == ObjectList.LOCATOR_NODE:
                self.air.uidMgr.addUidCallback(objKey, locatorNodeArrivedCallback)
                createConnectorLocatorNode(objKey, objectData)

    def createSearchableContainer(self, parent, parentUid, objKey, objectData):
        container = DistributedSearchableContainerAI(self.air)
        container.setUniqueId(objKey)
        container.setPos(objectData.get('GridPos', objectData.get('Pos', (0, 0, 0))))
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

    def createObjectSpawnNode(self, parent, parentUid, objKey, objectData):
        if objectData['Spawnables'] == 'Surface Treasure':
            spawnNode = DistributedSurfaceTreasureAI(self.air)
        else:
            spawnNode = DistributedBuriedTreasureAI(self.air)
            spawnNode.setStartingDepth(int(objectData.get('startingDepth', 10)))
            spawnNode.setCurrentDepth(spawnNode.getStartingDepth())

        spawnNode.setPos(objectData.get('GridPos', objectData.get('Pos', (0, 0, 0))))
        spawnNode.setHpr(objectData.get('Hpr', (0, 0, 0)))
        spawnNode.setScale(objectData.get('Scale', (1, 1, 1)))

        zoneId = self.parent.getZoneFromXYZ(spawnNode.getPos())
        parent.generateChildWithRequired(spawnNode, zoneId)
        self.parentObjectToCell(spawnNode, zoneId)
        self.addObject(spawnNode)
        return spawnNode

    def createInteractiveProp(self, parent, parentUid, objKey, objectData):
        prop = DistributedInteractivePropAI(self.air)
        prop.setUniqueId(objKey)
        prop.setPos(objectData.get('GridPos', objectData.get('Pos', (0, 0, 0))))
        prop.setHpr(objectData.get('Hpr', (0, 0, 0)))
        prop.setScale(objectData.get('Scale', (1, 1, 1)))

        prop.setModelPath(objectData['Visual']['Model'])
        prop.setInteractAble(objectData.get('interactAble', 'npc'))
        prop.setInteractType(objectData.get('interactType', 'stockade'))
        prop.setParentObjId(parent.doId)

        zoneId = self.parent.getZoneFromXYZ(prop.getPos())
        parent.generateChildWithRequired(prop, zoneId)
        self.parentObjectToCell(prop, zoneId)
        self.addObject(prop)
        return prop

    def createHolidayProp(self, parent, parentUid, objKey, objectData):
        propCls = None
        subType = objectData.get('SubType', 'Unknown')
        if subType == 'Roast Pig':
            propCls = DistributedHolidayPigAI
        elif subType == 'Bonfire':
            propCls = DistributedHolidayBonfireAI

        if not propCls:
            self.notify.warning('Unknown holiday prop type: %s' % subType)
            return None

        self.notify.debug('Spawning holiday object: %s' % propCls.__name__)
        prop = propCls(self.air)
        prop.setUniqueId(objKey)
        prop.setPos(objectData.get('GridPos', objectData.get('Pos', (0, 0, 0))))
        prop.setHpr(objectData.get('Hpr', (0, 0, 0)))
        prop.setScale(objectData.get('Scale', (1, 1, 1)))
        prop.setInteractRadius(float(objectData.get('Aggro Radius', 12.0)))
        prop.setActiveInteractMode(objectData.get('Interact Mode', 'All'))
        prop.setHoliday(objectData.get('Holiday', 'FoundersFeast'))

        zoneId = self.parent.getZoneFromXYZ(prop.getPos())
        parent.generateChildWithRequired(prop, zoneId)
        self.parentObjectToCell(prop, zoneId)
        self.addObject(prop)
        return prop
