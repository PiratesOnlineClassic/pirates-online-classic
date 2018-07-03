from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from direct.directnotify import DirectNotifyGlobal

class DistributedFlyTrapAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFlyTrapAI')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)
