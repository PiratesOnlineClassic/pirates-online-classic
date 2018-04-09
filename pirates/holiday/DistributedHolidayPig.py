# uncompyle6 version 3.1.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (default, Mar  9 2018, 23:57:12) 
# [GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)]
# Embedded file name: pirates.holiday.DistributedHolidayPig
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.uberdog.RejectCode import RejectCode
from pirates.holiday.DistributedHolidayObject import DistributedHolidayObject
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.effects.SmallFire import SmallFire

class DistributedHolidayPig(DistributedHolidayObject):
    __module__ = __name__

    def __init__(self, cr):
        DistributedHolidayObject.__init__(self, cr, proximityText=PLocalizer.InteractHolidayPig)
        self.pigRoasting = False
        self.fireEffect = None
        self.pigInterval = None
        self.pigModel = None
        return

    def delete(self):
        if self.pigInterval:
            self.pigInterval.finish()
            self.pigInterval = None
        if self.pigModel:
            self.pigModel.removeNode()
        if self.fireEffect:
            self.fireEffect.stopLoop()
            self.fireEffect = None
        DistributedHolidayObject.delete(self)
        return

    def setPigRoasting(self, value=False):
        self.pigRoasting = value
        if self.pigRoasting:
            self.startRoastingPig()
        else:
            self.stopRoastingPig()

    def getPigRoasting(self):
        return self.pigRoasting

    def acceptInteraction(self):
        DistributedHolidayObject.acceptInteraction(self)
        base.cr.interactionMgr.stop()

    def rejectInteraction(self):
        DistributedHolidayObject.rejectInteraction(self)
        localAvatar.guiMgr.createWarning(PLocalizer.NoPigRoasting)

    def startRoastingPig(self):
        self.pigModel = loader.loadModel('models/props/pir_m_prp_foo_barbecuepig')
        self.pigModel.setTransparency(1)
        self.pigModel.reparentTo(self)
        self.pigInterval = LerpColorScaleInterval(self.pigModel, 2.0, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0))
        self.fireEffect = SmallFire()
        if self.fireEffect:
            self.fireEffect.reparentTo(self)
            self.fireEffect.setScale(Vec3(1.5, 1, 1))
            self.fireEffect.startLoop()
        self.pigInterval.start()

    def stopRoastingPig(self):
        if self.pigModel:
            self.pigInterval = LerpColorScaleInterval(self.pigModel, 2.0, Vec4(1, 1, 1, 0), startColorScale=Vec4(1, 1, 1, 1))
            self.pigInterval.start()
        if self.fireEffect:
            self.fireEffect.stopLoop()
            self.fireEffect = None
        return

    def makeTradeResponse(self, result):
        if result == 0:
            localAvatar.guiMgr.createWarning(PLocalizer.TradeItemFullWarning, PiratesGuiGlobals.TextFG6)
        else:
            if result == 1:
                localAvatar.guiMgr.messageStack.addModalTextMessage(PLocalizer.PorkChunkReceived, seconds=10, icon=('pork',
                                                                                                                    ''))
                localAvatar.guiMgr.combatTray.tonicButton.getBestTonic()
                localAvatar.guiMgr.weaponPage.updateTonics()
            else:
                localAvatar.guiMgr.createWarning(PLocalizer.TradeFailedWarning, PiratesGuiGlobals.TextFG6)
        base.cr.interactionMgr.start()
        self.refreshState()
# okay decompiling DistributedHolidayPig.pyc
