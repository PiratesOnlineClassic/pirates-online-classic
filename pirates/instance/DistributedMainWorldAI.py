
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from direct.directnotify import DirectNotifyGlobal

class DistributedMainWorldAI(DistributedInstanceBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMainWorldAI')

    def __init__(self, air):
        DistributedInstanceBaseAI.__init__(self, air)



