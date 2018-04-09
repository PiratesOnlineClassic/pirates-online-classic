# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.uberdog.PirateInventory
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObject import DistributedObject
from pirates.uberdog.DistributedInventory import DistributedInventory


class PirateInventory(DistributedInventory):
    __module__ = __name__
    notify = directNotify.newCategory('Inventory')
# okay decompiling .\pirates\uberdog\PirateInventory.pyc
