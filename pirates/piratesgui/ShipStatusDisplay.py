# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.ShipStatusDisplay
import copy

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.task.Task import Task
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import (AnchorButton, GuiButton, GuiTray,
                                LootPopupPanel, PiratesGuiGlobals,
                                StatusEffectsPanel)
from pirates.piratesgui.BoardingPermissionPanel import BoardingPermissionPanel
from pirates.piratesgui.ShipArmorGui import ShipArmorGui
from pirates.ship import ShipGlobals, ShipMeter
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase


class ShipStatusDisplay(GuiTray.GuiTray):
    

    def __init__(self, parent, shipId, **kw):
        optiondefs = (('relief', None, None), ('pos', (-0.03, 0, -0.55), None), ('shipId', shipId, None), ('shipName', ('', 0), self.applyShipName), ('shipClass', '', self.applyShipClass), ('shipHp', (0, 0), self.applyShipHp), ('shipSp', (0, 0), self.applyShipSp), ('shipCargo', (0, 0), self.applyShipCargo), ('oldCargo', 0, None), ('shipCrew', (0, 0), self.applyShipCrew), ('oldCrew', 0, None), ('ownShip', 0, None))
        self.defineoptions(kw, optiondefs)
        GuiTray.GuiTray.__init__(self, parent, 0.5, 0.5, **kw)
        self.invReq = None
        self.timer = None
        self.anchorButton = None
        self.lootPanel = None
        self.prevChange = 0
        self.statusEffectsPanel = None
        self.skillEffects = {}
        self.durationTask = None
        self.armorGui = None
        self.permissionButton = None
        self.permissionLabel = None
        self.permissionPanel = None
        self.loadGUI()
        self.accept('setName-%s' % self['shipId'], self.setShipName)
        self.accept('setShipClass-%s' % self['shipId'], self.setShipClass)
        self.accept('setShipHp-%s' % self['shipId'], self.setShipHp)
        self.accept('setShipSp-%s' % self['shipId'], self.setShipSp)
        self.accept('setShipCargo-%s' % self['shipId'], self.setShipCargo)
        self.accept('setShipCrew-%s' % self['shipId'], self.setShipCrew)
        self.initialiseoptions(ShipStatusDisplay)
        return

    def destroy(self):
        self.ignoreAll()
        if self.invReq:
            DistributedInventoryBase.cancelGetInventory(self.invReq)
            self.invReq = None
        if self.statusEffectsPanel:
            self.statusEffectsPanel.destroy()
            self.statusEffectsPanel = None
        if self.anchorButton:
            self.anchorButton.destroy()
            self.anchorButton = None
        self.hpMeterDownIval.pause()
        self.hpMeterUpGreenIval.pause()
        self.hpMeterUpRedIval.pause()
        self.hpMeterUpYellowIval.pause()
        del self.hpMeterDownIval
        del self.hpMeterUpGreenIval
        del self.hpMeterUpRedIval
        del self.hpMeterUpYellowIval
        self.timer = None
        self.anchorButton = None
        GuiTray.GuiTray.destroy(self)
        self.destroyBoardingPermissionPanel()
        return

    def loadGUI(self):
        shipcard = loader.loadModel('models/gui/ship_battle')
        self.nameBox = DirectFrame(parent=self, relief=None, pos=(0.27, 0, 0.06), text='Ship Name', text_align=TextNode.ALeft, text_scale=0.045, text_pos=(0, -0.01), text_fg=PiratesGuiGlobals.TextFG1, text_wordwrap=15, text_shadow=(0,
                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                        1), textMayChange=1, text_font=PiratesGlobals.getInterfaceFont())
        tex = shipcard.find('**/ship_battle_speed_bar*')
        self.hpFrame = DirectFrame(parent=self, pos=(0.465, 0, 0.14), relief=None, image=tex, image_scale=(0.3,
                                                                                                           1,
                                                                                                           0.6))
        self.hpMeter = DirectWaitBar(parent=self.hpFrame, relief=DGG.RAISED, borderWidth=(0.004,
                                                                                          0.004), range=100, value=100, frameColor=(0,
                                                                                                                                    0,
                                                                                                                                    0,
                                                                                                                                    0), barColor=(0.1,
                                                                                                                                                  0.7,
                                                                                                                                                  0.1,
                                                                                                                                                  1), frameSize=(-0.27, 0.135, -0.013, 0.013), pos=(0.069,
                                                                                                                                                                                                    0,
                                                                                                                                                                                                    0.0), text=PLocalizer.Hull, text_scale=PiratesGuiGlobals.TextScaleLarge * 0.75, text_align=TextNode.ALeft, text_pos=(0.16, -0.012), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=(0,
                                                                                                                                                                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                                                                                                                                                                        1), text_font=PiratesGlobals.getInterfaceFont())
        self.hpMeterChange = DirectFrame(parent=self.hpFrame, relief=DGG.FLAT, borderWidth=(0.004,
                                                                                            0.004), frameColor=(1.0,
                                                                                                                0.0,
                                                                                                                0.0,
                                                                                                                1.0), sortOrder=0)
        self.hpMeterChange.setBin('gui-fixed', 0)
        self.hpMeterChange.hide()
        self.hpMeterDownIval = Sequence(Func(self.hpMeterChange.show), Wait(0.1), LerpColorInterval(self.hpMeterChange, 0.5, color=VBase4(0.7, 0.1, 0.1, 1.0), blendType='easeOut'), LerpColorInterval(self.hpMeterChange, 0.25, color=VBase4(0.0, 0.0, 0.0, 1.0), blendType='easeOut'), Func(self.hpMeterChange.hide))
        self.hpMeterUpGreenIval = Sequence(Func(self.hpMeterChange.show), Wait(0.1), LerpColorInterval(self.hpMeterChange, 0.75, color=VBase4(0.1, 0.7, 0.1, 1.0)), Func(self.hpMeterChange.hide))
        self.hpMeterUpRedIval = Sequence(Func(self.hpMeterChange.show), Wait(0.1), LerpColorInterval(self.hpMeterChange, 0.75, color=VBase4(1.0, 0.0, 0.0, 1.0)), Func(self.hpMeterChange.hide))
        self.hpMeterUpYellowIval = Sequence(Func(self.hpMeterChange.show), Wait(0.1), LerpColorInterval(self.hpMeterChange, 0.75, color=VBase4(1.0, 1.0, 0.1, 1.0)), Func(self.hpMeterChange.hide))
        self.spFrame = DirectFrame(parent=self, pos=(0.455, 0, 0.115), relief=None, image=tex, image_scale=(0.3,
                                                                                                            1,
                                                                                                            0.52))
        self.speedMeter = DirectWaitBar(parent=self.spFrame, relief=DGG.RAISED, borderWidth=(0.004,
                                                                                             0.004), range=100, value=100, frameColor=(0,
                                                                                                                                       0,
                                                                                                                                       0,
                                                                                                                                       0), barColor=(0.7,
                                                                                                                                                     0.7,
                                                                                                                                                     0.1,
                                                                                                                                                     1), frameSize=(-0.27, 0.135, -0.01, 0.01), pos=(0.069,
                                                                                                                                                                                                     0,
                                                                                                                                                                                                     0.0), text=PLocalizer.Speed, text_scale=PiratesGuiGlobals.TextScaleLarge * 0.75, text_align=TextNode.ALeft, text_pos=(0.16, -0.008), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=(0,
                                                                                                                                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                                                                                                                                          1), text_font=PiratesGlobals.getInterfaceFont())
        circlecard = loader.loadModel('models/textureCards/skillIcons')
        base1 = circlecard.find('**/base')
        base2 = circlecard.find('**/base_over')
        base3 = circlecard.find('**/base_down')
        self.cargoMeter = GuiButton.GuiButton(parent=self, frameSize=(-0.0453125, 0.0453125, -0.0453125, 0.0453125), pos=(0.32,
                                                                                                                          0,
                                                                                                                          0.21), helpText=PLocalizer.CargoIconHelp, helpPos=(0.054, 0, -0.1), command=self.toggleCargo, image=(base1, base3, base2), image_scale=0.1, relief=None)
        icons = loader.loadModel('models/gui/toplevel_gui')
        tex = icons.find('**/topgui_icon_ship_chest01')
        self.cargoLabel = DirectLabel(parent=self.cargoMeter, relief=None, state=DGG.DISABLED, image=tex, image_scale=0.27, image_color=(1,
                                                                                                                                         1,
                                                                                                                                         1,
                                                                                                                                         0.8), text='0/0', text_scale=0.045, text_align=TextNode.ACenter, text_pos=(0.0045, -0.025), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=(0,
                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                     1), text_font=PiratesGlobals.getInterfaceFont())
        self.crewMeter = GuiButton.GuiButton(parent=self, relief=None, state=DGG.DISABLED, frameSize=(-0.0453125, 0.0453125, -0.0453125, 0.0453125), pos=(0.45,
                                                                                                                                                          0,
                                                                                                                                                          0.21), helpText=PLocalizer.CrewIconHelp, helpPos=(-0.05, 0, -0.1), image=base1, image_scale=0.1)
        icons = loader.loadModel('models/textureCards/icons')
        tex = icons.find('**/icon_stickman')
        self.crewLabel = DirectLabel(parent=self.crewMeter, relief=None, state=DGG.DISABLED, image=tex, image_scale=0.08, image_color=(1,
                                                                                                                                       1,
                                                                                                                                       1,
                                                                                                                                       0.8), text='0/0', text_scale=0.045, text_align=TextNode.ACenter, text_pos=(0.0045, -0.025), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=(0,
                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                   1), text_font=PiratesGlobals.getInterfaceFont())
        self.crewLabel.setTransparency(1, 1)
        self.setupPermissionUI()
        self.statusEffectsPanel = StatusEffectsPanel.StatusEffectsPanel(parent=self, pos=(0.3,
                                                                                          0,
                                                                                          0.3))
        self.statusEffectsPanel.iconScale = 0.65
        self.armorGui = ShipArmorGui(self, pos=(0.15, 0.15, 0.15))
        return

    def setupPermissionUI(self):
        if not self.permissionButton:
            if self['ownShip']:
                text = PLocalizer.PermIconHelpOwn
            else:
                text = PLocalizer.PermIconHelp
            circlecard = loader.loadModel('models/textureCards/skillIcons')
            base1 = circlecard.find('**/base')
            base2 = circlecard.find('**/base_over')
            base3 = circlecard.find('**/base_down')
            self.permissionButton = GuiButton.GuiButton(parent=self, relief=None, state=DGG.NORMAL, frameSize=(-0.0453125, 0.0453125, -0.0453125, 0.0453125), pos=(0.58,
                                                                                                                                                                   0,
                                                                                                                                                                   0.21), helpText=text, helpPos=(-0.18, 0, -0.1), image=(base1, base3, base2), image_scale=0.1, command=self.showPermissionPanel)
            tex = loader.loadModel('models/gui/toplevel_gui').find('**/gui_boarding')
            self.permissionLabel = DirectLabel(parent=self.permissionButton, relief=None, state=DGG.DISABLED, image=tex, image_scale=0.15, image_color=(1,
                                                                                                                                                        1,
                                                                                                                                                        1,
                                                                                                                                                        0.8))
            self.permissionLabel.setTransparency(1, 1)
        return

    def showPermissionButton(self):
        if self.permissionButton:
            self.permissionButton.show()

    def hidePermissionButton(self):
        if self.permissionButton:
            self.permissionButton.hide()

    def createBoardingPermissionPanel(self):
        if not self.permissionPanel:
            self.permissionPanel = BoardingPermissionPanel(self, ownShip=self['ownShip'], command=self.hidePermissionPanel)
            self.permissionPanel.hide()

    def destroyBoardingPermissionPanel(self):
        if self.permissionPanel:
            self.permissionPanel.destroy()
            self.permissionPanel = None
        return

    def hidePermissionPanel(self):
        if self.permissionPanel:
            self.permissionPanel.hide()

    def showPermissionPanel(self):
        if not self.permissionPanel:
            self.createBoardingPermissionPanel()
        self.permissionPanel.show()

    def loadLootPanel(self):
        if self.lootPanel:
            return
        self.lootPanel = LootPopupPanel.LootPopupPanel()
        self.lootPanel.reparentTo(self)
        self.lootPanel.setPos(0.05, 0, 0)
        self.lootPanel.hide()

    def applyShipName(self):
        self.setShipName(*self['shipName'])

    def applyShipClass(self):
        self.setShipClass(self['shipClass'])

    def applyShipHp(self):
        self.setShipHp(*self['shipHp'])

    def applyShipSp(self):
        self.setShipSp(*self['shipSp'])

    def applyShipCargo(self):
        self.setShipCargo(*self['shipCargo'])

    def applyShipCrew(self):
        self.setShipCrew(*self['shipCrew'])

    def setShipName(self, name, team):
        if (
         name, team) != self['shipName']:
            self['shipName'] = (
             name, team)
            return
        self.nameBox['text'] = name
        if team == PiratesGlobals.PLAYER_TEAM:
            self.nameBox['text_fg'] = PiratesGlobals.PLAYER_NAMETAG
        else:
            if team == PiratesGlobals.NAVY_TEAM:
                self.nameBox['text_fg'] = PiratesGlobals.NAVY_NAMETAG
            else:
                if team == PiratesGlobals.UNDEAD_TEAM:
                    self.nameBox['text_fg'] = PiratesGlobals.UNDEAD_NAMETAG
                else:
                    if team == PiratesGlobals.FRENCH_UNDEAD_TEAM:
                        self.nameBox['text_fg'] = PiratesGlobals.FRENCH_NAMETAG
                    else:
                        if team == PiratesGlobals.SPANISH_UNDEAD_TEAM:
                            self.nameBox['text_fg'] = PiratesGlobals.SPANISH_NAMETAG

    def setShipClass(self, shipClass):
        if shipClass != self['shipClass']:
            self['shipClass'] = shipClass
            return

    def setShipHp(self, hp, maxHp):
        if (
         hp, maxHp) != self['shipHp']:
            self['shipHp'] = (
             hp, maxHp)
            return
        if hp < 0:
            hp = 0
        else:
            if hp > maxHp:
                hp = maxHp
        if not maxHp:
            return
        hpFraction = float(hp) / float(maxHp)
        if hpFraction >= 0.5:
            barColor = (0.1, 0.7, 0.1, 1)
        else:
            if hpFraction >= 0.25:
                barColor = (1.0, 1.0, 0.1, 1)
            else:
                barColor = (1.0, 0.0, 0.0, 1)
        self.hpMeter['barColor'] = barColor
        prevRange = self.hpMeter['range']
        prevValue = self.hpMeter['value']
        self.hpMeter['range'] = maxHp
        self.hpMeter['value'] = hp
        if self.hpMeterDownIval.isPlaying():
            currentTime = self.hpMeterDownIval.getT()
        else:
            if self.hpMeterUpGreenIval.isPlaying():
                currentTime = self.hpMeterUpGreenIval.getT()
            else:
                if self.hpMeterUpRedIval.isPlaying():
                    currentTime = self.hpMeterUpRedIval.getT()
                else:
                    if self.hpMeterUpYellowIval.isPlaying():
                        currentTime = self.hpMeterUpYellowIval.getT()
                    else:
                        currentTime = None
        if currentTime is not None:
            if currentTime < 0.5:
                prevValue = prevValue + self.prevChange
        if prevValue > hp:
            self.hpMeterChange.setColor(1.0, 0.0, 0.0, 1.0)
            self.prevChange = change = float(prevValue - hp)
            valueScale = float(hp) / float(maxHp)
            changeScale = float(change) / float(maxHp)
            frameRight = float(changeScale * 0.399)
            frameLeft = float(valueScale * 0.399)
            frameX = frameLeft - 0.001
            self.hpMeterChange.setPos(frameX - 0.1995, 0.0, 0.0)
            self.hpMeterChange['frameSize'] = (0.0, frameRight, -0.011, 0.008)
            if currentTime is None:
                self.hpMeterDownIval.start()
                return
            if currentTime >= 0.5:
                self.hpMeterDownIval.start()
            else:
                self.hpMeterDownIval.start(startT=currentTime)
        else:
            if prevValue < hp:
                self.hpMeterChange.setColor(0.0, 0.0, 0.0, 1.0)
                change = float(hp - prevValue)
                valueScale = float(hp) / float(maxHp)
                changeScale = float(change) / float(maxHp)
                frameRight = float(changeScale * 0.399)
                frameLeft = float(valueScale * 0.399)
                if frameLeft < 0.025:
                    return
                frameX = frameLeft - frameRight
                self.hpMeterChange.setPos(frameX - 0.1945, 0.0, 0.0)
                if frameLeft > 0.399:
                    diff = frameLeft - 0.399
                    frameRight = float(frameRight - diff)
                self.hpMeterChange['frameSize'] = (
                 0.0, frameRight, -0.011, 0.008)
                if hpFraction >= 0.5:
                    self.hpMeterUpGreenIval.start()
                elif hpFraction >= 0.25:
                    self.hpMeterUpYellowIval.start()
                else:
                    self.hpMeterUpRedIval.start()
        return

    def setShipSp(self, sp, maxSp):
        if (
         sp, maxSp) != self['shipSp']:
            self['shipSp'] = (
             sp, maxSp)
            return
        self.speedMeter['range'] = maxSp
        self.speedMeter['value'] = sp

    def setShipCargo(self, cargo, maxCargo):
        if (
         cargo, maxCargo) != self['shipCargo']:
            self['shipCargo'] = (
             cargo, maxCargo)
            return
        if self['oldCargo'] != cargo:
            self['oldCargo'] = cargo
            self.cargoLabel['text'] = '%s/%s' % (len(cargo), maxCargo)
            if len(cargo) >= maxCargo:
                self.cargoLabel['text_fg'] = (1, 0, 0, 1)
            else:
                if len(cargo) >= int(maxCargo * 0.75):
                    self.cargoLabel['text_fg'] = (1, 0.8, 0, 1)
                else:
                    self.cargoLabel['text_fg'] = (1, 1, 1, 1)
            scaleAnim = self.cargoMeter.scaleInterval(0.5, Point3(1), startScale=Point3(1.5), blendType='easeIn')
            scaleAnim.start()
            if self.lootPanel and not self.lootPanel.isHidden():
                self.lootPanel.showLoot(cargo)

    def setShipCrew(self, crew, maxCrew):
        if (
         crew, maxCrew) != self['shipCrew']:
            self['shipCrew'] = (
             crew, maxCrew)
            return
        if self['oldCrew'] != crew:
            self['oldCrew'] = crew
            if self['oldCrew'] == 0:
                return
            self.crewLabel['text'] = '%s/%s' % (len(crew), maxCrew)
            if len(crew) >= maxCrew:
                self.crewLabel['text_fg'] = (1, 0, 0, 1)
            else:
                self.crewLabel['text_fg'] = (1, 1, 1, 1)
            scaleAnim = self.crewMeter.scaleInterval(0.5, VBase3(1), startScale=VBase3(1.5), blendType='easeIn')
            scaleAnim.start()

    def toggleCargo(self):
        self.loadLootPanel()
        if self.lootPanel.isHidden():
            self.lootPanel.showLoot(self['oldCargo'])
        else:
            self.lootPanel.hide()

    def updateStatusEffects(self, effects):
        effectIdList = effects.keys()
        for effectKeyId in effectIdList:
            effectId = effects[effectKeyId][0]
            maxDur = effects[effectKeyId][1]
            ts = effects[effectKeyId][2]
            attackerId = effects[effectKeyId][3]
            if effectKeyId not in self.skillEffects.keys():
                self.statusEffectsPanel.addStatusEffect(effectId, maxDur, ts, attackerId)
            else:
                self.statusEffectsPanel.updateStatusEffect(effectId, maxDur, ts, attackerId)

        for effectKeyId in self.skillEffects.keys():
            if effectKeyId not in effectIdList:
                buff = self.skillEffects.get(effectKeyId)
                if buff:
                    effectId = buff[0]
                    attackerId = buff[3]
                    self.statusEffectsPanel.removeStatusEffect(effectId, attackerId)

        self.skillEffects = copy.copy(effects)
        if self.skillEffects:
            self.addDurationTask()
        else:
            self.removeDurationTask()

    def addDurationTask(self):
        if not self.durationTask:
            self.durationTask = taskMgr.add(self.updateDurationTask, self.taskName('updateStatusPanelTask'))

    def removeDurationTask(self):
        if self.durationTask:
            taskMgr.remove(self.taskName('updateStatusPanelTask'))
            self.durationTask = None
        return

    def updateDurationTask(self, task):
        if len(self.skillEffects) > 0:
            if self.statusEffectsPanel:
                self.statusEffectsPanel.updateDurations()
            return Task.cont
        else:
            self.durationTask = None
            return Task.done
        return

    def enableAnchorButton(self):
        if not self.anchorButton:
            self.anchorButton = AnchorButton.AnchorButton(parent=base.a2dBottomCenter, helpText=PLocalizer.AnchorButtonHelp, image_scale=0.18, pos=(0,
                                                                                                                                                    0,
                                                                                                                                                    0.34), scale=1.2, command=self.handleAnchorButton)
        self.anchorButton.show()

    def disableAnchorButton(self):
        if self.anchorButton:
            self.anchorButton.hide()

    def handleAnchorButton(self):
        self.disableAnchorButton()
        base.cr.doId2do[self['shipId']].requestDropAnchor()

    def setArmorStatus(self, location, status):
        self.armorGui.setArmorStatus(location, status)

    def setAllowFriends(self, allow):
        if self.permissionPanel:
            self.permissionPanel.setAllowFriends(allow)

    def setAllowCrew(self, allow):
        if self.permissionPanel:
            self.permissionPanel.setAllowCrew(allow)

    def setAllowGuild(self, allow):
        if self.permissionPanel:
            self.permissionPanel.setAllowGuild(allow)

    def setAllowPublic(self, allow):
        if self.permissionPanel:
            self.permissionPanel.setAllowPublic(allow)
# okay decompiling .\pirates\piratesgui\ShipStatusDisplay.pyc
