# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.CameraShaker
import random

from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *


class CameraShaker(NodePath):
    __module__ = __name__
    CutsceneScale = None
    TutorialInteriorScale = None

    def __init__(self):
        NodePath.__init__(self, 'CameraShakerRenderParent')
        self.shakeSpeed = 0.1
        self.shakePower = 5.0
        self.numShakes = 1.0
        self.scalePower = 0
        self.shakerNode = self.attachNewNode('shakerNode')

    @staticmethod
    def setCutsceneScale(scale):
        CameraShaker.CutsceneScale = scale

    @staticmethod
    def clearCutsceneScale():
        CameraShaker.CutsceneScale = None
        return

    @staticmethod
    def setTutorialInteriorScale(scale):
        CameraShaker.TutorialInteriorScale = scale

    @staticmethod
    def clearTutorialInteriorScale():
        CameraShaker.TutorialInteriorScale = None
        return

    def play(self, radius=10.0):
        if base.cam.getDistance(self.shakerNode) <= radius:
            if self.scalePower:
                self.shakePower = self.shakePower * (1 - base.localAvatar.getDistance(self.shakerNode) / radius)
            self.createTrack()
        else:
            self.removeNode()

    def createTrack(self):
        power = self.shakePower
        if CameraShaker.CutsceneScale is not None:
            power *= CameraShaker.CutsceneScale
        else:
            if CameraShaker.TutorialInteriorScale is not None:
                power *= CameraShaker.TutorialInteriorScale
        cameraRock1 = base.cam.hprInterval(self.shakeSpeed, Point3(power, power, 0), startHpr=Point3(0, 0, 0), blendType='easeInOut')
        cameraRock2 = base.cam.hprInterval(self.shakeSpeed, Point3(-power, -power, 0), startHpr=Point3(power, power, 0), blendType='easeInOut')
        cameraRock3 = base.cam.hprInterval(self.shakeSpeed, Point3(power, power, 0), startHpr=Point3(-power, -power, 0), blendType='easeInOut')
        cameraRock4 = base.cam.hprInterval(self.shakeSpeed, Point3(0, 0, 0), startHpr=Point3(power, power, 0), blendType='easeInOut')
        self.track = Sequence(cameraRock1)
        for i in range(self.numShakes):
            self.track.append(cameraRock2)
            self.track.append(cameraRock3)

        self.track.append(cameraRock4)
        self.track.append(Func(self.destroy))
        self.track.start()
        return

    def finish(self):
        if self.track:
            self.track.pause()
            self.track = None
        return

    def destroy(self):
        if self.track:
            self.track.finish()
            self.track = None
        self.removeNode()
        return
# okay decompiling .\pirates\effects\CameraShaker.pyc
