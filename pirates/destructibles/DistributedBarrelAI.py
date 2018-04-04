
from pirates.destructibles.DistributedDestructibleObjectAI import DistributedDestructibleObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBarrelAI(DistributedDestructibleObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBarrelAI')

    def __init__(self, air):
        DistributedDestructibleObjectAI.__init__(self, air)



