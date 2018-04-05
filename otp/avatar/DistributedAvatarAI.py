from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from direct.directnotify import DirectNotifyGlobal

class DistributedAvatarAI(DistributedSmoothNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAvatarAI')

    def __init__(self, air):
        DistributedSmoothNodeAI.__init__(self, air)
