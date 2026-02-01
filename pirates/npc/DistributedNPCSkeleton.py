from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.battle import DistributedBattleNPC
from pirates.npc import Skeleton
from pirates.effects.JRSpawnEffect import JRSpawnEffect
from . import NPCSkeletonGameFSM

class DistributedNPCSkeleton(DistributedBattleNPC.DistributedBattleNPC, Skeleton.Skeleton):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCSkeleton')
    
    def __init__(self, cr):
        DistributedBattleNPC.DistributedBattleNPC.__init__(self, cr)
        Skeleton.Skeleton.__init__(self)

    def announceGenerate(self):
        DistributedBattleNPC.DistributedBattleNPC.announceGenerate(self)
    
    def generate(self):
        DistributedBattleNPC.DistributedBattleNPC.generate(self)
        self.setInteractOptions(isTarget = False, allowInteract = False)
    
    def disable(self):
        DistributedBattleNPC.DistributedBattleNPC.disable(self)
        Skeleton.Skeleton.disable(self)
    
    def delete(self):
        DistributedBattleNPC.DistributedBattleNPC.delete(self)
        Skeleton.Skeleton.delete(self)
    
    def getNameText(self):
        return Skeleton.Skeleton.getNameText(self)

    def setAvatarType(self, avatarType):
        Skeleton.Skeleton.setAvatarType(self, avatarType)
        DistributedBattleNPC.DistributedBattleNPC.setAvatarType(self, avatarType)

    def createGameFSM(self):
        self.gameFSM = NPCSkeletonGameFSM.NPCSkeletonGameFSM(self)
    
    def initializeDropShadow(self):
        Skeleton.Skeleton.initializeDropShadow(self)
    
    def setSpeed(self, forwardSpeed, rotateSpeed):
        if self.gameFSM.state == 'Jump':
            return
        
        Skeleton.Skeleton.setSpeed(self, forwardSpeed, rotateSpeed)

    def setHp(self, hitPoints, quietly = 0):
        DistributedBattleNPC.DistributedBattleNPC.setHp(self, hitPoints, quietly)
        if self.glow:
            self.glow.adjustHeartColor(float(self.hp) / float(self.maxHp))

    def getEnterDeathTrack(self):
        return Skeleton.Skeleton.getEnterDeathTrack(self)
    
    def getExitDeathTrack(self):
        return Skeleton.Skeleton.getExitDeathTrack(self)
    
    def play(self, *args, **kwArgs):
        Skeleton.Skeleton.play(self, *args, **kwArgs)

    def loop(self, *args, **kwArgs):
        Skeleton.Skeleton.loop(self, *args, **kwArgs)
    
    def pose(self, *args, **kwArgs):
        Skeleton.Skeleton.pose(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        Skeleton.Skeleton.pingpong(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        Skeleton.Skeleton.stop(self, *args, **kwArgs)

    def getSpawnTrack(self):
        duration = self.getDuration('intro')
        if not duration:
            return None
        
        def startVFX():
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                spawnEffect = JRSpawnEffect.getEffect()
                if spawnEffect:
                    spawnEffect.reparentTo(render)
                    spawnEffect.setPos(self.getPos(render))
                    spawnEffect.duration = duration / 2.0
                    spawnEffect.effectScale = 1.0
                    spawnEffect.play()

        if hasattr(self, 'ambushEnemy'):
            spawnIval = Sequence(Func(self.hide), Func(startVFX), Wait(1.0), Parallel(self.actorInterval('intro'), Sequence(Wait(0.5), Func(self.show))), Func(self.ambushIntroDone))
        else:
            spawnIval = Sequence(Func(self.hide), Func(startVFX), Wait(1.0), Parallel(self.actorInterval('intro'), Sequence(Wait(0.5), Func(self.show))))
        return spawnIval


