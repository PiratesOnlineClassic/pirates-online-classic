# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.CrewIconSelector
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from otp.otpbase import OTPGlobals
from pandac.PandaModules import *
from pirates.band import BandConstance
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import GuiPanel, PDialog, PiratesGuiGlobals
from pirates.piratesgui.RequestButton import RequestButton

CREW_ICON_BAM = 'models/gui/gui_main'
CREW_ICONS = {1: 'crew_member/crew_member', 2: 'crew_member/crew_member'}

class CrewIconSelectorConfirmButton(RequestButton):
    __module__ = __name__

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewIconSelectorConfirmButton)


class CrewIconSelectorCancelButton(RequestButton):
    __module__ = __name__

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewIconSelectorCancelButton)


class CrewIconSelector(GuiPanel.GuiPanel):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('CrewIconSelector')

    def __init__(self, title, selectedIconKey=0):
        GuiPanel.GuiPanel.__init__(self, title, 0.8, 0.77, 0, '', pos=(0.52, 0, -0.82))
        self.initialiseoptions(CrewIconSelector)
        self.setPics = {}
        self.selectedIconKey = selectedIconKey
        self.currentIconKey = base.localAvatar.getCrewIcon()
        self.localHeight = PiratesGuiGlobals.InventoryPanelHeight - 0.2
        gui = loader.loadModel('models/gui/toplevel_gui')
        spotPic = gui.find('**/treasure_w_a_slot')
        self.card = loader.loadModelCopy(CREW_ICON_BAM)
        crewIconParent = NodePath('crewIconParent')
        for colSpot in range(4):
            for rowSpot in range(4):
                if colSpot > 0:
                    blip = spotPic.copyTo(crewIconParent)
                    blip.setScale(0.45)
                    blip.setPos(0.24 + 0.18 * rowSpot, 0, self.localHeight - 0.4 - 0.18 * colSpot)

        crewIconParent.flattenStrong()
        self.iconFrame = DirectFrame(parent=self, relief=None, geom=crewIconParent)
        self.iconFrame.setPos(-0.1, 0, -0.12)
        self.bOk = CrewIconSelectorConfirmButton(text=PLocalizer.GenericConfirmOK, command=self.__handleOK)
        self.bCancel = CrewIconSelectorCancelButton(text=PLocalizer.DialogCancel, command=self.__handleCancel)
        self.bOk.reparentTo(self)
        self.bCancel.reparentTo(self)
        self.bOk.setPos(0.25, 0, 0.05)
        self.bCancel.setPos(0.45, 0, 0.05)
        self.loadIconList()
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('Esc')
        GuiPanel.GuiPanel.destroy(self)

    def __handleOK(self):
        if type(self.selectedIconKey) != int:
            self.selectedIconKey = 0
        base.cr.PirateBandManager.d_requestCrewIconUpdate(self.selectedIconKey)
        base.localAvatar.guiMgr.crewPage.enableClearCrewIconButton(self.selectedIconKey)
        self.destroy()

    def __handleCancel(self):
        base.localAvatar.setCrewIcon(self.currentIconKey)
        self.destroy()

    def loadIconList(self):
        setCount = len(CREW_ICONS)
        rowSpot = 0
        colSpot = 0
        counter = 0
        for loopItr, iconFile in CREW_ICONS.items():
            setKey = loopItr
            pic_name = iconFile
            tex = self.card.find('**/%s' % pic_name)
            self.setPics[setKey] = DirectButton(parent=self.iconFrame, relief=None, image=tex, image_scale=0.34, image2_scale=0.36, image_pos=(0,
                                                                                                                                               0,
                                                                                                                                               0), pos=(0.24 + 0.18 * rowSpot, 0, self.localHeight - 0.4 - 0.18 * colSpot - 0.18), command=self.__setIconKey, extraArgs=[setKey], pressEffect=1)
            self.setPics[setKey].setTransparency(1)
            counter += 1
            rowSpot = counter % 4
            colSpot = counter / 4

        return

    def __setIconKey(self, setValue):
        self.selectedIconKey = setValue
        base.localAvatar.setCrewIcon(setValue)
# okay decompiling .\pirates\piratesgui\CrewIconSelector.pyc
