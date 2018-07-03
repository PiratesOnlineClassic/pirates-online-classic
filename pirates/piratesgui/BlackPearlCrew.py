# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.BlackPearlCrew
import copy
import datetime
import os
import string
import sys

from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.motiontrail.MotionTrail import MotionTrail
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from panda3d.core import *
from pirates.piratesbase import Freebooter, PiratesGlobals, PLocalizer
from pirates.piratesgui import PDialog, PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui.DialogButton import DialogButton
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui.InventoryItemGui import InventoryItemGui
from pirates.seapatch.Water import Water


class BlackPearlCrew(DirectFrame):
    

    def __init__(self):
        DirectFrame.__init__(self, relief=None)
        self.width = 2.0
        self.height = 1.5
        guiModel = loader.loadModel('models/gui/toplevel_gui')
        self.levelCapScroll = DirectFrame(parent=self, relief=None, image=guiModel.find('**/main_gui_quest_scroll'))
        scroll_x = 0.0
        scroll_y = 0.0
        scroll_z = 0.0
        scale_x = 0.5
        scale_z = 0.5
        self.levelCapScroll.setPos(scroll_x, scroll_y, scroll_z)
        self.levelCapScroll.setScale(scale_x, 1.0, scale_z)
        self.buttonText = PLocalizer.GameOptionsClose
        self.closeButton = DialogButton(self, buttonStyle=DialogButton.YES, command=self.close_button_function)
        self.button_x = 0.39
        self.button_z = -0.25
        self.closeButton.configure(text=self.buttonText, text_fg=(1.0, 1.0, 1.0, 1.0), text_scale=PiratesGuiGlobals.TextScaleLarge, text_wordwrap=0)
        self.closeButton.setPos(self.button_x, 0.0, self.button_z)
        self.closeButton.reparentTo(self)
        self.titleText = DirectLabel(parent=base.a2dTopRight, relief=None, text=PLocalizer.BPCrewTitle, text_font=PiratesGlobals.PirateFont, text_fg=PiratesGuiGlobals.TextFG0, text_scale=PiratesGuiGlobals.TextScaleTitleMed, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=12, pos=(-0.25, 0, 0.21))
        self.titleText.reparentTo(self)
        self.bp_crew = loader.loadModel('models/gui/gui_bpcrew.bam')
        self.tempX = 0.2
        self.tempY = 0.2
        self.tempZ = 0.2
        self.posX = -0.6
        self.posY = 1.0
        self.posZ = -0.33
        self.hendry = self.bp_crew.find('**/crew_3_HendryCutts')
        self.hendry.setScale(self.tempX, self.tempY, self.tempZ)
        self.hendry.setColor(0.0, 0.0, 0.0, 1.0)
        self.hendryJoinedText = DirectLabel(parent=base.a2dTopRight, relief=None, text=PLocalizer.HendryAcquired, text_font=PiratesGlobals.PirateFont, text_fg=PiratesGuiGlobals.TextFG8, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=12, pos=(-0.45, 0, -0.4))
        self.hendryJoinedText.reparentTo(self)
        self.hendryJoinedText.hide()
        self.hendryButton = GuiButton(parent=self, pos=(self.posX, self.posY, self.posZ), state=DGG.DISABLED, image=self.hendry, geom_pos=(self.posX, self.posY, self.posZ), helpText=PLocalizer.HendryName, helpDelay=PiratesGuiGlobals.HelpPopupTime, helpPos=(0.1,
                                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                                 0.65))
        self.hendryButton.helpWatcher['frameSize'] = Vec4(0.25, 0.37, 0.35, 0.58)
        self.carver = self.bp_crew.find('**/crew_1_CarverPidgeley')
        self.carver.setScale(self.tempX, self.tempY, self.tempZ)
        self.carver.setColor(0.0, 0.0, 0.0, 1.0)
        self.carverJoinedText = DirectLabel(parent=base.a2dTopRight, relief=None, text=PLocalizer.CarverAcquired, text_font=PiratesGlobals.PirateFont, text_fg=PiratesGuiGlobals.TextFG8, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=20, pos=(-0.45, 0, -0.4))
        self.carverJoinedText.reparentTo(self)
        self.carverJoinedText.hide()
        self.carverButton = GuiButton(parent=self, pos=(self.posX, self.posY, self.posZ), state=DGG.DISABLED, image=self.carver, geom_pos=(self.posX, self.posY, self.posZ), helpText=PLocalizer.CarverName, helpDelay=PiratesGuiGlobals.HelpPopupTime, helpPos=(-0.1, 0, 0.2))
        self.carverButton.helpWatcher['frameSize'] = Vec4(0.15, 0.25, 0.15, 0.5)
        self.leCerdo = self.bp_crew.find('**/crew_5_LeCerdo')
        self.leCerdo.setScale(self.tempX, self.tempY, self.tempZ)
        self.leCerdo.setPos(self.posX, self.posY, self.posZ)
        self.leCerdo.setColor(0.0, 0.0, 0.0, 1.0)
        self.leCerdoJoinedText = DirectLabel(parent=base.a2dTopRight, relief=None, text=PLocalizer.LeCerdoAcquired, text_font=PiratesGlobals.PirateFont, text_fg=PiratesGuiGlobals.TextFG8, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=12, pos=(-0.45, 0, -0.4))
        self.leCerdoJoinedText.reparentTo(self)
        self.leCerdoJoinedText.hide()
        self.leCerdoButton = GuiButton(parent=self, pos=(self.posX, self.posY, self.posZ), state=DGG.DISABLED, image=self.leCerdo, geom_pos=(self.posX, self.posY, self.posZ), helpText=PLocalizer.LeCerdoName, helpDelay=PiratesGuiGlobals.HelpPopupTime, helpPos=(0.2,
                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                    0.55))
        self.leCerdoButton.helpWatcher['frameSize'] = Vec4(0.35, 0.45, 0.25, 0.52)
        self.gunner = self.bp_crew.find('**/crew_6_Gunner')
        self.gunner.setScale(self.tempX, self.tempY, self.tempZ)
        self.gunner.setPos(self.posX, self.posY, self.posZ)
        self.gunner.setColor(0.0, 0.0, 0.0, 1.0)
        self.gunnerJoinedText = DirectLabel(parent=base.a2dTopRight, relief=None, text=PLocalizer.GunnerAcquired, text_font=PiratesGlobals.PirateFont, text_fg=PiratesGuiGlobals.TextFG8, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=12, pos=(-0.45, 0, -0.4))
        self.gunnerJoinedText.reparentTo(self)
        self.gunnerJoinedText.hide()
        self.gunnerButton = GuiButton(parent=self, pos=(self.posX, self.posY, self.posZ), state=DGG.DISABLED, image=self.gunner, geom_pos=(self.posX, self.posY, self.posZ), helpText=PLocalizer.GunnerName, helpDelay=PiratesGuiGlobals.HelpPopupTime, helpPos=(0.65,
                                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                                 0.6))
        self.gunnerButton.helpWatcher['frameSize'] = Vec4(0.75, 0.85, 0.25, 0.52)
        self.greer = self.bp_crew.find('**/crew_2_GordenGreer')
        self.greer.setScale(self.tempX, self.tempY, self.tempZ)
        self.greer_x = 1.0
        self.greer_y = 1.0
        self.greer_z = 1.0
        self.greer.setPos(self.posX, self.posY, self.posZ)
        self.greer.setColor(0.0, 0.0, 0.0, 1.0)
        self.gordonJoinedText = DirectLabel(parent=base.a2dTopRight, relief=None, text=PLocalizer.GordonAcquired, text_font=PiratesGlobals.PirateFont, text_fg=PiratesGuiGlobals.TextFG8, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=12, pos=(-0.45, 0, -0.4))
        self.gordonJoinedText.reparentTo(self)
        self.gordonJoinedText.hide()
        self.gordonButton = GuiButton(parent=self, pos=(self.posX, self.posY, self.posZ), state=DGG.DISABLED, image=self.greer, geom_pos=(self.posX, self.posY, self.posZ), helpText=PLocalizer.GordonName, helpDelay=PiratesGuiGlobals.HelpPopupTime, helpPos=(0.95,
                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                0.55))
        self.gordonButton.helpWatcher['frameSize'] = Vec4(0.92, 1.1, 0.35, 0.5)
        self.john = self.bp_crew.find('**/crew_9_JohnSmith')
        self.john.setScale(self.tempX, self.tempY, self.tempZ)
        self.john.setPos(self.posX, self.posY, self.posZ)
        self.john.setColor(0.0, 0.0, 0.0, 1.0)
        self.johnJoinedText = DirectLabel(parent=base.a2dTopRight, relief=None, text=PLocalizer.JohnAcquired, text_font=PiratesGlobals.PirateFont, text_fg=PiratesGuiGlobals.TextFG8, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=12, pos=(-0.45, 0, -0.4))
        self.johnJoinedText.reparentTo(self)
        self.johnJoinedText.hide()
        self.johnButton = GuiButton(parent=self, pos=(self.posX, self.posY, self.posZ), state=DGG.DISABLED, image=self.john, geom_pos=(self.posX, self.posY, self.posZ), helpText=PLocalizer.JohnName, helpDelay=PiratesGuiGlobals.HelpPopupTime, helpPos=(0.45,
                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                           0.6))
        self.johnButton.helpWatcher['frameSize'] = Vec4(0.5, 0.7, 0.35, 0.52)
        self.nill = self.bp_crew.find('**/crew_4_NillOffrill')
        self.nill.setScale(self.tempX, self.tempY, self.tempZ)
        self.nill_x = 1.6
        self.nill_y = 1.0
        self.nill_z = 1.0
        self.nill.setPos(self.posX, self.posY, self.posZ)
        self.nill.setColor(0.0, 0.0, 0.0, 1.0)
        self.nillJoinedText = DirectLabel(parent=base.a2dTopRight, relief=None, text=PLocalizer.NillAcquired, text_font=PiratesGlobals.PirateFont, text_fg=PiratesGuiGlobals.TextFG8, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=12, pos=(-0.45, 0, -0.4))
        self.nillJoinedText.reparentTo(self)
        self.nillJoinedText.hide()
        self.nillButton = GuiButton(parent=self, pos=(self.posX, self.posY, self.posZ), state=DGG.DISABLED, image=self.nill, geom_pos=(self.posX, self.posY, self.posZ), helpText=PLocalizer.NillName, helpDelay=PiratesGuiGlobals.HelpPopupTime, helpPos=(0.85,
                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                           0.2))
        self.nillButton.helpWatcher['frameSize'] = Vec4(0.85, 0.92, 0.15, 0.5)
        self.scaryMary = self.bp_crew.find('**/crew_7_ScaryMary')
        self.scaryMary.setScale(self.tempX, self.tempY, self.tempZ)
        self.scaryMary.setPos(self.posX, self.posY, self.posZ)
        self.scaryMary.setColor(0.0, 0.0, 0.0, 1.0)
        self.scaryMaryJoinedText = DirectLabel(parent=base.a2dTopRight, relief=None, text=PLocalizer.ScaryMaryAcquired, text_font=PiratesGlobals.PirateFont, text_fg=PiratesGuiGlobals.TextFG8, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=12, pos=(-0.45, 0, -0.4))
        self.scaryMaryJoinedText.hide()
        self.scaryMaryButton = GuiButton(parent=self, pos=(self.posX, self.posY, self.posZ), state=DGG.DISABLED, image=self.scaryMary, geom_pos=(self.posX, self.posY, self.posZ), helpText=PLocalizer.ScaryMaryName, helpDelay=PiratesGuiGlobals.HelpPopupTime, helpPos=(0.7,
                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                          0.1))
        self.scaryMaryButton.helpWatcher['frameSize'] = Vec4(0.6, 0.75, 0.1, 0.45)
        self.giladoga = self.bp_crew.find('**/crew_8_Giladoga')
        self.giladoga.setScale(self.tempX, self.tempY, self.tempZ)
        self.giladoga.setPos(self.posX, self.posY, self.posZ)
        self.giladoga.setColor(0.0, 0.0, 0.0, 1.0)
        self.giladogaJoinedText = DirectLabel(parent=base.a2dTopRight, relief=None, text=PLocalizer.GiladogaAcquired, text_font=PiratesGlobals.PirateFont, text_fg=PiratesGuiGlobals.TextFG8, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=12, pos=(-0.45, 0, -0.4))
        self.giladogaJoinedText.reparentTo(self)
        self.giladogaJoinedText.hide()
        self.giladogaButton = GuiButton(parent=self, pos=(self.posX, self.posY, self.posZ), state=DGG.DISABLED, image=self.giladoga, geom_pos=(self.posX, self.posY, self.posZ), helpText=PLocalizer.GiladogaName, helpDelay=PiratesGuiGlobals.HelpPopupTime, helpPos=(0.15,
                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                       0.1))
        self.giladogaButton.helpWatcher['frameSize'] = Vec4(0.4, 0.53, 0.07, 0.42)
        self.hide()
        self.carverAquired = False
        self.gordonAquired = False
        self.hendryAquired = False
        self.nillAquired = False
        self.docAquired = False
        self.gunnerAquired = False
        self.scaryMaryAquired = False
        self.giladogaAquired = False
        self.johnAquired = False
        return

    def destroy(self):
        DirectFrame.destroy(self)

    def close_button_function(self):
        self.hide()

    def fade_function(self, crewMember):
        startColor = Vec4(0.0, 0.0, 0.0, 1.0)
        endColor = Vec4(1.0, 1.0, 1.0, 1.0)
        duration = 2.5
        fade = LerpColorScaleInterval(crewMember, duration, endColor, startColorScale=startColor)
        fade.start()

    def showCrewStatus(self):
        currQuestList = localAvatar.getInventory().getQuestList()
        for item in currQuestList:
            print item.getQuestId(), len(item.getQuestId())
            if item.getQuestId()[0] == 'c' and item.getQuestId()[1] == '3':
                currQuest = item.getQuestId()

        if currQuest[0] != 'c' or currQuest[1] != '3':
            self.resetCrewAquired()
            self.drawCrew()
            return
        self.resetCrewAquired()
        if currQuest[1].isdigit():
            chapterInt = int(currQuest[1])
        if currQuest[3].isdigit():
            sectionInt = int(currQuest[3])
        else:
            sectionInt = -1
        if currQuest[5].isdigit():
            partInt = partInt = int(currQuest[5])
        else:
            partInt = -1
        eventInt = self.getEventInt(currQuest)
        if chapterInt < 3:
            print 'Draw Silouettes'
        if chapterInt == 3:
            print 'During Chapter 3'
            if sectionInt < 2:
                print 'Draw Silouettes'
            if sectionInt == 2:
                print 'During Section 2'
                if partInt == 1 and eventInt >= 15 or partInt > 1:
                    self.carverAquired = True
                if partInt == 2 and eventInt >= 11 or partInt > 2:
                    self.gordonAquired = True
                if partInt == 3 and eventInt >= 14 or partInt > 3:
                    self.hendryAquired = True
                if partInt == 4 and eventInt >= 12 or partInt > 4:
                    self.nillAquired = True
                if partInt == 5 and eventInt >= 11 or partInt > 5:
                    self.docAquired = True
            if sectionInt == 3:
                self.carverAquired = True
                self.gordonAquired = True
                self.hendryAquired = True
                self.nillAquired = True
                self.docAquired = True
                print 'During Section 3'
                if partInt == 1 and eventInt >= 53 or partInt > 1:
                    self.gunnerAquired = True
                if partInt == 2 and eventInt >= 21 or partInt > 2:
                    self.scaryMaryAquired = True
                if partInt == 3 and eventInt >= 14 or partInt > 3:
                    self.giladogaAquired = True
                if partInt == 4 and eventInt >= 13 or partInt > 4:
                    self.johnAquired = True
            if sectionInt > 3:
                self.carverAquired = True
                self.gordonAquired = True
                self.hendryAquired = True
                self.nillAquired = True
                self.docAquired = True
                self.gunnerAquired = True
                self.scaryMaryAquired = True
                self.giladogaAquired = True
                self.johnAquired = True
        if chapterInt > 3:
            print 'Draw everybody'
            self.carverAquired = True
            self.gordonAquired = True
            self.hendryAquired = True
            self.nillAquired = True
            self.docAquired = True
            self.gunnerAquired = True
            self.scaryMaryAquired = True
            self.giladogaAquired = True
            self.johnAquired = True
        self.drawCrew()

    def getEventInt(self, currQuest):
        tempString = ''
        if currQuest and currQuest[7].isdigit():
            tempString = localAvatar.activeQuestId[7]
            if currQuest and currQuest[8].isdigit():
                tempString = tempString + localAvatar.activeQuestId[8]
        if tempString != '':
            return int(tempString)
        else:
            return -1

    def resetCrewAquired(self):
        self.carverAquired = False
        self.gordonAquired = False
        self.hendryAquired = False
        self.nillAquired = False
        self.docAquired = False
        self.gunnerAquired = False
        self.scaryMaryAquired = False
        self.giladogaAquired = False
        self.johnAquired = False

    def drawCrew(self):
        if self.carverAquired:
            self.carver.setColor(1.0, 1.0, 1.0, 1.0)
            self.carverButton['image'] = self.carver
        else:
            self.carver.setColor(0.0, 0.0, 0.0, 1.0)
            self.carverButton['image'] = self.carver
        if self.gordonAquired:
            self.greer.setColor(1.0, 1.0, 1.0, 1.0)
            self.gordonButton['image'] = self.greer
        else:
            self.greer.setColor(0.0, 0.0, 0.0, 1.0)
            self.gordonButton['image'] = self.greer
        if self.hendryAquired:
            self.hendry.setColor(1.0, 1.0, 1.0, 1.0)
            self.hendryButton['image'] = self.hendry
        else:
            self.hendry.setColor(0.0, 0.0, 0.0, 1.0)
            self.hendryButton['image'] = self.hendry
        if self.nillAquired:
            self.nill.setColor(1.0, 1.0, 1.0, 1.0)
            self.nillButton['image'] = self.nill
        else:
            self.nill.setColor(0.0, 0.0, 0.0, 1.0)
            self.nillButton['image'] = self.nill
        if self.docAquired:
            self.leCerdo.setColor(1.0, 1.0, 1.0, 1.0)
            self.leCerdoButton['image'] = self.leCerdo
        else:
            self.leCerdo.setColor(0.0, 0.0, 0.0, 1.0)
            self.leCerdoButton['image'] = self.leCerdo
        if self.gunnerAquired:
            self.gunner.setColor(1.0, 1.0, 1.0, 1.0)
            self.gunnerButton['image'] = self.gunner
        else:
            self.gunner.setColor(0.0, 0.0, 0.0, 1.0)
            self.gunnerButton['image'] = self.gunner
        if self.scaryMaryAquired:
            self.scaryMary.setColor(1.0, 1.0, 1.0, 1.0)
            self.scaryMaryButton['image'] = self.scaryMary
        else:
            self.scaryMary.setColor(0.0, 0.0, 0.0, 1.0)
            self.scaryMaryButton['image'] = self.scaryMary
        if self.giladogaAquired:
            self.giladoga.setColor(1.0, 1.0, 1.0, 1.0)
            self.giladogaButton['image'] = self.giladoga
        else:
            self.giladoga.setColor(0.0, 0.0, 0.0, 1.0)
            self.giladogaButton['image'] = self.giladoga
        if self.johnAquired:
            self.john.setColor(1.0, 1.0, 1.0, 1.0)
            self.johnButton['image'] = self.john
        else:
            self.john.setColor(0.0, 0.0, 0.0, 1.0)
            self.johnButton['image'] = self.john

    def showCarver(self):
        self.fade_function(self.carverButton)
        self.carver.setColor(1.0, 1.0, 1.0, 1.0)
        self.carverButton['image'] = self.carver
        self.carverJoinedText.show()

    def showGordon(self):
        self.resetCrewAquired()
        self.carverAquired = True
        self.drawCrew()
        self.fade_function(self.gordonButton)
        self.greer.setColor(1.0, 1.0, 1.0, 1.0)
        self.gordonButton['image'] = self.gordon
        self.gordonJoinedText.show()

    def showHendry(self):
        self.resetCrewAquired()
        self.carverAquired = True
        self.gordonAquired = True
        self.drawCrew()
        self.fade_function(self.hendryButton)
        self.hendry.setColor(1.0, 1.0, 1.0, 1.0)
        self.hendryButton['image'] = self.hendry
        self.hendryJoinedText.show()

    def showNill(self):
        self.resetCrewAquired()
        self.carverAquired = True
        self.gordonAquired = True
        self.hendryAquired = True
        self.drawCrew()
        self.fade_function(self.nillButton)
        self.nill.setColor(1.0, 1.0, 1.0, 1.0)
        self.nillButton['image'] = self.nill
        self.nillJoinedText.show()

    def showLeCerdo(self):
        self.resetCrewAquired()
        self.carverAquired = True
        self.gordonAquired = True
        self.hendryAquired = True
        self.nillAquired = True
        self.drawCrew()
        self.fade_function(self.leCerdoButton)
        self.leCerdo.setColor(1.0, 1.0, 1.0, 1.0)
        self.leCerdoButton['image'] = self.leCerdo
        self.leCerdoJoinedText.show()

    def showGunner(self):
        self.resetCrewAquired()
        self.carverAquired = True
        self.gordonAquired = True
        self.hendryAquired = True
        self.nillAquired = True
        self.docAquired = True
        self.drawCrew()
        self.fade_function(self.gunnerButton)
        self.gunner.setColor(1.0, 1.0, 1.0, 1.0)
        self.gunnerButton['image'] = self.gunner
        self.gunnerJoinedText.show()

    def showScaryMary(self):
        self.resetCrewAquired()
        self.carverAquired = True
        self.gordonAquired = True
        self.hendryAquired = True
        self.nillAquired = True
        self.docAquired = True
        self.gunnerAquired = True
        self.drawCrew()
        self.fade_function(self.scaryMaryButton)
        self.scaryMary.setColor(1.0, 1.0, 1.0, 1.0)
        self.scaryMaryButton['image'] = self.scaryMary
        self.scaryMaryJoinedText.show()

    def showGiladoga(self):
        self.resetCrewAquired()
        self.carverAquired = True
        self.gordonAquired = True
        self.hendryAquired = True
        self.nillAquired = True
        self.docAquired = True
        self.gunnerAquired = True
        self.scaryMaryAquired = True
        self.drawCrew()
        self.fade_function(self.giladogaButton)
        self.giladoga.setColor(1.0, 1.0, 1.0, 1.0)
        self.giladogaButton['image'] = self.giladoga
        self.giladogaJoinedText.show()

    def showJohn(self):
        self.resetCrewAquired()
        self.carverAquired = True
        self.gordonAquired = True
        self.hendryAquired = True
        self.nillAquired = True
        self.docAquired = True
        self.gunnerAquired = True
        self.scaryMaryAquired = True
        self.giladogaAquired = True
        self.drawCrew()
        self.fade_function(self.johnButton)
        self.john.setColor(1.0, 1.0, 1.0, 1.0)
        self.johnButton['image'] = self.john
        self.johnJoinedText.show()
# okay decompiling .\pirates\piratesgui\BlackPearlCrew.pyc
