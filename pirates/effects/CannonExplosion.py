from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from .PooledEffect import PooledEffect
from .EffectController import EffectController
import random

class CannonExplosion(PooledEffect, EffectController):
    splashSfx = []
    splashSfxNames = ('explo_wood_1.mp3', 'explo_wood_2.mp3')
    
    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if not self.splashSfx:
            for filename in self.splashSfxNames:
                self.splashSfx.append(base.loader.loadSfx('audio/' + filename))

        self.splash = Actor.Actor()
        self.splash.loadModel('models/effects/cannonballExplosion-zero')
        animDict = {}
        animDict['splashdown'] = 'models/effects/cannonballExplosion-anim'
        self.splash.loadAnims(animDict)
        self.splash.reparentTo(self)
        self.splash.setTransparency(1)
        self.splash.setDepthWrite(0)
        self.splash.hide()
    
    def createTrack(self):
        animDuration = 0.35
        fadeOut = self.splash.colorInterval(0.8, Vec4(1, 1, 1, 0), startColor = Vec4(1, 1, 1, 1))
        animateSplash = Sequence(Func(self.splash.pose, 'splashdown', 0), Func(self.splash.show), Func(self.splash.setColor, Vec4(1, 1, 1, 1)), Func(self.splash.play, 'splashdown'), Wait(animDuration), fadeOut, Wait(1.0), Func(self.splash.stop), Func(self.splash.hide), Func(self.cleanUpEffect))
        sfx = random.choice(self.splashSfx)
        self.track = Parallel(animateSplash, Func(base.playSfx, sfx, volume = 1, node = self.splash))
    
    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        self.splash.cleanup()
        del self.splash
        EffectController.destroy(self)
        PooledEffect.destroy(self)


