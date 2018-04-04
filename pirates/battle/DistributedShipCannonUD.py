# AN UNEXPECTED ERROR OCCURED WHILE GENERATING THIS STUB FILE.
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class DistributedShipCannonUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipCannonUD')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)