from pirates.creature.DistributedAnimalAI import DistributedAnimalAI
from direct.directnotify import DirectNotifyGlobal

class DistributedDogAI(DistributedAnimalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDogAI')

    def __init__(self, air):
        DistributedAnimalAI.__init__(self, air)