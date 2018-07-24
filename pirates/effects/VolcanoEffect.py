import random

from direct.interval.IntervalGlobal import (Func, Parallel, Sequence,
                                            SoundInterval, Wait)
from pandac.PandaModules import *
from pirates.effects.VolcanoSmoke import VolcanoSmoke
from pirates.effects.VolcanoSplats import VolcanoSplats


class VolcanoEffect(NodePath):
    eruptionSfx = None

    def __init__(self):
        NodePath.__init__(self, 'VolcanoEffect')
        self.renderParent = self.attachNewNode('VolcanoEffect-renderParent')
        self.renderParent.setDepthWrite(0)
        self.renderParent.setLightOff()
        self.renderParent.setTwoSided(True)
        self.smoke = VolcanoSmoke()
        self.smoke.reparentTo(self)
        self.smoke.getRenderParent().reparentTo(self.renderParent)
        self.smoke.getRenderParent().setBin('fixed', 10)
        self.smoke.force0.setAmplitude(0.09)
        self.smoke2 = VolcanoSmoke()
        self.smoke2.reparentTo(self)
        self.smoke2.getRenderParent().reparentTo(self.renderParent)
        self.smoke2.getRenderParent().setBin('fixed', 15)
        self.splats1 = VolcanoSplats()
        self.splats1.reparentTo(self)
        self.splats1.getRenderParent().reparentTo(self.renderParent)
        self.splats1.getRenderParent().setBin('fixed', 20)
        self.splats2 = VolcanoSplats()
        self.splats2.setParticleScale(0.5)
        self.splats2.reparentTo(self)
        self.splats2.getRenderParent().reparentTo(self.renderParent)
        self.splats2.getRenderParent().setBin('fixed', 20)
        self.seq = None
        self.eruptSeq = None
        if not self.eruptionSfx:
            self.eruptionSfx = (
             loader.loadSfx('audio/eruption.mp3'),)
        return

    def enable(self):
        self.enableSmoke()
        self.enableRest()

    def enableSmoke(self):
        self.smoke.enable()
        self.smoke2.enable()

    def enableRest(self):
        self.splats1.enable()
        self.splats2.enable()

    def disable(self):
        self.disableSmoke()
        self.disableRest()

    def disableSmoke(self):
        self.smoke.disable()
        self.smoke2.disable()

    def disableRest(self):
        self.splats1.disable()
        self.splats2.disable()

    def destroy(self):
        self.disable()
        if self.seq:
            self.seq.pause()
        if self.eruptSeq:
            self.eruptSeq.finish()
        del self.seq
        del self.eruptSeq
        self.smoke.destroy()
        self.smoke2.destroy()
        self.splats1.destroy()
        self.splats2.destroy()
        del self.smoke
        del self.smoke2
        del self.splats1
        del self.splats2
        self.renderParent.removeNode()
        del self.renderParent

    def enableFogSmoke(self):
        self.smoke2.getRenderParent().setFogOff()
        self.splats1.getRenderParent().setFogOff()
        self.splats2.getRenderParent().setFogOff()

    def disableFogSmoke(self):
        self.smoke.getRenderParent().clearFog()
        self.smoke2.getRenderParent().clearFog()
        self.splats1.getRenderParent().clearFog()
        self.splats2.getRenderParent().clearFog()

    def getEruptSequence(self):
        if not self.eruptSeq:
            self.eruptSeq = Parallel(self.splats2.getEruptionSeq(), Sequence(Wait(0.75), self.splats1.getEruptionSeq()), SoundInterval(self.eruptionSfx[0]))
        return self.eruptSeq

    def start(self):
        self.stop()
        if not self.isRestEnabled():
            self.enableRest()
        self.seq = Parallel(self.getEruptSequence(), Sequence(Wait(random.randint(60, 120)), Func(self.start)))
        self.seq.start()

    def stop(self):
        if self.seq:
            self.seq.pause()
        if self.eruptSeq:
            self.eruptSeq.pause()

    def isEnabled(self):
        return self.smoke.isEnabled() | self.smoke2.isEnabled() | self.splats1.isEnabled() | self.splats2.isEnabled()

    def isSmokeEnabled(self):
        return self.smoke.isEnabled() | self.smoke2.isEnabled()

    def isRestEnabled(self):
        return self.splats1.isEnabled() | self.splats2.isEnabled()

    def isPlaying(self):
        if hasattr(self, 'seq') and self.seq:
            return self.seq.isPlaying()
        return False

    def hideSmoke(self):
        self.smoke.getRenderParent().hide()
        self.smoke2.getRenderParent().hide()

    def showSmoke(self):
        self.smoke.getRenderParent().show()
        self.smoke2.getRenderParent().show()

    def accelerateSmoke(self, time):
        self.smoke.accelerate(time)
        self.smoke2.accelerate(time)
