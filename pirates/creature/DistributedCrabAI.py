
from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from direct.directnotify import DirectNotifyGlobal

class DistributedCrabAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCrabAI')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)



