# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.world.DistributedShipDeployer
import math

from direct.distributed.DistributedNode import DistributedNode
from direct.showbase.PythonUtil import report
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals


class DistributedShipDeployer(DistributedNode):
    __module__ = __name__

    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        NodePath.__init__(self, 'ShipDeployer')
        self.minRadius = 0
        self.spacing = 0
        self.maxRadius = 0
        self.heading = 0
        self.minSphere = None
        self.maxSphereSoft = None
        self.maxSphereHard = None
        self.deploySpheres = []
        self.outerBarrierState = True
        return

    @report(types=['frameCount', 'args'], dConfigParam='want-shipboard-report')
    def announceGenerate(self):
        DistributedNode.announceGenerate(self)
        self.reparentTo(self.getParentObj())
        self.createSpheres()
        self.enableDeploySpheres(False)
        self.accept(self.uniqueName('enterShipDeploySphere'), self.handleShipCollideEnter)
        self.accept(self.uniqueName('exitShipDeploySphere'), self.handleShipCollideExit)
        self.accept(self.uniqueName('enterShipDeploy-MaxSphereSoft'), self.handleShipEnterSoftBarrier)
        self.accept(self.uniqueName('exitShipDeploy-MaxSphereSoft'), self.handleShipExitSoftBarrier)
        self.accept(self.uniqueName('enterShipDeploy-MaxSphereHard'), self.handleShipEnterHardBarrier)
        self.accept(self.uniqueName('exitShipDeploy-MaxSphereHard'), self.handleShipExitHardBarrier)
        self.accept(self.uniqueName('enterShipDeploy-MinSphere'), self.handleShipEnterMinSphere)

    @report(types=['frameCount', 'args'], dConfigParam='want-shipboard-report')
    def disable(self):
        self.ignore(self.uniqueName('enterShipDeploySphere'))
        self.ignore(self.uniqueName('exitShipDeploySphere'))
        self.ignore(self.uniqueName('enterShipDeploy-MaxSphereSoft'))
        self.ignore(self.uniqueName('exitShipDeploy-MaxSphereSoft'))
        self.ignore(self.uniqueName('enterShipDeploy-MaxSphereHard'))
        self.ignore(self.uniqueName('exitShipDeploy-MaxSphereHard'))
        self.ignore(self.uniqueName('enterShipDeploy-MinSphere'))
        self.removeChildren()
        self.minSphere = None
        self.maxSphereSoft = None
        self.maxSphereHard = None
        self.deploySpheres = []
        DistributedNode.disable(self)
        return

    def delete(self):
        DistributedNode.delete(self)

    def setMinRadius(self, radius):
        self.minRadius = radius

    def setMaxRadius(self, radius):
        self.maxRadius = radius

    def setSpacing(self, spacing):
        self.spacing = spacing

    def setHeading(self, heading):
        self.heading = heading

    def d_shipEnteredSphere(self, shipId, sphereId):
        self.sendUpdate('shipEnteredSphere', [shipId, sphereId])

    def d_shipExitedSphere(self, shipId, sphereId):
        self.sendUpdate('shipExitedSphere', [shipId, sphereId])

    def d_shipExitedBarrier(self, shipId):
        self.sendUpdate('shipExitedBarrier', [shipId])

    @report(types=['frameCount', 'args'], dConfigParam='want-shipboard-report')
    def createSpheres(self):
        self.createMinSphere()
        self.createMaxSpheres()
        self.createDeploySpheres()

    def createMinSphere(self):
        cSphere = CollisionSphere(0, 0, 0, self.minRadius)
        cSphere.setTangible(1)
        cSphereNode = CollisionNode(self.uniqueName('ShipDeploy-MinSphere'))
        cSphereNode.setFromCollideMask(BitMask32.allOff())
        cSphereNode.setIntoCollideMask(PiratesGlobals.ShipCollideBitmask)
        cSphereNode.addSolid(cSphere)
        self.minSphere = self.attachNewNode(cSphereNode)

    def createMaxSpheres(self):
        cSphere = CollisionSphere(0, 0, 0, self.maxRadius)
        cSphere.setTangible(0)
        cSphereNode = CollisionNode(self.uniqueName('ShipDeploy-MaxSphereSoft'))
        cSphereNode.setFromCollideMask(BitMask32.allOff())
        cSphereNode.setIntoCollideMask(PiratesGlobals.ShipCollideBitmask)
        cSphereNode.addSolid(cSphere)
        self.maxSphereSoft = self.attachNewNode(cSphereNode)
        cSphere = CollisionSphere(0, 0, 0, self.maxRadius)
        cSphere.setTangible(1)
        cSphereNode = CollisionNode(self.uniqueName('ShipDeploy-MaxSphereHard'))
        cSphereNode.setFromCollideMask(BitMask32.allOff())
        cSphereNode.setIntoCollideMask(PiratesGlobals.ShipDeployBitmask)
        cSphereNode.addSolid(cSphere)
        self.maxSphereHard = self.attachNewNode(cSphereNode)

    def createDeploySpheres(self):
        deployRingRadius = self.minRadius + self.spacing / 2.0
        C = 2 * math.pi * deployRingRadius
        numSpheres = int(C / self.spacing)
        stepAngle = 360.0 / numSpheres

        def getSpherePos(sphereId):
            h = sphereId * stepAngle + 90.0 + self.heading
            angle = h * math.pi / 180.0
            pos = Point3(math.cos(angle), math.sin(angle), 0) * deployRingRadius
            return pos

        for x in xrange(numSpheres):
            pos = getSpherePos(x)
            cSphere = CollisionSphere(pos[0], pos[1], pos[2], self.spacing / 2.0)
            cSphere.setTangible(0)
            cSphereNode = CollisionNode(self.uniqueName('ShipDeploySphere'))
            cSphereNode.addSolid(cSphere)
            cSphereNode.setFromCollideMask(BitMask32.allOff())
            cSphereNode.setIntoCollideMask(PiratesGlobals.ShipCollideBitmask)
            sphere = self.attachNewNode(cSphereNode)
            sphere.setTag('deploySphereId', `x`)
            self.deploySpheres.append(sphere)

    def showSpheres(self):
        self.minSphere.show()
        self.maxSphereSoft.show()
        self.maxSphereHard.show()
        for sphere in self.deploySpheres:
            sphere.show()

    def hideSpheres(self):
        self.minSphere.hide()
        self.maxSphereSoft.hide()
        self.maxSphereHard.hide()
        for sphere in self.deploySpheres:
            sphere.hide()

    def handleShipCollideEnter(self, colEntry):
        shipId = colEntry.getFromNodePath().getNetTag('shipId')
        shipId = int(shipId)
        sphereId = colEntry.getIntoNodePath().getNetTag('deploySphereId')
        sphereId = int(sphereId)
        self.d_shipEnteredSphere(shipId, sphereId)
        for sphere in self.deploySpheres:
            sphere.stash()

        padding = 3
        numSpheres = len(self.deploySpheres)
        for sphere in (s % numSpheres for s in xrange(sphereId - padding, sphereId + padding + 1)):
            self.deploySpheres[sphere].unstash()

    def handleShipCollideExit(self, colEntry):
        shipId = colEntry.getFromNodePath().getNetTag('shipId')
        shipId = int(shipId)
        sphereId = colEntry.getIntoNodePath().getNetTag('deploySphereId')
        sphereId = int(sphereId)
        self.d_shipExitedSphere(shipId, sphereId)

    @report(types=['frameCount', 'args'], dConfigParam='want-shipboard-report')
    def handleShipEnterMinSphere(self, colEntry):
        if localAvatar.ship and localAvatar.ship.steeringAvId == localAvatar.doId:
            localAvatar.guiMgr.createWarning(PLocalizer.CoralReefWarning, PiratesGuiGlobals.TextFG6)

    @report(types=['frameCount', 'args'], dConfigParam='want-shipboard-report')
    def handleShipEnterSoftBarrier(self, colEntry):
        shipId = colEntry.getFromNodePath().getNetTag('shipId')
        shipId = int(shipId)
        ship = base.cr.doId2do.get(shipId)
        if ship and not ship.getRespectDeployBarriers():
            self.enableDeploySpheres(True)

    @report(types=['frameCount', 'args'], dConfigParam='want-shipboard-report')
    def handleShipExitSoftBarrier(self, colEntry):
        shipId = colEntry.getFromNodePath().getNetTag('shipId')
        shipId = int(shipId)
        ship = base.cr.doId2do.get(shipId)
        if ship and not ship.getRespectDeployBarriers():
            self.enableDeploySpheres(False)
            self.d_shipExitedBarrier(shipId)

    @report(types=['frameCount', 'args'], dConfigParam='want-shipboard-report')
    def handleShipEnterHardBarrier(self, colEntry):
        if localAvatar.ship and localAvatar.ship.steeringAvId == localAvatar.doId:
            localAvatar.guiMgr.createWarning(PLocalizer.CoralReefWarning, PiratesGuiGlobals.TextFG6)

    @report(types=['frameCount', 'args'], dConfigParam='want-shipboard-report')
    def handleShipExitHardBarrier(self, colEntry):
        pass

    @report(types=['frameCount', 'args'], dConfigParam='want-shipboard-report')
    def enableDeploySpheres(self, enable):
        if base.config.GetBool('want-shipboard-report', 0):
            self.showSpheres()
        if enable:
            for sphere in self.deploySpheres:
                sphere.unstash()

        for sphere in self.deploySpheres:
            sphere.stash()
# okay decompiling .\pirates\world\DistributedShipDeployer.pyc
