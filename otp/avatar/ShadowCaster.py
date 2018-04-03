# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.avatar.ShadowCaster
from pandac.PandaModules import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShadowPlacer import ShadowPlacer
from otp.otpbase import OTPGlobals
globalDropShadowFlag = 1

def setGlobalDropShadowFlag(flag):
    global globalDropShadowFlag
    if flag != globalDropShadowFlag:
        globalDropShadowFlag = flag
        messenger.send('globalDropShadowFlagChanged')


globalDropShadowGrayLevel = 0.5

def setGlobalDropShadowGrayLevel(grayLevel):
    global globalDropShadowGrayLevel
    if grayLevel != globalDropShadowGrayLevel:
        globalDropShadowGrayLevel = grayLevel
        messenger.send('globalDropShadowGrayLevelChanged')


class ShadowCaster:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('ShadowCaster')

    def __init__(self, squareShadow=False):
        if squareShadow:
            self.shadowFileName = 'phase_3/models/props/square_drop_shadow'
        else:
            self.shadowFileName = 'phase_3/models/props/drop_shadow'
        self.dropShadow = None
        self.shadowPlacer = None
        self.activeShadow = 0
        self.wantsActive = 0
        if hasattr(base, 'wantDynamicShadows') and base.wantDynamicShadows:
            messenger.accept('globalDropShadowFlagChanged', self, self.__globalDropShadowFlagChanged)
            messenger.accept('globalDropShadowGrayLevelChanged', self, self.__globalDropShadowGrayLevelChanged)
        return

    def delete(self):
        if hasattr(base, 'wantDynamicShadows') and base.wantDynamicShadows:
            messenger.ignore('globalDropShadowFlagChanged', self)
            messenger.ignore('globalDropShadowGrayLevelChanged', self)
        self.deleteDropShadow()
        self.shadowJoint = None
        return

    def initializeDropShadow(self, hasGeomNode=True):
        self.deleteDropShadow()
        if hasGeomNode:
            self.getGeomNode().setTag('cam', 'caster')
        dropShadow = loader.loadModelCopy(self.shadowFileName)
        dropShadow.setScale(0.4)
        dropShadow.reparentTo(self.getShadowJoint())
        dropShadow.flattenMedium()
        dropShadow.setBillboardAxis(2)
        dropShadow.setColor(0.0, 0.0, 0.0, globalDropShadowGrayLevel, 1)
        self.shadowPlacer = ShadowPlacer(base.shadowTrav, dropShadow, OTPGlobals.WallBitmask, OTPGlobals.FloorBitmask)
        self.dropShadow = dropShadow
        if not globalDropShadowFlag:
            self.dropShadow.hide()
        self.setActiveShadow(self.wantsActive)

    def deleteDropShadow(self):
        if self.shadowPlacer:
            self.shadowPlacer.delete()
            self.shadowPlacer = None
        if self.dropShadow:
            self.dropShadow.removeNode()
            self.dropShadow = None
        return

    def setActiveShadow(self, isActive=1):
        self.wantsActive = isActive
        if self.shadowPlacer != None:
            isActive = isActive and globalDropShadowFlag
            if self.activeShadow != isActive:
                self.activeShadow = isActive
                if isActive:
                    self.shadowPlacer.on()
                else:
                    self.shadowPlacer.off()
        return

    def setShadowHeight(self, shadowHeight):
        if self.dropShadow:
            self.dropShadow.setZ(-shadowHeight)

    def getShadowJoint(self):
        if hasattr(self, 'shadowJoint'):
            return self.shadowJoint
        shadowJoint = self.find('**/attachShadow')
        if shadowJoint.isEmpty():
            self.shadowJoint = NodePath(self)
        else:
            self.shadowJoint = shadowJoint
        return self.shadowJoint

    def hideShadow(self):
        self.dropShadow.hide()

    def showShadow(self):
        if not globalDropShadowFlag:
            self.dropShadow.hide()
        else:
            self.dropShadow.show()

    def __globalDropShadowFlagChanged(self):
        if self.dropShadow != None:
            self.showShadow()
            self.setActiveShadow(self.wantsActive)
        return

    def __globalDropShadowGrayLevelChanged(self):
        if self.dropShadow != None:
            self.dropShadow.setColor(0.0, 0.0, 0.0, globalDropShadowGrayLevel, 1)
        return
# okay decompiling .\otp\avatar\ShadowCaster.pyc
