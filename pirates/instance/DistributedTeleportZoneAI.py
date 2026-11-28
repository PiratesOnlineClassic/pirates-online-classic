from direct.directnotify import DirectNotifyGlobal

from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from pirates.instance.DistributedInstanceWorldAI import DistributedInstanceWorldAI


class DistributedTeleportZoneAI(DistributedInstanceWorldAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportZoneAI')

    def __init__(self, air):
        DistributedInstanceWorldAI.__init__(self, air)

    def generate(self):
        # a teleport zone is only a temporary holding area for teleporting
        # avatars, it does not need an ocean grid of it's own...
        DistributedInstanceBaseAI.generate(self)

    def delete(self):
        self.air.deallocateZone(self.zoneId)

        DistributedInstanceWorldAI.delete(self)
