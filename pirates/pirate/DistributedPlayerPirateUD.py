# AN UNEXPECTED ERROR OCCURED WHILE GENERATING THIS STUB FILE.
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class DistributedPlayerPirateUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerPirateUD')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)