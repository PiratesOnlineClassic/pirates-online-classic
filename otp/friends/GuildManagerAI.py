# AN UNEXPECTED ERROR OCCURED WHILE GENERATING THIS STUB FILE.
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class GuildManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('GuildManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)