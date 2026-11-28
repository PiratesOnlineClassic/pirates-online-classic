from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from direct.directnotify import DirectNotifyGlobal

class DistributedScorpionAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedScorpionAI')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)
