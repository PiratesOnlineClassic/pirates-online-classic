
from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from direct.directnotify import DirectNotifyGlobal

class DistributedRoosterAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRoosterAI')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)



