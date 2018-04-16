# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.movement.Mover
import __builtin__

from direct.directnotify import DirectNotifyGlobal
from direct.showbase import PythonUtil
from otp.movement.PyVec3 import PyVec3
from panda3d.core import *


class Mover:
    
    notify = DirectNotifyGlobal.directNotify.newCategory('Mover')
    SerialNum = 0
    Profile = 0
    Pstats = 1
    PSCCpp = 'App:Show code:moveObjects:MoverC++'
    PSCPy = 'App:Show code:moveObjects:MoverPy'
    PSCInt = 'App:Show code:moveObjects:MoverIntegrate'

    def __init__(self, objNodePath, fwdSpeed=1, rotSpeed=1):
        self.serialNum = Mover.SerialNum
        Mover.SerialNum += 1
        self.VecType = Vec3
        self.impulses = {}
        if Mover.Pstats:
            self.pscCpp = PStatCollector(Mover.PSCCpp)
            self.pscPy = PStatCollector(Mover.PSCPy)
            self.pscInt = PStatCollector(Mover.PSCInt)

    def destroy(self):
        for name, impulse in self.impulses.items():
            self.notify.debug('removing impulse: %s' % name)
            self.removeImpulse(name)

    def addImpulse(self, name, impulse):
        self.impulses[name] = impulse
        impulse._setMover(self)

    def removeImpulse(self, name):
        if name not in self.impulses:
            self.notify.warning("Mover.removeImpulse: unknown impulse '%s'" % name)
            return

        self.impulses[name]._clearMover(self)
        del self.impulses[name]

    def getCollisionEventName(self):
        return 'moverCollision-%s' % self.serialNum

    def move(self, dt=-1, profile=0):
        if self.Profile and not profile:

            def func(doMove=self.move):
                for i in xrange(10000):
                    doMove(dt, profile=1)

            __builtin__.func = func
            PythonUtil.startProfile(cmd='func()', filename='profile', sorts=['cumulative'], callInfo=0)
            del __builtin__.func
            return

        if self.Pstats:
            self.pscCpp.start()

        if self.Pstats:
            self.pscCpp.stop()
            self.pscPy.start()

        for impulse in self.impulses.values():
            impulse._process(self.getDt())

        if self.Pstats:
            self.pscPy.stop()
            self.pscInt.start()

        if self.Pstats:
            self.pscInt.stop()
# okay decompiling .\otp\movement\Mover.pyc
