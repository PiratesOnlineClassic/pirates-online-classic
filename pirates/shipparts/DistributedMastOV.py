from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObjectOV
from pirates.ship import ShipGlobals

class DistributedMastOV(DistributedObjectOV.DistributedObjectOV):
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
        return repr(self.doId)

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
                self.mastType,
                self.posIndex,
                self.sailConfig])

