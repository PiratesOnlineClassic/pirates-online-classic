from pandac.PandaModules import *
from direct.particles import ParticleEffect
from direct.actor import Actor
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
import os
import math

class ShipFog(NodePath):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipFog')

    def __init__(self, parent, psbskp, bin, binPriority, camera, renderParent = None, color = Vec4(1)):
        NodePath.__init__(self, 'ShipFog')
        self.assign(parent.attachNewNode('fog'))
        self.ival = None
        if renderParent:
            self.renderParent = renderParent
        else:
            self.renderParent = parent.attachNewNode('fog-renderParent')
        self.renderParent.setColorScale(color, 100)
        self.renderParent.setLightOff(base.cr.timeOfDayManager.dlight)
        self.frontRenderParent = self.renderParent.attachNewNode('frontRenderParent')
        self.frontRenderParent.setBin('fixed', bin + 1, binPriority)
        self.backRenderParent = self.renderParent.attachNewNode('backRenderParent')
        self.backRenderParent.setBin('fixed', bin - 1, binPriority)
        self.setupParticles(parent, psbskp, camera)

    def setupParticles(self, parent, psbskp, camera):
        particleSearchPath = DSearchPath()
        if __debug__:
            particleSearchPath.appendDirectory(Filename('../resources/phase_2/etc'))
        else:
            particleSearchPath.appendDirectory(Filename('/phase_2/etc'))

        pfile = Filename('shipFogWall.ptf')
        found = vfs.resolveFilename(pfile, particleSearchPath)
        if not found:
            self.notify.warning('loadParticleFile() - no path: %s' % pfile)
            return

        self.notify.debug('Loading particle file: %s' % pfile)
        center = Point2(psbskp[0] + psbskp[1], psbskp[2] + psbskp[3]) / 2
        minor = abs(center[0] - psbskp[0])
        major = abs(center[1] - psbskp[2])
        ratio = major / minor
        scale = 1.4
        lifespan = (psbskp[5] - psbskp[4]) / 50.0
        self.lifespan = lifespan
        cloudScale = max(abs(psbskp[3] - psbskp[2]) / 7.0, 20)
        normal = camera.getPos(parent)
        normal.setZ(0)
        normal.normalize()
        angle = math.atan2(normal[1], normal[0]) * 180 / math.pi
        limit = 30
        self.frontEffect = ParticleEffect.ParticleEffect('ShipFogFront')
        self.frontEffect.loadConfig(pfile)
        particleSystem = self.frontEffect.getParticlesNamed('particles-1')
        particleSystem.getRenderer().setTextureFromNode('models/misc/volcanoParticles', '**/volcanoSmoke')
        particleSystem.getRenderer().setInitialXScale(cloudScale)
        particleSystem.getRenderer().setInitialYScale(cloudScale)
        particleSystem.getFactory().setLifespanBase(lifespan)
        particleSystem.getEmitter().setRadius(minor)
        physicalNodePath = particleSystem.getPhysicalNodePath()
        physicalNodePath.setPos(center[0], center[1], 0)
        physicalNodePath.setScale(Vec3(1, ratio, 1) * scale)
        particleSystem.getEmitter().setArc((angle - 180) + limit, angle - limit)
        self.backEffect = ParticleEffect.ParticleEffect('ShipFogBack')
        self.backEffect.loadConfig(pfile)
        particleSystem = self.backEffect.getParticlesNamed('particles-1')
        particleSystem.getRenderer().setTextureFromNode('models/misc/volcanoParticles', '**/volcanoSmoke')
        particleSystem.getRenderer().setInitialXScale(cloudScale)
        particleSystem.getRenderer().setInitialYScale(cloudScale)
        particleSystem.getFactory().setLifespanBase(lifespan)
        particleSystem.getEmitter().setRadius(minor)
        physicalNodePath = particleSystem.getPhysicalNodePath()
        physicalNodePath.setPos(center[0], center[1], 0)
        physicalNodePath.setScale(Vec3(1, ratio, 1) * scale)
        particleSystem.getEmitter().setArc(angle + limit, angle - 180 - limit)

    def getParticleInterval(self, duration, fadeTime, rebuild = False):
        if rebuild:
            if self.ival:
                self.ival.finish()
                self.ival = None

        if not self.ival:
            self.ival = Parallel(ParticleInterval(self.frontEffect, self, worldRelative = 0, renderParent = self.frontRenderParent, duration = duration + self.lifespan, softStopT = -(self.lifespan)), ParticleInterval(self.backEffect, self, worldRelative = 0, renderParent = self.backRenderParent, duration = duration + self.lifespan, softStopT = -(self.lifespan)), Sequence(LerpFunc(self.renderParent.setAlphaScale, 1, fromData = 0.0, toData = 1.0), Wait((duration - 2) + self.lifespan), LerpFunc(self.renderParent.setAlphaScale, 1, fromData = 1.0, toData = 0.0)))

        return self.ival

    def delete(self):
        if self.ival:
            self.ival.finish()
            self.ival = None

        self.duration = 0.0
        if self.frontRenderParent:
            self.frontRenderParent.removeNode()
            self.frontRenderParent = None

        if self.backRenderParent:
            self.backRenderParent.removeNode()
            self.backRenderParent = None

        self.frontEffect.cleanup()
        self.frontEffect = None
        self.backEffect.cleanup()
        self.backEffect = None
        self.removeNode()
