# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.uberdog.DistributedGoldReceipt
from direct.distributed.ClockDelta import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObject import DistributedObject
from pirates.uberdog.UberDogGlobals import *

class DistributedGoldReceipt(DistributedObject):
    __module__ = __name__
    notify = directNotify.newCategory('GoldReceipt')

    def setGoldPaid(self, goldPaid):
        self.goldPaid = goldPaid

    def setExpirationDate(self, expirationDate):
        self.expirationDate = expirationDate
# okay decompiling .\pirates\uberdog\DistributedGoldReceipt.pyc
