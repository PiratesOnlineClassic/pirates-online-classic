from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify import DirectNotifyGlobal

class DistributedEnemySpawner(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedEnemySpawner')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
