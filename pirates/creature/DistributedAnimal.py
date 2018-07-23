from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPRender
from pirates.creature import DistributedCreature
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals


class DistributedAnimal(DistributedCreature.DistributedCreature):
    

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
