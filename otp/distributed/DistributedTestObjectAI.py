
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTestObjectAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTestObjectAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.requiredField = 0


    # setRequiredField(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setRequiredField(self, requiredField):
        self.requiredField = requiredField

    def d_setRequiredField(self, requiredField):
        self.sendUpdate('setRequiredField', [requiredField])

    def b_setRequiredField(self, requiredField):
        self.setRequiredField(requiredField)
        self.d_setRequiredField(requiredField)

    def getRequiredField(self):
        return self.requiredField

    # setB(uint32) broadcast

    def setB(self, b):
        self.sendUpdate('setB', [b])

    # setBA(uint32) broadcast airecv

    def setBA(self, bA):
        pass

    # setBO(uint32) broadcast ownsend

    def setBO(self, bO):
        self.sendUpdate('setBO', [bO])

    # setBR(uint32) broadcast ram

    def setBR(self, bR):
        self.sendUpdate('setBR', [bR])

    # setBRA(uint32) broadcast ram airecv

    def setBRA(self, bRA):
        pass

    # setBRO(uint32) broadcast ram ownsend

    def setBRO(self, bRO):
        self.sendUpdate('setBRO', [bRO])

    # setBROA(uint32) broadcast ram ownsend airecv

    def setBROA(self, bROA):
        pass


