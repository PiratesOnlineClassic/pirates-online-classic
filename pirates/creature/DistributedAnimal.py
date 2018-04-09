# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.DistributedAnimal
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPRender
from pirates.creature import DistributedCreature
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals


class DistributedAnimal(DistributedCreature.DistributedCreature):
    __module__ = __name__

    def __init__(self, cr):
        DistributedCreature.DistributedCreature.__init__(self, cr)
        self.battleCollisionBitmask = PiratesGlobals.WallBitmask | PiratesGlobals.TargetBitmask
        OTPRender.renderReflection(False, self, 'p_animal', None)
        return

    def customInteractOptions(self):
        self.setInteractOptions(proximityText=None, allowInteract=False)
        return

    def showHpMeter(self):
        pass

    def isBattleable(self):
        return 0

    def initializeBattleCollisions(self):
        pass
# okay decompiling .\pirates\creature\DistributedAnimal.pyc
