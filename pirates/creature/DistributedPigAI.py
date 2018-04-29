from pirates.creature.DistributedAnimalAI import DistributedAnimalAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPigAI(DistributedAnimalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPigAI')

    def __init__(self, air):
        DistributedAnimalAI.__init__(self, air)
