# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.BlinkButton
from direct.gui.DirectGui import *
from panda3d.core import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import GuiButton, PiratesGuiGlobals


class BlinkButton(GuiButton.GuiButton):

    def __init__(self, parent, **kw):
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
        optiondefs = (('sortOrder', 1, None), ('relief', None, None),
                      ('image', (seq, base3, base2), None))
        self.defineoptions(kw, optiondefs)
        GuiButton.GuiButton.__init__(self, parent=parent, **kw)
        self.initialiseoptions(BlinkButton)
        return


# okay decompiling .\pirates\piratesgui\BlinkButton.pyc
