
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class DistributedFlagUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFlagUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
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



