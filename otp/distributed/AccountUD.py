# NO BASE CLASSES WERE FOUND! 
 #THIS CLASS LIKELY HAD NO DEFINITION IN THE DCLASS FILES WHEN stub_generator.py WAS RUN!

from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class AccountUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('AccountUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)



