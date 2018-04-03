# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.BuffIcon
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from pirates.piratesbase import PiratesGlobals
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.DialMeter import DialMeter
from pirates.piratesgui.BorderFrame import BorderFrame
buffTable = {WeaponGlobals.C_POISON: ('buff_poison', PLocalizer.BuffPoison), WeaponGlobals.C_ACID: ('buff_acid', PLocalizer.BuffAcid), WeaponGlobals.C_HOLD: ('buff_hold', PLocalizer.BuffHold), WeaponGlobals.C_WOUND: ('buff_wound', PLocalizer.BuffWound), WeaponGlobals.C_ON_FIRE: ('buff_burn', PLocalizer.BuffOnFire), WeaponGlobals.C_FLAMING: ('buff_burn', PLocalizer.BuffOnFire), WeaponGlobals.C_STUN: ('buff_stun', PLocalizer.BuffStun), WeaponGlobals.C_UNSTUN: ('buff_stun', PLocalizer.BuffUnstun), WeaponGlobals.C_SLOW: ('buff_stun', PLocalizer.BuffSlow), WeaponGlobals.C_PAIN: ('buff_stun', PLocalizer.BuffSlow), WeaponGlobals.C_DIRT: ('buff_blind', PLocalizer.BuffBlind), WeaponGlobals.C_BLIND: ('buff_blind', PLocalizer.BuffBlind), WeaponGlobals.C_CURSE: ('buff_curse', PLocalizer.BuffCurse), WeaponGlobals.C_HASTEN: ('buff_hasten', PLocalizer.BuffHasten), WeaponGlobals.C_TAUNT: ('buff_taunt', PLocalizer.BuffTaunt), WeaponGlobals.C_WEAKEN: ('buff_weaken', PLocalizer.BuffWeaken), WeaponGlobals.C_REGEN: ('buff_stun', PLocalizer.BuffRegen), WeaponGlobals.C_SPAWN: ('buff_blind', PLocalizer.BuffSpawn), WeaponGlobals.C_VOODOO_STUN_LOCK: ('buff_stun', PLocalizer.BuffVoodooStunLock), WeaponGlobals.C_ATTUNE: ('buff_attune', PLocalizer.BuffAttune), WeaponGlobals.C_FULLSAIL: ('sail_full_sail', PLocalizer.BuffFullSail), WeaponGlobals.C_COMEABOUT: ('sail_come_about', PLocalizer.BuffComeAbout), WeaponGlobals.C_OPENFIRE: ('buff_openfire', PLocalizer.BuffOpenFire), WeaponGlobals.C_RAM: ('sail_ramming_speed', PLocalizer.BuffRam), WeaponGlobals.C_TAKECOVER: ('sail_take_cover', PLocalizer.BuffTakeCover), WeaponGlobals.C_RECHARGE: ('sail_recharge', PLocalizer.BuffPowerRecharge)}

class BuffIcon(DirectFrame):
    __module__ = __name__
    Background = None
    Card = None

    def __init__(self, parent, effectId, duration, attackerId, **kw):
        optiondefs = (('relief', None, None), )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        self.initialiseoptions(BuffIcon)
        if not self.Background:
            self.Background = loader.loadModel('models/gui/lookout_gui').find('**/lookout_submit')
            self.Background.setScale(0.33)
        if not self.Card:
            self.Card = loader.loadModel('models/textureCards/buff_icons')
        self.myIcon = None
        self.detailFrame = None
        self.dial = None
        self.iconScale = 0.07
        self.effectId = effectId
        self.maxDuration = duration
        self.startTimestamp = 0
        self.attackerId = attackerId
        self.setDepthWrite(0)
        self.setFogOff()
        self.setLightOff()
        return

    def makeIcons(self):
        self.Background.copyTo(self)
        self.dial = DialMeter(parent=self, meterColor=Vec4(0.3, 0.0, 0.8, 1), baseColor=Vec4(0, 0, 0, 1), scale=0.17, sortOrder=0)
        info = buffTable.get(self.effectId)
        self.myIcon = DirectButton(parent=self, relief=None, geom=self.Card.find('**/' + info[0]), geom_scale=self.iconScale, sortOrder=1)
        self.myIcon.bind(DGG.ENTER, self.showDetails)
        self.myIcon.bind(DGG.EXIT, self.hideDetails)
        self.updateIconInfo()
        return

    def makeDetails(self):
        if self.detailFrame:
            return
        durationStr = str(int(self.maxDuration))
        text = buffTable[self.effectId][1] + PLocalizer.BuffDuration % durationStr
        self.detailBox = DirectLabel(state=DGG.DISABLED, relief=None, text=text, text_align=TextNode.ALeft, text_scale=0.03, text_fg=(1,
                                                                                                                                      1,
                                                                                                                                      1,
                                                                                                                                      1), text_wordwrap=15, text_shadow=(0,
                                                                                                                                                                         0,
                                                                                                                                                                         0,
                                                                                                                                                                         1), textMayChange=1)
        height = -(self.detailBox.getHeight() + 0.01)
        width = max(0.25, self.detailBox.getWidth() + 0.04)
        self.detailFrame = BorderFrame(parent=self.myIcon, state=DGG.DISABLED, frameSize=(-0.04, width, height, 0.05), pos=(0.05, 0, -0.05))
        self.detailBox.reparentTo(self.detailFrame)
        self.detailFrame.setBin('gui-popup', 0)
        self.detailFrame.hide()
        return

    def showDetails(self, event):
        self.makeDetails()
        self.detailFrame.show()
        self.updateIconInfo()

    def hideDetails(self, event):
        if self.detailFrame:
            self.detailFrame.hide()

    def updateIconInfo(self):
        if self.startTimestamp == None:
            timeOffset = 0.0
        else:
            timeOffset = globalClockDelta.localElapsedTime(self.startTimestamp)
        duration = max(0.0, self.maxDuration - timeOffset)
        self.dial.update(duration, self.maxDuration)
        if self.detailFrame and not self.detailFrame.isHidden():
            durationStr = str(int(duration) + 1)
            text = buffTable[self.effectId][1] + PLocalizer.BuffDuration % durationStr
            self.detailBox['text'] = text
        return

    def destroy(self):
        DirectFrame.destroy(self)
# okay decompiling .\pirates\piratesgui\BuffIcon.pyc
