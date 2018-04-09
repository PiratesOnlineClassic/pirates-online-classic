# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.CannonGUI
import math
import random

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.battle import CannonGlobals, WeaponGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals


class CannonGUI(DirectFrame):
    __module__ = __name__

    def __init__(self, cannon):
        gui = loader.loadModelOnce('models/gui/toplevel_gui')
        DirectFrame.__init__(self, parent=base.a2dBottomCenter, relief=None, image=gui.find('**/topgui_name_text_box'), image_scale=(0.76,
                                                                                                                                     1,
                                                                                                                                     3.2), pos=(0,
                                                                                                                                                0,
                                                                                                                                                0.35), scale=0.6)
        self.initialiseoptions(CannonGUI)
        self.cannon = cannon
        self.reloadIval = None
        self.ammoName = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ARight, text_scale=0.05, pos=(0.25, 0, -0.05), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow)
        self.ammoLeft = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=0.045, pos=(-0.05, 0, 0.09), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow)
        self.volleyLabel = DirectLabel(parent=self, relief=None, text='0', text_align=TextNode.ACenter, text_scale=0.16, pos=(0.2,
                                                                                                                              0,
                                                                                                                              0.02), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow)
        self.reloadBar = DirectWaitBar(parent=self, relief=None, image=gui.find('**/topgui_health_frame'), image_pos=(0.25,
                                                                                                                      0,
                                                                                                                      0.02), image_scale=(0.37,
                                                                                                                                          0.4,
                                                                                                                                          0.4), borderWidth=(0,
                                                                                                                                                             0), range=1, value=1, frameColor=(0.05,
                                                                                                                                                                                               0.35,
                                                                                                                                                                                               0.05,
                                                                                                                                                                                               1), barColor=(0.25,
                                                                                                                                                                                                             1.0,
                                                                                                                                                                                                             0.1,
                                                                                                                                                                                                             1), pos=(-0.25, 0, -0.12), frameSize=(0,
                                                                                                                                                                                                                                                   0.5,
                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                   0.04), text='', text_fg=(0.1,
                                                                                                                                                                                                                                                                            0.1,
                                                                                                                                                                                                                                                                            0.1,
                                                                                                                                                                                                                                                                            1), text_pos=(0.07,
                                                                                                                                                                                                                                                                                          0.01,
                                                                                                                                                                                                                                                                                          0.0), text_scale=0.03)
        self.card = loader.loadModelCopy('models/textureCards/cannonAmmo')
        self.ammoImage = DirectFrame(parent=self, relief=DGG.RIDGE, image_scale=0.18, image_pos=(0.1,
                                                                                                 0,
                                                                                                 0.1), frameColor=PiratesGuiGlobals.FrameColor, borderWidth=PiratesGuiGlobals.BorderWidth, pos=(-0.25, 0, -0.07), frameSize=(0,
                                                                                                                                                                                                                             0.2,
                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                             0.2))
        self.ammoImage.setTransparency(1)
        gui.removeNode()
        return

    def setAmmoId(self, ammoSkillId):
        aname = WeaponGlobals.getSkillName(ammoSkillId)
        self.ammoName['text'] = aname
        asset = CannonGlobals.CANNON_AMMO[ammoSkillId][CannonGlobals.ADEX_ASSET]
        tex = self.card.find('**/%s*' % asset)
        self.ammoImage['image'] = tex
        self.ammoImage['image_scale'] = 0.18
        self.ammoImage['image_pos'] = (0.1, 0, 0.1)

    def setVolley(self, volleyCount):
        self.volleyLabel['text'] = '%d' % (volleyCount,)

    def setAmmoLeft(self, count, maxCount):
        if count < 0:
            self.ammoLeft['text'] = '++'
        else:
            self.ammoLeft['text'] = '%d/%d' % (count, maxCount)

    def resetGui(self):
        pass

    def startReload(self, time, volley, elapsedTime=0, doneCallback=None):
        self.stopReload()
        self.reloadIval = Sequence(LerpFunctionInterval(self.__updateReloadBar, time), Func(self.__reloadDone))
        if doneCallback:
            self.reloadIval.append(Func(doneCallback))
        self.reloadBar['text'] = PLocalizer.Reloading
        if volley:
            self.reloadBar['barColor'] = (0.93, 0.98, 0.35, 1)
        else:
            self.reloadBar['barColor'] = (0.9, 0.0, 0.0, 1)
        self.reloadIval.start(elapsedTime)

    def __updateReloadBar(self, val):
        self.reloadBar['value'] = val

    def __reloadDone(self):
        self.reloadBar['text'] = ''
        self.reloadBar['barColor'] = (0.25, 1.0, 0.1, 1)

    def stopReload(self):
        if self.reloadIval:
            self.reloadIval.pause()
            self.reloadIval = None
        return

    def destroy(self):
        self.stopReload()
        del self.cannon
        self.ammoName.destroy()
        self.volleyLabel.destroy()
        del self.volleyLabel
        self.ammoLeft.destroy()
        del self.ammoLeft
        del self.ammoImage
        self.card.removeNode()
        del self.card
        del self.reloadBar
        DirectFrame.destroy(self)
# okay decompiling .\pirates\battle\CannonGUI.pyc
