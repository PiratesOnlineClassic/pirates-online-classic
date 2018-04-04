
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTeleportZoneAI(DistributedInstanceBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportZoneAI')

    def __init__(self, air):
        DistributedInstanceBaseAI.__init__(self, air)



