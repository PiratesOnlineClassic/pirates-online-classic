# NO BASE CLASSES WERE FOUND! 
 #THIS CLASS LIKELY HAD NO DEFINITION IN THE DCLASS FILES WHEN stub_generator.py WAS RUN!

from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class ObjectServerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('ObjectServerUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
        self.name = ''
        self.dcHash = 0


    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    # setDcHash(uint32) ram required
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setDcHash(self, dcHash):
        self.dcHash = dcHash

    def d_setDcHash(self, dcHash):
        self.sendUpdate('setDcHash', [dcHash])

    def b_setDcHash(self, dcHash):
        self.setDcHash(dcHash)
        self.d_setDcHash(dcHash)

    def getDcHash(self):
        return self.dcHash



