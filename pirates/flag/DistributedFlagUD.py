from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedFlagUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFlagUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        self.dnaString = b''

    def setDNAString(self, dnaString):
        self.dnaString = dnaString

    def d_setDNAString(self, dnaString):
        self.sendUpdate('setDNAString', [dnaString])

    def b_setDNAString(self, dnaString):
        self.setDNAString(dnaString)
        self.d_setDNAString(dnaString)

    def getDNAString(self):
        return self.dnaString

    def requestDNAString(self, dnaString):
        # flag designs are only ever validated by the AI which owns the flag object...
        self.notify.warning('Received requestDNAString on the UberDOG for flag %d!' % self.doId)
