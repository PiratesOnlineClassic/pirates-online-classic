# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.SoundFX
import random

from direct.task import Task
from pandac.PandaModules import *


class SoundFX(NodePath):

    def __init__(self,
                 sfxFile,
                 volume=0.5,
                 looping=True,
                 delayMin=0,
                 delayMax=0,
                 pos=None,
                 hpr=None,
                 parent=None,
                 listenerNode=None,
                 taskName='playSfx',
                 drawIcon=False):
        NodePath.NodePath.__init__(self, 'soundFX')
        self.volume = volume
        self.looping = looping
        self.delayMin = delayMin
        self.delayMax = delayMax
        self.listenerNode = listenerNode
        self.taskName = taskName
        self.drawIcon = drawIcon
        self.models = []
        self.delayStartT = 0
        self.currentDelay = 0
        if parent == None:
            parent = render
        self.reparentTo(parent)
        if pos == None:
            pos = VBase3(0, 0, 0)
        self.setPos(pos)
        if hpr == None:
            hpr = VBase3(0, 0, 0)
        self.setHpr(hpr)
        if sfxFile:
            self.sfx = base.loader.loadSfx(sfxFile)
            self.playSfx(taskName)
        else:
            self.sfx = None
            self.isPlaying = False
        self.task = None
        if self.drawIcon:
            newModel = loader.loadModelCopy('models/misc/smiley')
            newModel.setColor(0, 0.65, 0, 1)
            newModel.reparentTo(self)
            self.models.append(newModel)
        return

    def startPlaying(self, taskName=None):
        self.isPlaying = True
        self.stopPlaying()
        if taskName is None:
            taskName = self.taskName
        base.sfxPlayer.playSfx(
            sfx=self.sfx,
            volume=self.volume,
            node=self,
            listenerNode=self.listenerNode)
        self.delayStartT = 0
        if self.looping:
            self.currentDelay = random.uniform(self.delayMin, self.delayMax)
            self.task = Task.Task(self.playSfx)
            taskMgr.add(self.task, taskName)
        self.setTaskName(taskName)
        return

    def playSfx(self, task):
        if self.sfx.status() == 1:
            if self.delayStartT == 0:
                self.delayStartT = globalClock.getFrameTime()
            stopT = globalClock.getFrameTime()
            deltaT = stopT - self.delayStartT
            if deltaT >= self.currentDelay:
                base.sfxPlayer.playSfx(
                    sfx=self.sfx,
                    volume=self.volume,
                    node=self,
                    listenerNode=self.listenerNode)
                self.delayStartT = 0
                self.currentDelay = random.uniform(self.delayMin, self.delayMax)
        return Task.cont

    def setSfxFile(self, sfxFile):
        if self.sfx:
            del self.sfx
        self.sfx = base.loader.loadSfx(sfxFile)

    def setVolume(self, volume):
        self.volume = volume

    def setLooping(self, looping):
        self.looping = looping

    def setDelayMin(self, delayMin):
        self.delayMin = delayMin

    def setDelayMax(self, delayMax):
        self.delayMax = delayMax

    def setListenerNode(self, listenerNode):
        self.listenerNode = listenerNode

    def setTaskName(self, taskName):
        self.taskName = taskName

    def stopPlaying(self):
        if self.task:
            taskMgr.remove(self.task.name)
        if taskMgr.hasTaskNamed(self.taskName):
            taskMgr.remove(self.taskName)


# okay decompiling .\pirates\effects\SoundFX.pyc
