from direct.directnotify import DirectNotifyGlobal
from pirates.creature import DistributedCreature
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPRender

class DistributedAnimal(DistributedCreature.DistributedCreature):
    
    def __init__(self, cr):
        DistributedCreature.DistributedCreature.__init__(self, cr)
        self.battleCollisionBitmask = PiratesGlobals.WallBitmask | PiratesGlobals.TargetBitmask
        OTPRender.renderReflection(False, self, 'p_animal', None)

    def customInteractOptions(self):
        self.setInteractOptions(proximityText = None, allowInteract = False)

    def showHpMeter(self):
        pass

    def isBattleable(self):
        return 0
    
    def initializeBattleCollisions(self):
        pass


