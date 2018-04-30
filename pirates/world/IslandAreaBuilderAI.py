from pirates.world.GameAreaBuilderAI import GameAreaBuilderAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesbase import PiratesGlobals
from pirates.interact.DistributedSearchableContainerAI import DistributedSearchableContainerAI
from pirates.world.DistributedDinghyAI import DistributedDinghyAI
from pirates.treasuremap.DistributedBuriedTreasureAI import DistributedBuriedTreasureAI
from pirates.treasuremap.DistributedSurfaceTreasureAI import DistributedSurfaceTreasureAI

class IslandAreaBuilderAI(GameAreaBuilderAI):
    notify = directNotify.newCategory('IslandAreaBuilderAI')

    def __init__(self, air, parent):
        GameAreaBuilderAI.__init__(self, air, parent)

        self.wantDinghys = config.GetBool('want-dinghys', True)

    def parentObjectToCell(self, object, zoneId=None, parent=None):
        parent = GameAreaBuilderAI.parentObjectToCell(self, object, zoneId, parent)
        object.b_setLocation(parent.doId, PiratesGlobals.IslandLocalZone)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        if objType == 'Player Spawn Node':
            newObj = self.__createPlayerSpawnNode(objectData, parent, parentUid, objKey, dynamic)
        elif objType == 'Dinghy' and self.wantDinghys:
            newObj = self.__createDinghy(parent, parentUid, objKey, objectData)
        else:
            newObj = GameAreaBuilderAI.createObject(self, objType, objectData, parent, parentUid, objKey,
                dynamic, parentIsObj, fileName, actualParentObj)

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

        (x, y, z), objectParent = self.getObjectTruePosAndParent(objKey, parentUid, objectData)
        h, p, r = objectData.get('Hpr', (0, 0, 0))

        parent.addSpawnPt(self.parent.getUniqueId(), (x, y, z, h))

        return None

    def __createDinghy(self, parent, parentUid, objKey, objectData):
        dinghy = DistributedDinghyAI(self.air)
        dinghy.setPos(objectData.get('Pos', (0, 0, 0)))
        dinghy.setHpr(objectData.get('Hpr', (0, 0, 0)))
        dinghy.setInteractRadius(float(objectData.get('Aggro Radius', 25)))

        zoneId = self.parent.getZoneFromXYZ(dinghy.getPos())
        parent.generateChildWithRequired(dinghy, zoneId)
        self.parentObjectToCell(dinghy, zoneId)

        self.addObject(dinghy)

        return dinghy
