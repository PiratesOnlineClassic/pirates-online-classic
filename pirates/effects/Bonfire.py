from panda3d.core import *
from direct.interval.IntervalGlobal import *
from pirates.effects.Fire import Fire
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.piratesgui.GameOptions import Options

class Bonfire(NodePath):
    HackCount = 0
    
    def __init__(self, parent = None):
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
            self._sound = SoundInterval(base.loader.loadSfx('audio/bonfire.wav'), node = self, volume = 0.5)
        else:
            self._hasSound = False

    def disableSound(self):
        self._sound.pause()
        self._sound = None

    def startLoop(self, lod = Options.SpecialEffectsHigh):
        if self._fire:
            self._fire.startLoop(lod)
        
        if self._smoke and lod >= Options.SpecialEffectsHigh:
            self._smoke.startLoop(lod)
        
        if self._sound is not None:
            self._sound.loop(stagger = True)

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


