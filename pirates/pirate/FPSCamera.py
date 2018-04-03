# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.FPSCamera
Instruction context:
-> 
 100     175  LOAD_FAST             0  'self'
            178  LOAD_ATTR            18  'setHpr'
            181  LOAD_CONST            1  0
            184  LOAD_CONST            1  0
            187  LOAD_CONST            1  0
            190  CALL_FUNCTION_3       3  None
            193  POP_TOP          
import math
from pandac.PandaModules import *
from direct.showbase.InputStateGlobal import inputState
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import reduceAngle, fitSrcAngle2Dest
from direct.showbase.PythonUtil import clampScalar, getSetter
from direct.showbase.PythonUtil import ParamObj
from direct.task import Task
from otp.otpbase import OTPGlobals
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

    def enterActive--- This code section failed: ---

  85       0  LOAD_GLOBAL           0  'CameraMode'
           3  LOAD_ATTR             0  'CameraMode'
           6  LOAD_ATTR             1  'enterActive'
           9  LOAD_FAST             0  'self'
          12  CALL_FUNCTION_1       1  None
          15  POP_TOP          

  87      16  LOAD_GLOBAL           3  'base'
          19  LOAD_ATTR             4  'camNode'
          22  LOAD_ATTR             5  'setLodCenter'
          25  LOAD_FAST             0  'self'
          28  LOAD_ATTR             6  'subject'
          31  CALL_FUNCTION_1       1  None
          34  POP_TOP          

  89      35  LOAD_FAST             0  'self'
          38  LOAD_ATTR             7  'reparentTo'
          41  LOAD_FAST             0  'self'
          44  LOAD_ATTR             6  'subject'
          47  CALL_FUNCTION_1       1  None
          50  POP_TOP          

  90      51  LOAD_FAST             0  'self'
          54  LOAD_ATTR             8  'setPos'
          57  LOAD_CONST            1  0
          60  LOAD_CONST            1  0
          63  LOAD_FAST             0  'self'
          66  LOAD_ATTR             9  'camOffset'
          69  LOAD_CONST            2  2
          72  BINARY_SUBSCR    
          73  CALL_FUNCTION_3       3  None
          76  POP_TOP          

  92      77  LOAD_GLOBAL          10  'camera'
          80  LOAD_ATTR             7  'reparentTo'
          83  LOAD_FAST             0  'self'
          86  CALL_FUNCTION_1       1  None
          89  POP_TOP          

  93      90  LOAD_GLOBAL          10  'camera'
          93  LOAD_ATTR            11  'setPosHpr'
          96  LOAD_FAST             0  'self'
          99  LOAD_ATTR             9  'camOffset'
         102  LOAD_CONST            1  0
         105  BINARY_SUBSCR    
         106  LOAD_FAST             0  'self'
         109  LOAD_ATTR             9  'camOffset'
         112  LOAD_CONST            3  1
         115  BINARY_SUBSCR    
         116  LOAD_CONST            1  0

  94     119  LOAD_CONST            1  0
         122  LOAD_CONST            1  0
         125  LOAD_CONST            1  0
         128  CALL_FUNCTION_6       6  None
         131  POP_TOP          

  95     132  LOAD_FAST             0  'self'
         135  LOAD_ATTR            12  '_initMaxDistance'
         138  CALL_FUNCTION_0       0  None
         141  POP_TOP          

  96     142  LOAD_FAST             0  'self'
         145  LOAD_ATTR            13  '_startCollisionCheck'
         148  CALL_FUNCTION_0       0  None
         151  POP_TOP          

  98     152  LOAD_GLOBAL           3  'base'
         155  LOAD_ATTR            14  'camLens'
         158  LOAD_ATTR            15  'setMinFov'
         161  LOAD_GLOBAL          16  'PiratesGlobals'
         164  LOAD_ATTR            17  'BattleCameraFov'
         167  CALL_FUNCTION_1       1  None
         170  POP_TOP          
         171  JUMP_FORWARD        228  'to 402'
         174  POP_TOP          

 100     175  LOAD_FAST             0  'self'
         178  LOAD_ATTR            18  'setHpr'
         181  LOAD_CONST            1  0
         184  LOAD_CONST            1  0
         187  LOAD_CONST            1  0
         190  CALL_FUNCTION_3       3  None
         193  POP_TOP          

 101     194  LOAD_GLOBAL          10  'camera'
         197  LOAD_ATTR            19  'wrtReparentTo'
         200  LOAD_FAST             0  'self'
         203  CALL_FUNCTION_1       1  None
         206  POP_TOP          

 102     207  LOAD_FAST             0  'self'
         210  LOAD_ATTR            20  'camIval'
         213  JUMP_IF_FALSE        17  'to 233'
       216_0  THEN                     234
         216  POP_TOP          

 103     217  LOAD_FAST             0  'self'
         220  LOAD_ATTR            20  'camIval'
         223  LOAD_ATTR            21  'pause'
         226  CALL_FUNCTION_0       0  None
         229  POP_TOP          
         230  JUMP_FORWARD          1  'to 234'
       233_0  COME_FROM           213  '213'
         233  POP_TOP          
       234_0  COME_FROM           230  '230'

 104     234  LOAD_GLOBAL          22  'Sequence'
         237  LOAD_GLOBAL          23  'Func'
         240  LOAD_FAST             0  'self'
         243  LOAD_ATTR            12  '_initMaxDistance'
         246  CALL_FUNCTION_1       1  None

 105     249  LOAD_GLOBAL          23  'Func'
         252  LOAD_FAST             0  'self'
         255  LOAD_ATTR            13  '_startCollisionCheck'
         258  CALL_FUNCTION_1       1  None

 106     261  LOAD_GLOBAL          23  'Func'
         264  LOAD_FAST             0  'self'
         267  LOAD_ATTR            24  'setForceMaxDistance'
         270  LOAD_GLOBAL          25  'False'
         273  CALL_FUNCTION_2       2  None

 107     276  LOAD_GLOBAL          10  'camera'
         279  LOAD_ATTR            26  'posHprInterval'
         282  LOAD_CONST            4  1.5

 108     285  LOAD_CONST            5  'pos'
         288  LOAD_GLOBAL          27  'Vec3'
         291  LOAD_FAST             0  'self'
         294  LOAD_ATTR             9  'camOffset'
         297  LOAD_CONST            1  0
         300  BINARY_SUBSCR    
         301  LOAD_FAST             0  'self'
         304  LOAD_ATTR             9  'camOffset'
         307  LOAD_CONST            3  1
         310  BINARY_SUBSCR    
         311  LOAD_CONST            1  0
         314  CALL_FUNCTION_3       3  None

 109     317  LOAD_CONST            6  'hpr'
         320  LOAD_GLOBAL          27  'Vec3'
         323  LOAD_CONST            1  0
         326  LOAD_CONST            1  0
         329  LOAD_CONST            1  0
         332  CALL_FUNCTION_3       3  None

 110     335  LOAD_CONST            7  'blendType'
         338  LOAD_CONST            8  'easeOut'
         341  CALL_FUNCTION_769   769  None

 112     344  LOAD_GLOBAL          23  'Func'
         347  LOAD_GLOBAL           3  'base'
         350  LOAD_ATTR            14  'camLens'
         353  LOAD_ATTR            15  'setMinFov'
         356  LOAD_GLOBAL          16  'PiratesGlobals'
         359  LOAD_ATTR            17  'BattleCameraFov'
         362  CALL_FUNCTION_2       2  None

 113     365  LOAD_GLOBAL          23  'Func'
         368  LOAD_FAST             0  'self'
         371  LOAD_ATTR            24  'setForceMaxDistance'
         374  LOAD_GLOBAL          28  'True'
         377  CALL_FUNCTION_2       2  None
         380  CALL_FUNCTION_6       6  None
         383  LOAD_FAST             0  'self'
         386  STORE_ATTR           20  'camIval'

 115     389  LOAD_FAST             0  'self'
         392  LOAD_ATTR            20  'camIval'
         395  LOAD_ATTR            29  'start'
         398  CALL_FUNCTION_0       0  None
         401  POP_TOP          
       402_0  COME_FROM           171  '171'

Parse error at or near `LOAD_FAST' instruction at offset 175

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
