from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.world.ClientAreaBuilderAI import ClientAreaBuilderAI

class InteriorAreaBuilderAI(ClientAreaBuilderAI):
    notify = directNotify.newCategory('InteriorAreaBuilderAI')

    def __init__(self, air, parent):
        ClientAreaBuilderAI.__init__(self, air, parent)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        return None
