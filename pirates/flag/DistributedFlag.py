from panda3d.core import *
from direct.distributed.DistributedObject import DistributedObject
from . import FlagGlobals
from .Flag import Flag

class DistributedFlag(DistributedObject, Flag):
    notify = directNotify.newCategory('DistributedFlag')
    
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        Flag.__init__(self, 'flag')

    def setDNAString(self, dnaStr):
        self.notify.debug('setDNAString: ' + repr(dnaStr))
        Flag.setDNAString(self, dnaStr)
        self.flatten()
    
    def d_requestDNAString(self, dnaStr):
        self.notify.debug('d_requestDNAString: ' + repr(dnaStr))
        self.sendUpdate('requestDNAString', [dnaStr])

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.notify.debug('generated')
    
    def disable(self):
        self.detachNode()
        DistributedObject.disable(self)

