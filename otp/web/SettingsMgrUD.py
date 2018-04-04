
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class SettingsMgrUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('SettingsMgrUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)





