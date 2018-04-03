# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.shipparts.DistributedMastOV
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObjectOV
from pirates.ship import ShipGlobals


class DistributedMastOV(DistributedObjectOV.DistributedObjectOV):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedMastOV')

    def __init__(self, cr):
        DistributedObjectOV.DistributedObjectOV.__init__(self, cr)
        self.stopSend = 8 | 4 | 2 | 1
        self.shipId = 0
        self.mastType = 0
        self.posIndex = 0
        self.sailConfig = []

    def announceGenerate(self):
        DistributedObjectOV.DistributedObjectOV.announceGenerate(self)

    def disable(self):
        DistributedObjectOV.DistributedObjectOV.disable(self)

    def __repr__(self):
        return `(self.doId)`

    def setShipId(self, val):
        self.shipId = val
        self.stopSend ^= 1
        self.sendMessage()

    def setMastType(self, val):
        self.mastType = val
        self.stopSend ^= 2
        self.sendMessage()

    def setPosIndex(self, val):
        self.posIndex = val
        self.stopSend ^= 4
        self.sendMessage()

    def setSailConfig(self, val):
        self.sailConfig = val
        self.stopSend ^= 8
        self.sendMessage()

    def sendMessage(self):
        if not self.stopSend:
            messenger.send('setMastType-%s' % self.shipId, [
             self.mastType, self.posIndex, self.sailConfig])
# okay decompiling .\pirates\shipparts\DistributedMastOV.pyc
