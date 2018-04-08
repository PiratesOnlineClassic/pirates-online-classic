from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.world.ClientAreaBuilderAI import ClientAreaBuilderAI
from pirates.interact.DistributedSearchableContainerAI import DistributedSearchableContainerAI
from pirates.world.DistributedDinghyAI import DistributedDinghyAI

class GameAreaBuilderAI(ClientAreaBuilderAI):
    notify = directNotify.newCategory('GameAreaBuilderAI')

    def __init__(self, air, parent):
        ClientAreaBuilderAI.__init__(self, air, parent)

        self.wantSearchables = config.GetBool('want-searchables', True)
        self.wantDinghys = config.GetBool('want-dignhys', True)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        newObj = None

        if objType == 'Player Spawn Node':
            newObj = self.__createPlayerSpawnNode(objectData, parent, parentUid, objKey, dynamic)
        elif objType == 'Searchable Container' and self.wantSearchables:
            newObj = self.__createSearchableContainer(parent, parentUid, objKey, objectData)
        elif objType == 'Dinghy' and self.wantDinghys:
            newObj = self.__createDinghy(parent, parentUid, objKey, objectData)
        elif objType in ['Animal', 'Townsperson', 'Spawn Node', 'Dormant NPC Spawn Node', 'Skeleton', 'NavySailor', 'Creature', 'Ghost']:
            newObj = self.air.spawner.createObject(objType, objectData, parent, parentUid, objKey, dynamic)
            
        return newObj

    def __createPlayerSpawnNode(self, objectData, parent, parentUid, objKey, dynamic):
        from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
        from pirates.world.DistributedIslandAI import DistributedIslandAI

        parent = self.parent.getParentObj()

        if isinstance(parent, DistributedIslandAI):
            parent = parent.getParentObj()

        if not parent or not isinstance(parent, DistributedInstanceBaseAI):
            self.notify.warning('Cannot setup player spawn point for %r!' % parent)
            return None

        x, y, z = objectData.get('Pos', objectData.get('GridPos', (0, 0, 0)))
        h, p, r = objectData.get('Hpr', (0, 0, 0))

        parent.addSpawnPt(self.parent.getUniqueId(), (x, y, z, h))

        return None

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

    def __createDinghy(self, parent, parentUid, objKey, objectData):
        dinghy = DistributedDinghyAI(self.air)

        dinghy.setPos(objectData.get('Pos', (0, 0, 0)))
        dinghy.setHpr(objectData.get('Hpr', (0, 0, 0)))
        dinghy.setInteractRadius(float(objectData.get('Aggro Radius', 25)))

        zoneId = self.parent.getZoneFromXYZ(dinghy.getPos())
        parent.generateChildWithRequired(dinghy, zoneId)
        self.parentObjectToCell(dinghy, zoneId)

        self.addObject(dinghy)
        self.broadcastObjectPosition(dinghy)

        return dinghy