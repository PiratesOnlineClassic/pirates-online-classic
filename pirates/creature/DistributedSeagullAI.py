from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from direct.directnotify import DirectNotifyGlobal

class DistributedSeagullAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSeagullAI')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)
