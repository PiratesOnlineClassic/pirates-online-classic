from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from direct.directnotify import DirectNotifyGlobal

class DistributedScoprionAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedScoprionAI')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)
