from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.world.ClientAreaBuilderAI import ClientAreaBuilderAI

class GameAreaBuilderAI(ClientAreaBuilderAI):
    notify = directNotify.newCategory('GameAreaBuilderAI')

    def __init__(self, air, parent):
        ClientAreaBuilderAI.__init__(self, air, parent)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        newObj = None

        if objType == 'Player Spawn Node':
            newObj = self.__createPlayerSpawnNode(objectData, parent, parentUid, objKey, dynamic)

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
