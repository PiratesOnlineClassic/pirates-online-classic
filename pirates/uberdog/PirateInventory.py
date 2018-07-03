from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObject import DistributedObject
from pirates.uberdog.DistributedInventory import DistributedInventory

class PirateInventory(DistributedInventory):
    notify = directNotify.newCategory('Inventory')
