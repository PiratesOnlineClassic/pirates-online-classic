from pirates.world.ClientAreaBuilderAI import ClientAreaBuilderAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.interact.DistributedSearchableContainerAI import DistributedSearchableContainerAI
from pirates.treasuremap.DistributedBuriedTreasureAI import DistributedBuriedTreasureAI
from pirates.treasuremap.DistributedSurfaceTreasureAI import DistributedSurfaceTreasureAI

class GameAreaBuilderAI(ClientAreaBuilderAI):
    notify = directNotify.newCategory('GameAreaBuilderAI')

    def __init__(self, air, parent):
        ClientAreaBuilderAI.__init__(self, air, parent)

        self.wantSearchables = config.GetBool('want-searchables', True)
        self.wantSpawnNodes = config.GetBool('want-spawn-nodes', True)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        newObj = None

        if objType == 'Searchable Container' and self.wantSearchables:
            newObj = self.__createSearchableContainer(parent, parentUid, objKey, objectData)
        elif objType in ['Animal', 'Townsperson', 'Spawn Node', 'Dormant NPC Spawn Node', 'Skeleton', 'NavySailor', 'Creature']:
            newObj = self.air.enemySpawner.createObject(objType, objectData, parent, parentUid, objKey, dynamic)
        elif objType == 'Object Spawn Node' and self.wantSpawnNodes:
            newObj = self.__createObjectSpawnNode(parent, parentUid, objKey, objectData)

        return newObj

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
        self.broadcastObjectPosition(container)

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
        self.broadcastObjectPosition(spawnNode)

        return spawnNode
