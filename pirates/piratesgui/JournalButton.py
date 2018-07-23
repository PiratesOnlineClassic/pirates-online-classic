from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import GuiButton, PiratesGuiGlobals


class JournalButton(GuiButton.GuiButton):
    

    def __init__(self, hotkeys=(), hotkeyLabel='J', helpText=None, parent=None, **kw):
        gui = loader.loadModelOnce('models/gui/toplevel_gui')
        iconTexture = gui.find('**/topgui_icon_journal')
        gui.removeNode()
        del gui
        optiondefs = (
         (
          'image', iconTexture, None), ('image_scale', 0.5, None), ('sortOrder', 1, None), ('relief', None, None))
        self.defineoptions(kw, optiondefs)
        GuiButton.GuiButton.__init__(self, hotkeys=hotkeys, hotkeyLabel=hotkeyLabel, helpText=helpText, parent=parent)
        self.initialiseoptions(JournalButton)
        self.questCounter = 0
        self.infoText = DirectFrame(parent=self, relief=None, text=PLocalizer.JournalButtonInfo, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), textMayChange=1, pos=(0,
                                                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                                                   0.1))
        self.numberText = DirectFrame(parent=self, relief=None, text=str(self.questCounter), text_align=TextNode.ACenter, text_scale=0.08, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateOutlineFont(), textMayChange=1, pos=(0, 0, -0.01))
        self.hotkeyLabel = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=hotkeyLabel, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(0.1, -0.04), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0)
        return

    def addNewQuest(self):
        self.questCounter = 1
        if self.questCounter > 1:
            self.numberText['text'] = str(self.questCounter)
        else:
            self.numberText['text'] = ''

    def removeNewQuest(self):
        self.questCounter = max(self.questCounter - 1, 0)
        if self.questCounter > 1:
            self.numberText['text'] = str(self.questCounter)
        else:
            self.numberText['text'] = ''
