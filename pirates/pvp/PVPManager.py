# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pvp.PVPManager
from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject
from pirates.uberdog.UberDogGlobals import *
from pirates.piratesbase import PiratesGlobals

class PVPManager(DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPManager')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.cr.pvpManager = self

    def delete(self):
        self.ignoreAll()
        if self.cr.pvpManager == self:
            self.cr.pvpManager = None
        DistributedObject.delete(self)
        return

    def sendRequestChallenge(self, challengeeId):
        self.sendUpdate('requestChallenge', [challengeeId])

    def sendAcceptChallenge(self, challengerId):
        self.sendUpdate('acceptChallenge', [challengerId])

    def challengeFrom(self, avId):
        messenger.send(PiratesGlobals.PVPChallengedEvent, [avId])

    def challengeAccepted(self, avId):
        messenger.send(PiratesGlobals.PVPAcceptedEvent, [avId])
# okay decompiling .\pirates\pvp\PVPManager.pyc
