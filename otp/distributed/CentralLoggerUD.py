
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class CentralLoggerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('CentralLoggerUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)


    # sendMessage(string, string, uint32, uint32) clsend


