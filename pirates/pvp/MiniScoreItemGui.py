import random

from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectGui import *
from direct.gui.DirectGuiGlobals import *
from direct.gui.DirectLabel import *
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals

class MiniScoreItemGui(DirectFrame):
    
    Width = PiratesGuiGlobals.PVPPanelWidth - PiratesGuiGlobals.GridSize
    Height = 0.055

    def __init__(self, scoreValue, parent=None, world=None, itemColorScale=None, blink=False, **kw):
        optiondefs = (('state', DGG.NORMAL, None), ('frameColor', (1, 1, 1, 0.05), None), ('borderWidth', PiratesGuiGlobals.BorderWidth, None), ('frameSize', (0.0, MiniScoreItemGui.Width, 0.0, MiniScoreItemGui.Height), None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(MiniScoreItemGui)
        self.scoreValue = scoreValue
        self.world = world
        self.itemColorScale = itemColorScale
        self.blink = blink
        self.scaleSeq = None
        self._createIface()

    def destroy(self):
        self._destroyIface()
        DirectFrame.destroy(self)
        del self.scoreValue
        self.ignoreAll()

    def _createIface(self):
        textFg = PiratesGuiGlobals.TextFG1
        if self.world != None:
            scoreText = self.world.getScoreText(self.scoreValue)
        else:
            scoreText = ''
        self.descText = DirectLabel(parent=self, relief=None, text=scoreText, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, 
                                    text_fg=textFg, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.04, 0, 0.015), text_font=PiratesGlobals.getPirateOutlineFont())
        if self.itemColorScale:
            self.colorLabel(self.itemColorScale)
        if self.blink:
            textPos = self.descText['text_pos']
            textPosX = textPos[0]
            textPosY = textPos[1]
            self.scaleSeq = Parallel(Sequence(LerpFunctionInterval(self.descText.setScale, duration=0.2, toData=1.05, fromData=1.0, blendType='easeInOut'), LerpFunctionInterval(self.descText.setScale, duration=0.7, toData=1.0, fromData=1.05, blendType='easeInOut')), Sequence(Func(self.colorLabel, (1, 1, 1, 1)), 
                                     Func(self.moveLabel, (textPosX, textPosY)), Wait(0.05), Func(self.moveLabel, (textPosX, textPosY)), Wait(0.05), Func(self.colorLabel, (1, 0, 0, 1)), Func(self.moveLabel, (textPosX, textPosY)), Wait(0.05), Func(self.moveLabel, (textPosX, textPosY)), Wait(0.05), 
                                     Func(self.colorLabel, (1, 1, 1, 1)), Func(self.moveLabel, (textPosX, textPosY)), Wait(0.05), Func(self.moveLabel, (textPosX, textPosY)), Wait(0.05), Func(self.colorLabel, (1, 0, 0, 1)), Func(self.moveLabel, (textPosX, textPosY)), Wait(0.05), Func(self.moveLabel, (textPosX, textPosY)), 
                                     Wait(0.05), Func(self.colorLabel, (1, 1, 1, 1)), Func(self.moveLabel, (textPosX, textPosY)), Wait(0.05), Func(self.moveLabel, (textPosX, textPosY)), Wait(0.05), Func(self.colorLabel, (1, 0, 0, 1)), Func(self.moveLabel, (textPosX, textPosY)), Wait(0.05), Func(self.moveLabel, (textPosX, textPosY)), Wait(0.05), Func(self.colorLabel, (1, 1, 1, 1)), 
                                     Func(self.moveLabel, (textPosX, textPosY)), Wait(0.05), Func(self.moveLabel, (textPosX, textPosY)), Wait(0.05), Func(self.colorLabel, PiratesGuiGlobals.TextFG1), Func(self.moveLabel, (textPosX, textPosY))))
            self.scaleSeq.start()

    def moveLabel(self, xy):
        randX = random.random() * 0.005 + 0.005
        randY = random.random() * 0.005 + 0.005
        self.descText['text_pos'] = (xy[0] + randX, xy[1] + randY)

    def colorLabel(self, color):
        self.descText['text_fg'] = color

    def shakeItUp(self, (x, y, r, g, b, a)):
        self.colorLabel((r, g, b, a))
        randX = random.random() * 0.005 + 0.005
        randY = random.random() * 0.005 + 0.005
        self.moveLabel((x + randX, y + randY))
        Wait(0.05)
        randX = random.random() * 0.005 + 0.005
        randY = random.random() * 0.005 + 0.005
        self.moveLabel((x + randX, y + randY))
        Wait(0.05)

    def _destroyIface(self):
        if self.scaleSeq:
            self.scaleSeq.finish()
            self.scaleSeq = None
        self.descText.destroy()
        del self.descText