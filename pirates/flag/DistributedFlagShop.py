from panda3d.core import *
from direct.distributed.DistributedObject import DistributedObject
from . import FlagGlobals
from .Flag import Flag

class DistributedFlagShop(DistributedObject):
    notify = directNotify.newCategory('DistributedFlagShop')
    
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

