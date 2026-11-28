from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class ObjectServerAI(DistributedObjectAI):
    """
    Describes a server process to the cluster: its name, the hash of the dc
    files it was started with and when it came up.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('ObjectServerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.name = ''
        self.dcHash = 0
        self.dateCreated = 0

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setDcHash(self, dcHash):
        self.dcHash = dcHash

    def getDcHash(self):
        return self.dcHash

    def setDateCreated(self, dateCreated):
        self.dateCreated = dateCreated

    def getDateCreated(self):
        return self.dateCreated
