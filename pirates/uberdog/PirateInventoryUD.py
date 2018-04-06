from pirates.uberdog.DistributedInventoryUD import DistributedInventoryUD
from direct.directnotify import DirectNotifyGlobal

class PirateInventoryUD(DistributedInventoryUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PirateInventoryUD')
