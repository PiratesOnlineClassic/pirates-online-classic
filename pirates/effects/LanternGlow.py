from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from EffectController import EffectController
import random

class LanternGlow(DirectObject, EffectController, NodePath):
    
    def __init__(self, newParent = render, billboardOffset = 1.0):
        NodePath.__init__(self, 'LanternGlow')
        EffectController.__init__(self)
        self.newParent = newParent
        self.setColorScaleOff()
        self.setBillboardPointEye(billboardOffset)
        self.glow = NodePath(SequenceNode('lanternGlow'))
        glowCard = loader.loadModel('models/effects/lanternGlow').getChild(0)
        self.glowCards = []
        level = [
            15,
            15.5,
            16,
            16.5,
            17,
            17.5,
            18,
            17.5,
            17,
            16.5,
            16,
            15.5,
            15]
        index = random.randint(0, len(level))
        level = level[index:-1] + level[0:index]
        for i in level:
            for j in xrange(random.choice([1, 2, 3, 4])):
                newGlow = glowCard.copyTo(self.glow)
                newGlow.setScale(i)
                self.glowCards.append(newGlow)

        self.glow.node().setFrameRate(len(self.glowCards * 2) * random.choice([
            0.8,
            0.9,
            1,
            1.1,
            1.2]))
        self.glow.node().setPlayRate(1)
        self.glow.node().loop(1)
        self.glow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.glow.setDepthWrite(0)
        self.glow.setFogOff()
        self.glow.setLightOff()
        self.glow.setBin('fixed', 120)
        self.glow.setColorScale(0.5, 0.5, 0.5, 1)
        self.glow.reparentTo(self)
        self.startScale = 15
        self.endScale = 18
        self.period = 0.2
        self.glow.node().setAttrib(ColorWriteAttrib.make(ColorWriteAttrib.CRed | ColorWriteAttrib.CGreen | ColorWriteAttrib.CBlue))

    def createTrack(self, lod = None):
        randomness = random.random() / 20
        scaleUp = self.glow.scaleInterval(self.period + randomness, self.endScale, startScale = self.startScale, blendType = 'easeInOut', other = render)
        scaleDown = self.glow.scaleInterval(self.period + randomness, self.startScale, startScale = self.endScale, blendType = 'easeInOut', other = render)
        self.startEffect = Sequence(scaleUp, scaleDown)
        self.endEffect = None
        self.track = self.startEffect
        self.accept('toggleGlows', self.toggleGlows)

    def destroy(self):
        self.ignore('toggleGlows')
        if self.glow:
            self.glow.removeNode()
            self.glow = None
        
        self.glowCards = None
        EffectController.destroy(self)

    def toggleGlows(self):
        if self.glow.isStashed():
            self.glow.unstash()
        else:
            self.glow.stash()
    
    def setupShaders(self):
        LanternGlow.shaders = {
            'lantern': loader.loadShader('models/misc/ship_lantern.cg')}

    def enableShaders(self):
        if 1:
            if self.glow and not self.glow.isEmpty():
                self.glow.setShaderOff()

        elif not self.isEmpty() and hasattr(self, 'glow'):
            LanternGlow.setupShaders(self)
            self.shaderNp = self.glow
            if not taskMgr.hasTaskNamed('LanternColorScale'):

                def lanternColorScaleTask(task):
                    if task.shaderCount > 0:
                        if hasattr(self, 'glow'):
                            render.setShaderInput('lanternColorScale', Vec4(self.glow.getColorScale()))

                        return Task.cont
                    else:
                        render.clearShaderInput('lanternColorScale')
                        render.clearAttrib(ShaderAttrib.getClassType())
                        return Task.done

                t = taskMgr.add(lanternColorScaleTask, 'LanternColorScale')
                t.shaderCount = 0

            tList = taskMgr.getTasksNamed('LanternColorScale')
            tList[0].shaderCount += 1

    def disableShaders(self):
        if 1:
            if self.glow and not self.glow.isEmpty():
                self.glow.clearShader()
                self.glow.clearAttrib(ShaderAttrib.getClassType())

        elif hasattr(self, 'shaderNp'):
            self.shaderNp.clearShader()
            self.shaderNp.clearAttrib(ShaderAttrib.getClassType())
            tList = taskMgr.getTasksNamed('LanternColorScale')
            tList[0].shaderCount -= 1
            del self.shaderNp
        


