# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.uberdog.DistributedShipLoader
from pickle import dumps, loads

from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.distributed.ClockDelta import *
from pirates.uberdog.UberDogGlobals import *


class DistributedShipLoader(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipLoader')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.ships = {}
        self.notify.warning('ShipLoader going online')

    def delete(self):
        self.ignoreAll()
        self.notify.warning('ShipLoader going offline')
        self.cr.shipLoader = None
        DistributedObject.DistributedObject.delete(self)
        return
# okay decompiling .\pirates\uberdog\DistributedShipLoader.pyc
