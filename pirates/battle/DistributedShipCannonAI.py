# AN UNEXPECTED ERROR OCCURED WHILE GENERATING THIS STUB FILE.
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedShipCannonAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipCannonAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)