import os
import random

from direct.interval.IntervalGlobal import *
from direct.particles import ForceGroup, Particles
from direct.particles.ParticleEffect import *
from pandac.PandaModules import *
from PooledEffect import PooledEffect


class Twister(PooledEffect):
    __module__ = __name__
    particleDummy = None

    def __init__(self):
        PooledEffect.__init__(self)
        self.psParent = self.attachNewNode('psParent')
        self.psParent.setDepthWrite(0)
        self.psParent.setColorScale(Vec4(1), 1)
        self.psParent.setLightOff()
        self.psParent.setColorScaleOff()
        particleSearchPath = DSearchPath()
        particleSearchPath.appendDirectory(Filename('../resources/phase_2/etc'))
        particleSearchPath.appendDirectory(Filename('phase_2/etc'))
        particleSearchPath.appendDirectory(Filename('.'))
        pfile = Filename('dust.ptf')
        found = vfs.resolveFilename(pfile, particleSearchPath)
        self.dust = ParticleEffect()
        self.dust.setBin('fixed', 110)
        if found:
            self.dust.loadConfig(pfile)
        pfile = Filename('dirt.ptf')
        found = vfs.resolveFilename(pfile, particleSearchPath)
        self.dirt = ParticleEffect()
        self.dirt.setBin('fixed', 105)
        if found:
            self.dirt.loadConfig(pfile)
        self.pIval = None
        return

    def getParticleInterval(self, duration):
        if not self.pIval:
            self.pIval = Sequence(Parallel(ParticleInterval(self.dust, parent=self.psParent, worldRelative=0, duration=duration, softStopT=-3.0), ParticleInterval(self.dirt, parent=self.psParent, worldRelative=0, duration=duration, softStopT=-3.0)))
        return self.pIval

    def start(self):
        self.dust.start(self.psParent)
        self.dust.softStart()
        self.dirt.start(self.psParent)
        self.dirt.softStart()

    def stop(self):
        if self.pIval:
            self.pIval.finish()
            self.pIval = None
        for p in self.dust.getParticlesList():
            p.softStop()
            p.clearToInitial()

        self.dust.disable()
        for p in self.dirt.getParticlesList():
            p.softStop()
            p.clearToInitial()

        self.dirt.disable()
        return

    def cleanUpEffect(self):
        self.stop()
        self.detachNode()
        if self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        self.cleanUpEffect()
        self.dust.cleanup()
        self.dirt.cleanup()
        del self.dust
        del self.dirt
        self.removeNode()
        PooledEffect.destroy(self, self)
