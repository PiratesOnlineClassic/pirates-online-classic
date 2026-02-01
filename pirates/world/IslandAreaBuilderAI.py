from direct.directnotify.DirectNotifyGlobal import directNotify

from pirates.world.GameAreaBuilderAI import GameAreaBuilderAI
from pirates.leveleditor import ObjectList
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.interact.DistributedSearchableContainerAI import DistributedSearchableContainerAI
from pirates.world.DistributedDinghyAI import DistributedDinghyAI
from pirates.treasuremap.DistributedBuriedTreasureAI import DistributedBuriedTreasureAI
from pirates.treasuremap.DistributedSurfaceTreasureAI import DistributedSurfaceTreasureAI


class IslandAreaBuilderAI(GameAreaBuilderAI):
    notify = directNotify.newCategory('IslandAreaBuilderAI')

    def __init__(self, air, parent):
        GameAreaBuilderAI.__init__(self, air, parent)

        self.wantDinghys = config.GetBool('want-dinghys', True)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        if objType == ObjectList.AREA_TYPE_ISLAND_REGION:
            newObj = self.createGameArea(objectData, parent, parentUid, objKey, dynamic)
        elif objType == 'Dinghy' and self.wantDinghys:
            newObj = self.createDinghy(parent, parentUid, objKey, objectData)
        else:
            newObj = GameAreaBuilderAI.createObject(self, objType, objectData, parent, parentUid,
                objKey, dynamic, parentIsObj, fileName, actualParentObj)

        return newObj

    def createGameArea(self, objectData, parent, parentUid, objKey, dynamic):
        from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI

        parent = self.parent.getParentObj()
        if not parent:
            return

        areaName = PLocalizer.LocationNames.get(objKey, '')
        areaFile = objectData.get('File')
        if not areaFile:
            self.notify.warning('Cannot create island game area: %s with uniqueId: %s, '
                'no area file found!' % (areaName, objKey))

            return

        gameArea = DistributedGAInteriorAI(self.air)
        gameArea.setUniqueId(objKey)
        gameArea.setName(areaName)
        gameArea.setFileName(areaFile)
        gameArea.setModelPath(objectData['Visual']['Model'])

        # create a new instance object that lays under the main world instance
        # this allows us to load the game area file data and set the correct values...
        parent = self.air.worldCreator.createWorldInstance({}, self.air.worldCreator.world, '', objKey, False)
        parent.generateChildWithRequired(gameArea, self.air.allocateZone())
        parent.builder.addObject(gameArea)
        self.air.worldCreator.linkManager.registerLinkData(objKey)

        def createConnectorLocatorNode(objKey, objectData):
            locatorName = objectData.get('Name', '')
            if 'interior' not in locatorName:
                return

            self.air.worldCreator.locatorManager.addLocator(gameArea.getUniqueId(), objKey, objectData)

        for objKey, objectData in objectData.get('Objects', {}).items():
            if objectData['Type'] == ObjectList.LOCATOR_NODE:
                createConnectorLocatorNode(objKey, objectData)

        self.air.worldCreator.loadObjectsFromFile(areaFile + '.py', gameArea)
        return gameArea

    def createDinghy(self, parent, parentUid, objKey, objectData):
        dinghy = DistributedDinghyAI(self.air)
        dinghy.setPos(objectData.get('Pos', (0, 0, 0)))
        dinghy.setHpr(objectData.get('Hpr', (0, 0, 0)))
        dinghy.setInteractRadius(float(objectData.get('Aggro Radius', 25)))

        zoneId = self.parent.getZoneFromXYZ(dinghy.getPos())
        parent.generateChildWithRequired(dinghy, zoneId)
        self.parentObjectToCell(dinghy, zoneId)
        self.addObject(dinghy)
        return dinghy
