from direct.directnotify import DirectNotifyGlobal
from pirates.destructibles.DistributedDestructibleObjectAI import DistributedDestructibleObjectAI

class DistributedBarrelAI(DistributedDestructibleObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBarrelAI')

    def __init__(self, air):
        DistributedDestructibleObjectAI.__init__(self, air)