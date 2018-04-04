
from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal

class DistributedShipDeployerAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipDeployerAI')

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)
        self.minRadius = 0
        self.maxRadius = 0
        self.spacing = 0
        self.heading = 0


    # setMinRadius(uint32/100) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setMinRadius(self, minRadius):
        self.minRadius = minRadius

    def d_setMinRadius(self, minRadius):
        self.sendUpdate('setMinRadius', [minRadius])

    def b_setMinRadius(self, minRadius):
        self.setMinRadius(minRadius)
        self.d_setMinRadius(minRadius)

    def getMinRadius(self):
        return self.minRadius

    # setMaxRadius(uint32/100) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setMaxRadius(self, maxRadius):
        self.maxRadius = maxRadius

    def d_setMaxRadius(self, maxRadius):
        self.sendUpdate('setMaxRadius', [maxRadius])

    def b_setMaxRadius(self, maxRadius):
        self.setMaxRadius(maxRadius)
        self.d_setMaxRadius(maxRadius)

    def getMaxRadius(self):
        return self.maxRadius

    # setSpacing(uint32/100) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setSpacing(self, spacing):
        self.spacing = spacing

    def d_setSpacing(self, spacing):
        self.sendUpdate('setSpacing', [spacing])

    def b_setSpacing(self, spacing):
        self.setSpacing(spacing)
        self.d_setSpacing(spacing)

    def getSpacing(self):
        return self.spacing

    # setHeading(uint32/100) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setHeading(self, heading):
        self.heading = heading

    def d_setHeading(self, heading):
        self.sendUpdate('setHeading', [heading])

    def b_setHeading(self, heading):
        self.setHeading(heading)
        self.d_setHeading(heading)

    def getHeading(self):
        return self.heading

    # shipEnteredSphere(uint32, uint8) clsend airecv

    def shipEnteredSphere(self, shipEnteredSphere, todo_uint8_1):
        pass

    # shipExitedSphere(uint32, uint8) clsend airecv

    def shipExitedSphere(self, shipExitedSphere, todo_uint8_1):
        pass

    # shipExitedBarrier(uint32) clsend airecv

    def shipExitedBarrier(self, shipExitedBarrier):
        pass


