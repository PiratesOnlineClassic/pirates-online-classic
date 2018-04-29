# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.RoundshotProjectile
import random

from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from pirates.effects.EffectController import EffectController
from panda3d.core import *
from pirates.effects import PolyTrail
from pirates.piratesbase import PiratesGlobals
from pirates.effects.PooledEffect import PooledEffect


class RoundshotProjectile(EffectController, NodePath):
    
    motion_color = [
     Vec4(0.5, 0.6, 0.8, 1.0), Vec4(0.5, 0.6, 0.8, 1.0), Vec4(0.5, 0.6, 0.8, 1.0)]
    vertex_list = [
     Vec4(0.2, 0, 0.1, 1.0), Vec4(-0.2, 0, -0.1, 1.0), Vec4(0, 0, 0.2, 1.0)]

    def __init__(self):
        NodePath.__init__(self, 'RoundshotProjectile')
        EffectController.__init__(self)
        self.shot = loader.loadModel('models/ammunition/cannonball')
        self.shot.reparentTo(self)
        self.shot.setScale(0.35)
        self.motion_trail = PolyTrail.PolyTrail(None, self.vertex_list, self.motion_color)
        self.motion_trail.setUnmodifiedVertexColors(self.motion_color)
        self.motion_trail.motion_trail.geom_node_path.setTwoSided(False)
        self.motion_trail.reparentTo(self)
        self.motion_trail.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        return

    def createTrack(self, time, targetPos, motion_color, rate=1):
        throwTrack = LerpPosInterval(self, time, targetPos)
        if not motion_color:
            motion_color = self.motion_color
        self.motion_trail.setVertexColors(motion_color)
        fader = LerpColorScaleInterval(self.shot, time, Vec4(1.0, 1.0, 1.0, 0.0))
        movement = Sequence(Func(self.motion_trail.beginTrail), throwTrack, Func(self.motion_trail.endTrail))
        self.track = Sequence(Func(self.shot.setColorScale, Vec4(1, 1, 1, 1)), Parallel(movement, fader), Func(self.cleanUpEffect), Func(self.destroy))

    def play(self, time, targetPos, motion_color=None, rate=1):
        self.createTrack(time, targetPos, motion_color)
        self.track.start()

    def cleanUpEffect(self):
        self.detachNode()

    def destroy(self):
        self.stop()
        self.motion_trail.destroy()
        EffectController.destroy(self)
# okay decompiling .\pirates\effects\RoundshotProjectile.pyc
