from direct.showbase import DirectObject
from direct.fsm import ClassicFSM, State
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import reduceAngle, fitSrcAngle2Dest, clampScalar, lerp, Functor
from direct.showbase.InputStateGlobal import inputState
from panda3d.core import *
from otp.otpbase import OTPGlobals
from pirates.pirate.OrbitCamera import OrbitCamera
import math

class ShipCamera(OrbitCamera):
    
    class ParamSet(OrbitCamera.ParamSet):
        Params = {}
    
    def getName(self):
        return 'Orbit'

    def _getTopNodeName(self):
        return 'ShipCam'

    def _handleWheelUp(self):
        self.setIdealDistance(self.idealDistance - (self._maxDistance - self._minDistance) * 0.2)
        self.applyIdealDistance()
    
    def _handleWheelDown(self):
        self.setIdealDistance(self.idealDistance + (self._maxDistance - self._minDistance) * 0.2)
        self.applyIdealDistance()
    
    def _startCollisionCheck(self):
        OrbitCamera._startCollisionCheck(self, shipBarrier = 1)

    def enterActive(self):
        OrbitCamera.enterActive(self)
        self.accept('wheel_up', self._handleWheelUp)
        self.accept('wheel_down', self._handleWheelDown)
        self._scInputState = ScratchPad()
        self._scInputState.rmbPressed = False
        self._scInputState.fwdPressed = False
        self._scInputListener = DirectObject.DirectObject()
        self._scInputListener.accept(inputState.getEventName('RMB'), self._handleRmbEvent)
        self._handleRmbEvent(inputState.isSet('RMB'))
        self._scInputListener.accept(inputState.getEventName('forward'), self._handleForwardEvent)
        self._handleForwardEvent(inputState.isSet('forward'))
    
    def exitActive(self):
        OrbitCamera.exitActive(self)
        self.ignore('wheel_up')
        self.ignore('wheel_down')
        self._scInputListener.ignoreAll()
        del self._scInputListener
        del self._scInputState
    
    def _startMouseControlTasks(self):
        OrbitCamera._startMouseControlTasks(self)
        if self.mouseControl:
            self._lockAtRear = False

    def _handleRmbEvent(self, pressed):
        if pressed and not self._scInputState.rmbPressed:
            self._disableRotateToRear()
        
        self._scInputState.rmbPressed = pressed
    
    def _handleForwardEvent(self, pressed):
        if pressed and not self._scInputState.fwdPressed:
            if not self._scInputState.rmbPressed:
                self._enableRotateToRear()

        self._scInputState.fwdPressed = pressed
    
    def _stopMouseControlTasks(self):
        OrbitCamera._stopMouseControlTasks(self)
    
    def _mouseUpdateTask(self, task):
        if OrbitCamera._mouseUpdateTask(self, task) == task.cont and self.mouseDelta[0] or self.mouseDelta[1]:
            sensitivity = 0.5
            self.setRotation(self.getRotation() - self.mouseDelta[0] * sensitivity)
            self.setEscapement(clampScalar(self.escapement + self.mouseDelta[1] * sensitivity * 0.6, self._minEsc, self._maxEsc))
        
        return task.cont


