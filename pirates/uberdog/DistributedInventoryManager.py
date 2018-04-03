# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.uberdog.DistributedInventoryManager
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.distributed.ClockDelta import *
from pirates.uberdog.UberDogGlobals import *


class DistributedInventoryManager(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('InventoryManager')

    def sendRequestInventory(self):
        self.sendUpdate('requestInventory', [])
# okay decompiling .\pirates\uberdog\DistributedInventoryManager.pyc
