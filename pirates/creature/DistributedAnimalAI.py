
from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from direct.directnotify import DirectNotifyGlobal

class DistributedAnimalAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAnimalAI')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)



