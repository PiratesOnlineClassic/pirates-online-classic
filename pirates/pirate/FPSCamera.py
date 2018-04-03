# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.FPSCamera
import math

from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.PythonUtil import (ParamObj, clampScalar,
                                        fitSrcAngle2Dest, getSetter,
                                        reduceAngle)
from direct.task import Task
from otp.otpbase import OTPGlobals
from pandac.PandaModules import *
from pirates.pirate import CameraMode
from pirates.piratesbase import PiratesGlobals


class FPSCamera(CameraMode.CameraMode, NodePath, ParamObj):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('FPSCamera')

    class ParamSet(ParamObj.ParamSet):
        __module__ = __name__
        Params = {'camOffset': Vec3(0, -14, 5.5)}

    UpdateTaskName = 'FPSCamUpdateTask'
    ReadMouseTaskName = 'FPSCamReadMouseTask'
    CollisionCheckTaskName = 'FPSCamCollisionTask'
    MinP = -50
    MaxP = 20
    baseH = None
    minH = None
    maxH = None
    SensitivityH = base.config.GetFloat('fps-cam-sensitivity-x', 0.2)
    SensitivityP = base.config.GetFloat('fps-cam-sensitivity-y', 0.1)

    def __init__(self, subject, params=None):
        ParamObj.__init__(self)
        NodePath.__init__(self, 'fpsCam')
        CameraMode.CameraMode.__init__(self)
        self.subject = subject
        self.mouseX = 0.0
        self.mouseY = 0.0
        self._paramStack = []
        self._hadMouse = False
        if params is None:
            self.setDefaultParams()
        else:
            params.applyTo(self)
        self.zIval = None
        self.camIval = None
        self.forceMaxDistance = True
        return

    def destroy(self):
        if self.zIval:
            self.zIval.finish()
            self.zIval = None
        if self.camIval:
            self.camIval.finish()
            self.camIval = None
        del self.subject
        NodePath.removeNode(self)
        ParamObj.destroy(self)
        CameraMode.CameraMode.destroy(self)
        return

    def getName(self):
        return 'FPS'

    def _getTopNodeName(self):
        return 'FPSCam'

    def enterActive(self):
        CameraMode.CameraMode.enterActive(self)
        base.camNode.setLodCenter(self.subject)
        if base.wantEnviroDR:
            base.enviroCamNode.setLodCenter(self.subject)

        self.reparentTo(self.subject)
        self.setPos(0, 0, self.camOffset[2])
        camera.reparentTo(self)
        camera.setPosHpr(self.camOffset[0], self.camOffset[1], 0, 0, 0, 0)
        self._initMaxDistance()
        self._startCollisionCheck()
        base.camLens.setMinFov(PiratesGlobals.BattleCameraFov)

    def _initMaxDistance(self):
        self._maxDistance = abs(self.camOffset[1])

    def exitActive(self):
        if self.camIval:
            self.camIval.finish()
            self.camIval = None
        self._stopCollisionCheck()
        base.camNode.setLodCenter(NodePath())
        CameraMode.CameraMode.exitActive(self)
        return

    def enableMouseControl(self):
        CameraMode.CameraMode.enableMouseControl(self)
        self.subject.controlManager.setWASDTurn(0)

    def disableMouseControl(self):
        CameraMode.CameraMode.disableMouseControl(self)
        self.subject.controlManager.setWASDTurn(1)

    def isSubjectMoving(self):
        if 'localAvatar' in __builtins__:
            autoRun = localAvatar.getAutoRun()
        else:
            autoRun = False
        return (inputState.isSet('forward') or inputState.isSet('reverse') or inputState.isSet('turnRight') or inputState.isSet('turnLeft') or inputState.isSet('slideRight') or inputState.isSet('slideLeft') or autoRun) and self.subject.controlManager.isEnabled

    def isWeaponEquipped(self):
        return self.subject.isWeaponDrawn

    def _avatarFacingTask(self, task):
        if hasattr(base, 'oobeMode') and base.oobeMode:
            return task.cont
        if self.isSubjectMoving() or self.isWeaponEquipped():
            camH = self.getH(render)
            subjectH = self.subject.getH(render)
            if abs(camH - subjectH) > 0.01:
                self.subject.setH(render, camH)
                self.setH(0)
        return task.cont

    def _mouseUpdateTask(self, task):
        if hasattr(base, 'oobeMode') and base.oobeMode:
            return task.cont
        if base.mouseWatcherNode.hasMouse():
            self.cTravOnFloor.traverse(render)
        subjectMoving = self.isSubjectMoving()
        subjectTurning = (inputState.isSet('turnRight') or inputState.isSet('turnLeft')) and self.subject.controlManager.isEnabled
        weaponEquipped = self.isWeaponEquipped()
        if subjectMoving or weaponEquipped:
            hNode = self.subject
        else:
            hNode = self
        if self.mouseDelta[0] or self.mouseDelta[1]:
            dx, dy = self.mouseDelta
            if subjectTurning:
                dx = 0
            if hasattr(base, 'options') and base.options.mouse_look:
                dy = -dy
            hNode.setH(hNode, -dx * self.SensitivityH)
            curP = self.getP()
            newP = curP + -dy * self.SensitivityP
            newP = min(max(newP, self.MinP), self.MaxP)
            self.setP(newP)
            if self.baseH:
                messenger.send('pistolMoved')
                self._checkHBounds(hNode)
            self.setR(render, 0)
        return task.cont

    def setHBounds(self, baseH, minH, maxH):
        self.baseH = baseH
        self.minH = minH
        self.maxH = maxH
        if self.isSubjectMoving() or self.isWeaponEquipped():
            hNode = self.subject
        else:
            hNode = self
        hNode.setH(maxH)

    def clearHBounds(self):
        self.baseH = self.minH = self.maxH = None
        return

    def _checkHBounds(self, hNode):
        currH = fitSrcAngle2Dest(hNode.getH(), 180)
        if currH < self.minH:
            hNode.setH(reduceAngle(self.minH))
        else:
            if currH > self.maxH:
                hNode.setH(reduceAngle(self.maxH))

    def acceptWheel(self):
        self.accept('wheel_up', self._handleWheelUp)
        self.accept('wheel_down', self._handleWheelDown)
        self._resetWheel()

    def ignoreWheel(self):
        self.ignore('wheel_up')
        self.ignore('wheel_down')
        self._resetWheel()

    def _handleWheelUp(self):
        y = self.camOffset[1]
        y = max(-14, min(-2, y + 1.0))
        self._collSolid.setPointB(0, y + 1, 0)
        self.camOffset.setY(y)
        inZ = localAvatar.headNode.getZ()
        outZ = self.camOffset[2]
        t = (-14 - y) / -12
        z = lerp(outZ, inZ, t)
        self.setZ(z)

    def _handleWheelDown(self):
        y = self.camOffset[1]
        y = max(-14, min(-2, y - 1.0))
        self._collSolid.setPointB(0, y + 1, 0)
        self.camOffset.setY(y)
        inZ = localAvatar.headNode.getZ()
        outZ = self.camOffset[2]
        t = (-14 - y) / -12
        z = lerp(outZ, inZ, t)
        self.setZ(z)

    def _resetWheel(self):
        self.camOffset = Vec3(0, -14, 5.5)
        y = self.camOffset[1]
        z = self.camOffset[2]
        self._collSolid.setPointB(0, y + 1, 0)
        self.setZ(z)

    def getCamOffset(self):
        return self.camOffset

    def setCamOffset(self, camOffset):
        self.camOffset = Vec3(camOffset)

    def applyCamOffset(self):
        if self.isActive():
            camera.setPos(self.camOffset)

    def _setCamDistance(self, distance):
        offset = camera.getPos(self)
        offset.normalize()
        camera.setPos(self, offset * distance)

    def _getCamDistance(self):
        return camera.getPos(self).length()

    def _startCollisionCheck(self):
        self._collSolid = CollisionSegment(0, 0, 0, 0, -(self._maxDistance + 1.0), 0)
        collSolidNode = CollisionNode('FPSCam.CollSolid')
        collSolidNode.addSolid(self._collSolid)
        collSolidNode.setFromCollideMask(OTPGlobals.CameraBitmask | OTPGlobals.CameraTransparentBitmask | OTPGlobals.FloorBitmask)
        collSolidNode.setIntoCollideMask(BitMask32.allOff())
        self._collSolidNp = self.attachNewNode(collSolidNode)
        self._cHandlerQueue = CollisionHandlerQueue()
        self._cTrav = CollisionTraverser('FPSCam.cTrav')
        self._cTrav.addCollider(self._collSolidNp, self._cHandlerQueue)
        taskMgr.add(self._collisionCheckTask, FPSCamera.CollisionCheckTaskName, priority=45)

    def _collisionCheckTask(self, task=None):
        if hasattr(base, 'oobeMode'):
            return Task.cont
        self._cTrav.traverse(render)
        if self._cHandlerQueue.getNumEntries() > 0:
            self._cHandlerQueue.sortEntries()
            collEntry = self._cHandlerQueue.getEntry(0)
            cPoint = collEntry.getSurfacePoint(self)
            cNormal = collEntry.getSurfaceNormal(self)
            offset = 0.9
            camera.setPos(cPoint + cNormal * offset)
            distance = camera.getDistance(self)
            if distance < 1.8:
                self.subject.getGeomNode().hide()
            else:
                self.subject.getGeomNode().show()
        else:
            if self.forceMaxDistance:
                camera.setPos(self.camOffset)
                camera.setZ(0)
            self.subject.getGeomNode().show()
        return Task.cont

    def _stopCollisionCheck(self):
        taskMgr.remove(FPSCamera.CollisionCheckTaskName)
        self._cTrav.removeCollider(self._collSolidNp)
        del self._cHandlerQueue
        del self._cTrav
        self._collSolidNp.detachNode()
        del self._collSolidNp
        self.subject.getGeomNode().show()

    def lerpFromZOffset(self, z=0.0, duration=1):
        if self.zIval:
            self.zIval.finish()
        self.zIval = LerpFunc(self.setZ, duration, fromData=z + self.camOffset[2], toData=self.camOffset[2])
        self.zIval.start()
        self.zIval.setT(0)

    def avFaceCamera(self):
        if not self.mouseControl:
            camH = self.getH(render)
            subjectH = self.subject.getH(render)
            if abs(camH - subjectH) > 0.01:
                self.subject.setH(render, camH)
                self.setH(0)

    def setForceMaxDistance(self, force):
        self.forceMaxDistance = force
