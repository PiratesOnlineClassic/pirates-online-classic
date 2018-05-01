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
        if objType == 'Dinghy' and self.wantDinghys:
            newObj = self.__createDinghy(parent, parentUid, objKey, objectData)
        else:
            newObj = GameAreaBuilderAI.createObject(self, objType, objectData, parent, parentUid, objKey,
                dynamic, parentIsObj, fileName, actualParentObj)

        return newObj

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
