from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from direct.directnotify import DirectNotifyGlobal

class DistributedWaspAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWaspAI')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)
