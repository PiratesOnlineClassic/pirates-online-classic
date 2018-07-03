from pirates.creature.DistributedAnimalAI import DistributedAnimalAI
from direct.directnotify import DirectNotifyGlobal

class DistributedRoosterAI(DistributedAnimalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRoosterAI')

    def __init__(self, air):
        DistributedAnimalAI.__init__(self, air)