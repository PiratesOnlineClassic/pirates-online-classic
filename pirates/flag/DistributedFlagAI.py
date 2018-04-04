
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedFlagAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFlagAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.dNAString = ''


    # setDNAString(string) required broadcast ram db
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setDNAString(self, dNAString):
        self.dNAString = dNAString

    def d_setDNAString(self, dNAString):
        self.sendUpdate('setDNAString', [dNAString])

    def b_setDNAString(self, dNAString):
        self.setDNAString(dNAString)
        self.d_setDNAString(dNAString)

    def getDNAString(self):
        return self.dNAString

    # requestDNAString(string) airecv clsend

    def requestDNAString(self, requestDNAString):
        pass


