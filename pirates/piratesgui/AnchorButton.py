# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.AnchorButton
from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import BlinkButton, PiratesGuiGlobals


class AnchorButton(BlinkButton.BlinkButton):
    

    def __init__(self, hotkeys=(), hotkeyLabel=None, helpText=PLocalizer.AnchorButtonHelp, parent=None, **kw):
        card = loader.loadModel('models/textureCards/icons')
        iconTexture = card.find('**/icon_anchor').copyTo(NodePath())
        card = loader.loadModel('models/textureCards/skillIcons')
        base1 = card.find('**/base')
        base2 = card.find('**/base_over')
        base3 = card.find('**/base_down')
        seq = NodePath(SequenceNode(''))
        base2.copyTo(seq)
        base1.copyTo(seq)
        base1.copyTo(seq)
        base1.copyTo(seq)
        seq.node().setFrameRate(1.5)
        seq.node().loop(True)
        optiondefs = (
         (
          'image', (seq, base3, base2), None), ('image_scale', 0.195, None), ('geom', iconTexture, None), ('geom_scale', 0.15, None), ('sortOrder', 1, None), ('relief', None, None))
        self.defineoptions(kw, optiondefs)
        BlinkButton.BlinkButton.__init__(self, hotkeys=hotkeys, hotkeyLabel=hotkeyLabel, helpText=helpText, helpPos=(0.05, 0, -0.1), parent=parent)
        self.initialiseoptions(AnchorButton)
        self.infoText = DirectFrame(parent=self, relief=None, text=PLocalizer.AnchorButtonInfo, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), textMayChange=1, pos=(0,
                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                  0.105))
        return
# okay decompiling .\pirates\piratesgui\AnchorButton.pyc
