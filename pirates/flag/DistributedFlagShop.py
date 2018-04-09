# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.flag.DistributedFlagShop
import FlagGlobals
from direct.distributed.DistributedObject import DistributedObject
from Flag import Flag
from pandac.PandaModules import *


class DistributedFlagShop(DistributedObject):
    
    notify = directNotify.newCategory('DistributedFlagShop')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
# okay decompiling .\pirates\flag\DistributedFlagShop.pyc
