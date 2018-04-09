from direct.directnotify import DirectNotifyGlobal
from pirates.destructibles.DistributedDestructibleObjectUD import DistributedDestructibleObjectUD

class DistributedDestructibleArrayUD(DistributedDestructibleObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDestructibleArrayUD')

    def __init__(self, air):
        DistributedDestructibleObjectUD.__init__(self, air)