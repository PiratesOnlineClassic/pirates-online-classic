from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal


class ObjectServerUD(DistributedObjectUD):
    """
    Describes a server process to the cluster: its name, the hash of the dc
    files it was started with and when it came up.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('ObjectServerUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
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
