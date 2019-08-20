
from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from direct.directnotify import DirectNotifyGlobal

class DistributedAlligatorAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAlligatorAI')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)



