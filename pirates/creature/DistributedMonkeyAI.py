from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from direct.directnotify import DirectNotifyGlobal

class DistributedMonkeyAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMonkeyAI')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)
