
from pirates.instance.DistributedInstanceBase import DistributedInstanceBase
from direct.directnotify import DirectNotifyGlobal

class DistributedTeleportZoneUD(DistributedInstanceBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportZoneUD')

    def __init__(self, air):
        DistributedInstanceBase.__init__(self, air)



