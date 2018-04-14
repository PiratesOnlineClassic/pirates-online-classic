import FlagGlobals
from direct.distributed.DistributedObject import DistributedObject
from Flag import Flag
from pandac.PandaModules import *

class DistributedFlag(DistributedObject, Flag):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedFlag')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        Flag.__init__(self, 'flag')

    def setDNAString(self, dnaStr):
        self.notify.debug('setDNAString: ' + `dnaStr`)
        Flag.setDNAString(self, dnaStr)
        self.flatten()

    def d_requestDNAString(self, dnaStr):
        self.notify.debug('d_requestDNAString: ' + `dnaStr`)
        self.sendUpdate('requestDNAString', [dnaStr])

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.notify.debug('generated')

    def disable(self):
        self.detachNode()
        DistributedObject.disable(self)