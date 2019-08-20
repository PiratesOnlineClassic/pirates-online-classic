from direct.directnotify import DirectNotifyGlobal

from pirates.instance.DistributedInstanceWorldAI import DistributedInstanceWorldAI


class DistributedTeleportZoneAI(DistributedInstanceWorldAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportZoneAI')

    def __init__(self, air):
        DistributedInstanceWorldAI.__init__(self, air)

    def delete(self):
        self.air.deallocateZone(self.zoneId)

        DistributedInstanceWorldAI.delete(self)
