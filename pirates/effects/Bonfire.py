# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.Bonfire
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.effects.Fire import Fire
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.piratesgui.GameOptions import Options

class Bonfire(NodePath):
    __module__ = __name__
    HackCount = 0

    def __init__(self, parent=None):
        NodePath.__init__(self, uniqueName('Bonfire'))
        self._fire = Fire.getEffect()
        self._smoke = BlackSmoke.getEffect()
        if self._fire:
            self._fire.reparentTo(self)
            self._fire.effectScale = 1.0
        if self._smoke:
            self._smoke.reparentTo(self)
        if parent is not None:
            self.reparentTo(parent)
        self._sound = None
        if Bonfire.HackCount == 0:
            Bonfire.HackCount += 1
            self._hasSound = True
            self._sound = SoundInterval(base.loadSfx('audio/bonfire.wav'), node=self, volume=0.5)
        else:
            self._hasSound = False
        return

    def disableSound(self):
        self._sound.pause()
        self._sound = None
        return

    def startLoop(self, lod=Options.SpecialEffectsHigh):
        if self._fire:
            self._fire.startLoop(lod)
        if self._smoke and lod >= Options.SpecialEffectsHigh:
            self._smoke.startLoop(lod)
        if self._sound is not None:
            self._sound.loop(stagger=True)
        return

    def stop(self):
        if self._fire:
            self._fire.stop()
        if self._smoke:
            self._smoke.stop()
        if self._sound:
            self._sound.pause()

    def destroy(self):
        if self._hasSound:
            Bonfire.HackCount = 0
            self._hasSound = False
        if self._fire:
            self._fire.destroy()
        if self._smoke:
            self._smoke.destroy()
        if self._sound is not None:
            self._sound.pause()
        del self._fire
        del self._smoke
        del self._sound
        return
# okay decompiling .\pirates\effects\Bonfire.pyc
