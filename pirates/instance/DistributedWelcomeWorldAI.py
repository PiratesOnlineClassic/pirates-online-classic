
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from direct.directnotify import DirectNotifyGlobal

class DistributedWelcomeWorldAI(DistributedInstanceBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWelcomeWorldAI')

    def __init__(self, air):
        DistributedInstanceBaseAI.__init__(self, air)



