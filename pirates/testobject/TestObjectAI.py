# NO BASE CLASSES WERE FOUND! 
 #THIS CLASS LIKELY HAD NO DEFINITION IN THE DCLASS FILES WHEN stub_generator.py WAS RUN!

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class TestObjectAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TestObjectAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.value = ''


    # setValue(string) broadcast ram db required
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setValue(self, value):
        self.value = value

    def d_setValue(self, value):
        self.sendUpdate('setValue', [value])

    def b_setValue(self, value):
        self.setValue(value)
        self.d_setValue(value)

    def getValue(self):
        return self.value


