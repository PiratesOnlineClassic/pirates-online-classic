import FlagGlobals
from direct.distributed.DistributedObject import DistributedObject
from Flag import Flag
from pandac.PandaModules import *

class DistributedFlagShop(DistributedObject):
    
    notify = directNotify.newCategory('DistributedFlagShop')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)