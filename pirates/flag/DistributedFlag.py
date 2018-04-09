# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.flag.DistributedFlag
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
# okay decompiling .\pirates\flag\DistributedFlag.pyc
