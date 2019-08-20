from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from direct.directnotify import DirectNotifyGlobal

class DistributedStumpAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedStumpAI')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)
