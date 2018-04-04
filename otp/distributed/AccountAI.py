# NO BASE CLASSES WERE FOUND! 
 #THIS CLASS LIKELY HAD NO DEFINITION IN THE DCLASS FILES WHEN stub_generator.py WAS RUN!

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class AccountAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('AccountAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)



