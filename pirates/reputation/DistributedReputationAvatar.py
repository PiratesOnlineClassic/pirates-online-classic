# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.reputation.DistributedReputationAvatar
from . import ReputationGlobals
from direct.directnotify import DirectNotifyGlobal
from otp.avatar import DistributedAvatar
from pirates.battle import WeaponGlobals
from pirates.distributed import DistributedInteractive
from pirates.movement import DistributedMovingObject
from pirates.piratesbase import PiratesGlobals
from pirates.quest import DistributedQuestGiver
from pirates.uberdog.UberDogGlobals import InventoryType


class DistributedReputationAvatar(DistributedAvatar.DistributedAvatar, DistributedMovingObject.DistributedMovingObject, DistributedInteractive.DistributedInteractive, DistributedQuestGiver.DistributedQuestGiver):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedReputationAvatar')

    def __init__(self, cr):
        DistributedAvatar.DistributedAvatar.__init__(self, cr)
        DistributedMovingObject.DistributedMovingObject.__init__(self, cr)
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        DistributedQuestGiver.DistributedQuestGiver.__init__(self)
        self.nametag.setWordwrap(PiratesGlobals.NAMETAG_WORDWRAP)

    def generate(self):
        DistributedAvatar.DistributedAvatar.generate(self)
        DistributedMovingObject.DistributedMovingObject.generate(self)
        DistributedInteractive.DistributedInteractive.generate(self)
        DistributedQuestGiver.DistributedQuestGiver.generate(self)

    def delete(self):
        DistributedAvatar.DistributedAvatar.delete(self)
        DistributedMovingObject.DistributedMovingObject.delete(self)
        DistributedInteractive.DistributedInteractive.delete(self)
        DistributedQuestGiver.DistributedQuestGiver.delete(self)

    def disable(self):
        DistributedAvatar.DistributedAvatar.disable(self)
        DistributedMovingObject.DistributedMovingObject.disable(self)
        DistributedInteractive.DistributedInteractive.disable(self)
        DistributedQuestGiver.DistributedQuestGiver.disable(self)

    def announceGenerate(self):
        DistributedAvatar.DistributedAvatar.announceGenerate(self)
        DistributedMovingObject.DistributedMovingObject.announceGenerate(self)
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        DistributedQuestGiver.DistributedQuestGiver.announceGenerate(self)

    def setLocation(self, parentId, zoneId, teleport=0):
        DistributedMovingObject.DistributedMovingObject.setLocation(self, parentId, zoneId, teleport)

    def wrtReparentTo(self, parent):
        DistributedMovingObject.DistributedMovingObject.wrtReparentTo(self, parent)

    def updateReputation(self, category, value):
        pass

    def __str__(self):
        className = self.__class__.__name__
        if hasattr(self, 'doId'):
            doId = self.doId
        else:
            doId = 'no doId'

        name = self.getName()
        return '%s: %s: "%s"' % (className, doId, name)
# okay decompiling .\pirates\reputation\DistributedReputationAvatar.pyc
