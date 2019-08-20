from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class AvatarAccessoriesManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarAccessoriesManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)