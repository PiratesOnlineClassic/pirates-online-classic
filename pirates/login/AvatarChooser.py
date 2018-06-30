import math
import os
import time

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.fsm.ClassicFSM import ClassicFSM
from direct.fsm.State import State
from direct.fsm.StateData import StateData
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.PythonUtil import quickProfile
from direct.task.Task import Task
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from panda3d.core import *
from pirates.makeapirate import NameGUI
from pirates.pirate import Human, HumanDNA, Pirate
from pirates.piratesbase import (PiratesGlobals, PLocalizer, TimeOfDayManager,
                                 TODGlobals, UserFunnel)
from pirates.piratesgui import (NonPayerPanel, PDialog, PiratesGuiGlobals,
                                TrialNonPayerPanel)
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui.GameOptions import GameOptions
from pirates.piratesgui.ShardPanel import ShardPanel
from pirates.seapatch.Reflection import Reflection
from pirates.seapatch.SeaPatch import SeaPatch

APPROVED = 1
DENIED = 2


class AvatarChooser(DirectObject, StateData):
    notify = directNotify.newCategory('AvatarChooser')

    def __init__(self, parentFSM, doneEvent):
        StateData.__init__(self, doneEvent)
        self.choice = (0, 0)
        self.gameOptions = None
        self.av = None
        self.deleteConfirmDialog = None
        self.shareConfirmDialog = None
        self.firstAddDialog = None
        self.notDownloadDialog = None
        self.notifications = {}
        self.subFrames = {}
        self.subAvButtons = {}
        self.handleDialogOnScreen = 0
        self.subIds = base.cr.avList.keys()
        if base.cr.isPaid() == 1:
            for subId in base.cr.avList:
                avSet = base.cr.avList[subId]
                for avatar in avSet:
                    if type(avatar) != int:
                        avatar.dna.setTattooChest(0, 0, 0, 0, 0, 0)
                        avatar.dna.setTattooZone2(0, 0, 0, 0, 0, 0)
                        avatar.dna.setTattooZone3(0, 0, 0, 0, 0, 0)
                        avatar.dna.setTattooZone4(0, 0, 0, 0, 0, 0)
                        avatar.dna.setTattooZone5(0, 0, 0, 0, 0, 0)
                        avatar.dna.setTattooZone6(0, 0, 0, 0, 0, 0)
                        avatar.dna.setTattooZone7(0, 0, 0, 0, 0, 0)
                        avatar.dna.setJewelryZone1(0, 0, 0)
                        avatar.dna.setJewelryZone2(0, 0, 0)
                        avatar.dna.setJewelryZone3(0, 0, 0)
                        avatar.dna.setJewelryZone4(0, 0, 0)
                        avatar.dna.setJewelryZone5(0, 0, 0)
                        avatar.dna.setJewelryZone6(0, 0, 0)
                        avatar.dna.setJewelryZone7(0, 0, 0)
                        avatar.dna.setJewelryZone8(0, 0, 0)

        self.subIds.sort()
        self.currentSubIndex = 0
        self.currentSubId = 0
        self.nonPayerPanel = None
        self.trialNonPayerPanel = None
        self.lastMousePos = (0, 0)
        base.avc = self
        return

    def enter(self):
        if self.isLoaded == 0:
            self.load()
        base.disableMouse()
        self.quitButton.show()
        if base.cr.loginInterface.supportsRelogin() and base.config.GetBool(
                'want-logout', False):
            self.logoutButton.show()
        self.scene.reparentTo(render)
        camera.reparentTo(render)
        camera.setPosHpr(-29.0187, 37.0125, 24.75, 4.09, 1.0, 0.0)
        loggedInSubId = base.cr.accountDetailRecord.playerAccountId
        if loggedInSubId in self.subIds:
            index = self.subIds.index(loggedInSubId)
        else:
            index = 0
        self.showSub(index)
        if self.ship:
            taskMgr.add(self.__shipRockTask, 'avatarChooserShipRockTask')
        base.transitions.fadeScreen(1)
        globalClock.tick()
        base.graphicsEngine.renderFrame()
        base.playSfx(self.oceanSfx, looping=1, volume=0.6)
        base.playSfx(self.woodCreaksSfx, looping=1)
        base.musicMgr.request('avchooser-theme', volume=0.4, priority=-2)
        base.transitions.fadeIn(2)
        self.accept('mouse1', self._startMouseReadTask)
        self.accept('mouse1-up', self._stopMouseReadTask)
        self.accept('mouse3', self._startMouseReadTask)
        self.accept('mouse3-up', self._stopMouseReadTask)
        base.options.savePossibleWorking(base.options)
        if os.getenv('GAME_SHOW_FIRSTADD'):
            self.popupTrialPanel()

    def exit(self):
        if self.isLoaded == 0:
            return
        base.musicMgr.requestFadeOut('avchooser-theme')
        self.oceanSfx.stop()
        self.woodCreaksSfx.stop()
        if self.deleteConfirmDialog:
            self.deleteConfirmDialog.destroy()
            self.deleteConfirmDialog = None
        if self.shareConfirmDialog:
            self.shareConfirmDialog.destroy()
            self.shareConfirmDialog = None
        if self.notDownloadDialog:
            self.notDownloadDialog.destroy()
            self.notDownloadDialog = None
        self.avatarListFrame.hide()
        self.highlightFrame.hide()
        self.quitFrame.hide()
        self.renameButton.hide()
        self.rotateSlider.hide()
        self.avName.hide()
        self.scene.detachNode()
        if self.ship:
            taskMgr.remove('avatarChooserShipRockTask')
        self.ignore('mouse1')
        self.ignore('mouse1-up')
        self.ignore('mouse3')
        self.ignore('mouse3-up')
        self._stopMouseReadTask()
        base.options.saveWorking()
        self.ignoreAll()
        if hasattr(self, 'fadeInterval'):
            self.fadeInterval.pause()
            del self.fadeInterval
        if hasattr(self, 'fadeFrame'):
            self.fadeFrame.destroy()
        return

    def load(self):
        if self.isLoaded == 1:
            return
        base.musicMgr.load('avchooser-theme')
        self.model = loader.loadModel('models/gui/avatar_chooser_rope')
        charGui = loader.loadModel('models/gui/char_gui')
        self.oceanSfx = loader.loadSfx('audio/oceanloop.mp3')
        self.woodCreaksSfx = loader.loadSfx('audio/ship_rigging_std.mp3')
        self.exclam = charGui.find('**/chargui_exclamation_mark')
        self.scene = NodePath('AvatarChooserScene')
        self.todManager = TimeOfDayManager.TimeOfDayManager()
        if base.getHoliday(PiratesGlobals.HALLOWEEN):
            self.todManager.cycleType = TODGlobals.TOD_HALLOWEEN_CYCLE
            self.todManager.request('HalloweenNight')
        else:
            self.todManager.request('Night')
        self.todManager.skyGroup.moonTrack.setHpr(345.826, 15.9454, 0)
        self.todManager.dlight.setHpr(-120, -30, 0)
        pier = loader.loadModel('models/islands/pier_port_royal_2deck')
        pier.setPosHpr(-222.23, 360.08, 15.06, 251.57, 0.0, 0.0)
        pier.flattenStrong()
        pier.reparentTo(self.scene)
        pier2 = loader.loadModel('models/islands/pier_port_royal_1deck')
        pier2.setPosHpr(-35.0, 83.27, 19.26, 274.09, 0.0, 0.0)
        pier2.setScale(0.4, 0.3, 0.4)
        pier2.flattenStrong()
        pier2.reparentTo(self.scene)
        saintPatricksDay = base.saintPatricksDay
        self.water = SeaPatch(
            render,
            Reflection.getGlobalReflection(),
            todMgr=self.todManager,
            saintPatricksDay=saintPatricksDay)
        self.water.loadSeaPatchFile('out.spf')
        self.ship = None
        base.richPresence.update(details='Choosing a Pirate')
        if base.launcher.getPhaseComplete(3):
            if base.config.GetBool('want-ships', 1):
                from pirates.ship import ShipGlobals
                from pirates.ship.ShipModel import ShipModel
                self.ship = ShipModel(None, ShipGlobals.INTERCEPTORL1, 0, 1)
                self.ship.setPosHpr(140.86, 538.97, -3.62, -133.04, 0.0, 0.0)
                self.ship.reparentTo(self.scene)
                for n in self.ship.findAllMatches('**/+LODNode'):
                    n.node().forceSwitch(n.node().getHighestSwitch())

        self.avatarListFrame = DirectFrame(parent=base.a2dTopLeft, relief=None)
        self.ropeFrame = DirectFrame(
            parent=self.avatarListFrame,
            relief=None,
            image=self.model.find('**/avatar_c_A_rope'),
            image_scale=0.36,
            pos=(0, 0, -0.015))
        self.subFrame = BorderFrame(
            parent=self.avatarListFrame,
            frameSize=(-0.25, 0.25, -0.04, 0.05),
            borderScale=0.2,
            pos=(0, 0, -0.16),
            suffix='_f')
        triangleGui = loader.loadModel('models/gui/triangle')
        self.subLabel = DirectLabel(
            parent=self.subFrame,
            relief=None,
            text='',
            text_scale=0.05,
            text_fg=(1, 0.9, 0.7, 0.9),
            text_pos=(-0, -0.01),
            textMayChange=1)
        self.nextSubButton = DirectButton(
            parent=self.subFrame,
            relief=None,
            image=(triangleGui.find('**/triangle'),
                   triangleGui.find('**/triangle_down'),
                   triangleGui.find('**/triangle_over')),
            pos=(0.31, 0, 0.025),
            scale=0.08,
            command=self.changeSub,
            extraArgs=[1])
        self.prevSubButton = DirectButton(
            parent=self.subFrame,
            relief=None,
            image=(triangleGui.find('**/triangle'),
                   triangleGui.find('**/triangle_down'),
                   triangleGui.find('**/triangle_over')),
            hpr=(0, 0, 180),
            pos=(-0.31, 0, 0.025),
            scale=0.08,
            command=self.changeSub,
            extraArgs=[-1])
        self.__createAvatarButtons()
        self.ropeFrame.reparentTo(self.avatarListFrame)
        self.subFrame.reparentTo(self.avatarListFrame)
        self.versionLabel = DirectLabel(
            parent=base.a2dTopRight,
            relief=None,
            text_scale=0.04,
            text_fg=(1, 1, 1, 0.5),
            text=str(base.cr.getServerVersion()),
            text_align=TextNode.ARight,
            pos=(-0.05, 0, -0.05))
        self.highlightFrame = DirectFrame(
            parent=base.a2dBottomCenter,
            relief=None,
            image=self.model.find('**/avatar_c_B_frame'),
            image_scale=0.37,
            pos=(0, 0, 0.25),
            scale=0.9)
        self.highlightFrame.hide()
        self.avName = DirectLabel(
            parent=base.a2dBottomCenter,
            relief=None,
            text='',
            text_scale=0.05,
            text_fg=(1, 0.9, 0.7, 0.9),
            text_shadow=PiratesGuiGlobals.TextShadow,
            text_pos=(0, -0.015),
            pos=(0, 0, 0.225))
        self.avName.hide()
        self.shareButton = DirectButton(
            parent=self.highlightFrame,
            relief=None,
            text_scale=0.045,
            text_fg=(1, 0.9, 0.7, 0.9),
            text_shadow=PiratesGuiGlobals.TextShadow,
            text=('', '', PLocalizer.AvatarChooserShared, ''),
            image=(self.model.find('**/avatar_c_B_unlock'),
                   self.model.find('**/avatar_c_B_unlock'),
                   self.model.find('**/avatar_c_B_unlock_over')),
            image_scale=0.37,
            text_pos=(0, -0.1),
            pos=(-0.51, 0, -0.08),
            scale=1.3,
            command=self.__handleShare)
        self.shareButton.hide()
        self.rotateSlider = DirectSlider(
            parent=base.a2dBottomCenter,
            relief=None,
            frameSize=(-0.6, 0.6, 0.1, -0.1),
            image=charGui.find('**/chargui_slider_small'),
            image_scale=1.33,
            thumb_image=(charGui.find('**/chargui_slider_node'),
                         charGui.find('**/chargui_slider_node_down'),
                         charGui.find('**/chargui_slider_node_over')),
            thumb_image_scale=0.6,
            thumb_relief=None,
            scale=0.45,
            value=0,
            range=(-180, 180),
            pos=(0, 0, 0.15),
            command=self.__rotateHighlightedAvatar)
        self.rotateSlider.hide()
        self.playButton = DirectButton(
            parent=self.highlightFrame,
            relief=None,
            text_scale=0.05,
            text_fg=(1, 0.9, 0.7, 0.9),
            text_shadow=PiratesGuiGlobals.TextShadow,
            text='\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserPlay,
            image=(self.model.find('**/avatar_c_B_bottom'),
                   self.model.find('**/avatar_c_B_bottom'),
                   self.model.find('**/avatar_c_B_bottom_over')),
            image_scale=0.37,
            text_pos=(0, -0.015),
            pos=(0, 0, -0.08),
            scale=1.7,
            command=self.__handlePlay)
        self.accept('enter', self.__handleEnter)
        self.accept('arrow_up', self.__handleArrowUp)
        self.accept('arrow_down', self.__handleArrowDown)
        self.deleteButton = DirectButton(
            parent=self.highlightFrame,
            relief=None,
            text_scale=0.045,
            text_fg=(1, 0.9, 0.7, 0.9),
            text_shadow=PiratesGuiGlobals.TextShadow,
            text=('', '', PLocalizer.AvatarChooserDelete, ''),
            image=(self.model.find('**/avatar_c_B_delete'),
                   self.model.find('**/avatar_c_B_delete'),
                   self.model.find('**/avatar_c_B_delete_over')),
            image_scale=0.37,
            text_pos=(0, -0.1),
            pos=(0.51, 0, -0.08),
            scale=1.3,
            command=self.__handleDelete)
        self.quitFrame = DirectFrame(
            parent=base.a2dBottomRight,
            relief=None,
            image=self.model.find('**/avatar_c_C_back'),
            image_scale=0.37,
            pos=(-0.4, 0, 0.21),
            scale=0.9)
        self.quitFrameForeground = DirectFrame(
            parent=self.quitFrame,
            relief=None,
            image=self.model.find('**/avatar_c_C_frame'),
            image_scale=0.37,
            pos=(0, 0, 0))
        self.logoutButton = DirectButton(
            parent=self.quitFrame,
            relief=None,
            text_scale=0.045,
            text_fg=(1, 0.9, 0.7, 0.9),
            text_shadow=PiratesGuiGlobals.TextShadow,
            text=PLocalizer.OptionsPageLogout,
            image=(self.model.find('**/avatar_c_C_box'),
                   self.model.find('**/avatar_c_C_box'),
                   self.model.find('**/avatar_c_C_box_over')),
            image_scale=0.37,
            text_pos=(0, -0.015),
            pos=(0, 0, 0.2),
            command=self.__handleLogoutWithoutConfirm)
        self.logoutButton.hide()
        self.disableOptions = base.config.GetBool('disable-pirates-options', 0)
        if self.disableOptions:
            optionsState = DGG.DISABLED
        else:
            optionsState = DGG.NORMAL
        self.optionsButton = DirectButton(
            parent=self.quitFrame,
            relief=None,
            text_scale=0.05,
            text_fg=(1, 0.9, 0.7, 0.9),
            text_shadow=PiratesGuiGlobals.TextShadow,
            text='\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserOptions,
            image=(self.model.find('**/avatar_c_C_box'),
                   self.model.find('**/avatar_c_C_box'),
                   self.model.find('**/avatar_c_C_box_over')),
            image_scale=0.37,
            text_pos=(0, -0.015),
            pos=(0, 0, 0.07),
            command=self.__handleOptions,
            state=optionsState)
        if self.disableOptions:
            self.optionsButton.setColorScale(Vec4(0.7, 0.7, 0.7, 0.7))
        self.disableQuit = base.config.GetBool('disable-pirates-quit', 0)
        if self.disableQuit:
            quitState = DGG.DISABLED
        else:
            quitState = DGG.NORMAL
        self.quitButton = DirectButton(
            parent=self.quitFrame,
            state=quitState,
            relief=None,
            text_scale=0.05,
            text_fg=(1, 0.9, 0.7, 0.9),
            text_shadow=PiratesGuiGlobals.TextShadow,
            text='\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserQuit,
            image=(self.model.find('**/avatar_c_C_box'),
                   self.model.find('**/avatar_c_C_box'),
                   self.model.find('**/avatar_c_C_box_over')),
            image_scale=0.37,
            text_pos=(0, -0.015),
            pos=(0, 0, -0.07),
            command=self.__handleQuit)
        if self.disableQuit:
            self.quitButton.setColorScale(Vec4(0.7, 0.7, 0.7, 0.7))
        self.renameButton = DirectButton(
            parent=base.a2dTopRight,
            relief=None,
            text_scale=0.05,
            text_fg=(1, 0.9, 0.7, 0.9),
            text_shadow=PiratesGuiGlobals.TextShadow,
            text='\x01smallCaps\x01%s\x02' % 'rename',
            image=(self.model.find('**/avatar_c_C_box'),
                   self.model.find('**/avatar_c_C_box'),
                   self.model.find('**/avatar_c_C_box_over')),
            image_scale=0.37,
            text_pos=(0, -0.015),
            pos=(-0.3, 0, -0.2),
            command=self.__handleRename)

        def shardSelected(shardId):
            self.shardPanel['preferredShard'] = shardId
            base.cr.defaultShard = shardId

        self.shardPanel = ShardPanel(
            base.a2dBottomLeft,
            gear=NodePath('gear'),
            inverted=True,
            relief=None,
            scale=0.85,
            hpr=Vec3(0, 0, 180),
            pos=Vec3(0.415, 0, 0.02),
            uppos=Vec3(0.415, 0, 0.02),
            downpos=Vec3(0.415, 0, 0.6),
            shardSelected=shardSelected,
            buttonFont=PiratesGlobals.getInterfaceFont())
        self.clipPlane = self.highlightFrame.attachNewNode(PlaneNode('clip'))
        self.clipPlane.node().setPlane(Plane(0, 0, 1, 0))
        self.clipPlane.setPos(0, 0, -0.18)
        self.shardPanel.setClipPlane(self.clipPlane)
        self.shardPanelBottom = loader.loadModel(
            'models/gui/general_frame_bottom')
        self.shardPanelBottom.setPos(0.42, 0, 0.095)
        self.shardPanelBottom.setScale(0.273)
        self.shardPanelBottom.reparentTo(base.a2dBottomLeft)
        self.logo = OnscreenImage(
            image='../phase_2/maps/POC_LOGO.png',
            pos=(0, 0, 0.08),
            scale=(0.6, 0.10, 0.40),
            parent=self.avatarListFrame)
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        charGui.removeNode()
        return

    def __createAvatarButtons(self):
        subCard = loader.loadModel('models/gui/toplevel_gui')
        for subFrame in self.subFrames.values():
            subFrame.destroy()

        for buttonList in self.subAvButtons.values():
            for button in buttonList:
                button.destroy()

        self.subFrames = {}
        self.subAvButtons = {}
        i = 0
        for subId, avData in base.cr.avList.items():
            subFrame = DirectFrame(
                parent=self.avatarListFrame, relief=None, pos=(0, 0, -0.3))
            self.subFrames[subId] = subFrame
            avatarButtons = []
            self.subAvButtons[subId] = avatarButtons
            spacing = -0.1
            for av, slot in zip(avData, range(len(avData))):
                x = 0.0
                imageColor = Vec4(1, 1, 1, 1)
                textScale = 0.045
                textFg = (1, 0.9, 0.7, 0.9)
                if slot == 0:
                    z = -0.08
                    textPos = (0, -0.02)
                    image = (self.model.find('**/avatar_c_A_top'),
                             self.model.find('**/avatar_c_A_top'),
                             self.model.find('**/avatar_c_A_top_over'),
                             self.model.find('**/avatar_c_A_top'))
                else:
                    if slot == len(avData) - 1:
                        z = slot * spacing - 0.125
                        textPos = (0, 0.033)
                        image = (self.model.find('**/avatar_c_A_bottom'),
                                 self.model.find('**/avatar_c_A_bottom'),
                                 self.model.find('**/avatar_c_A_bottom_over'),
                                 self.model.find('**/avatar_c_A_bottom'))
                    else:
                        z = slot * spacing - 0.08
                        textPos = (0, -0.015)
                        image = (self.model.find('**/avatar_c_A_middle'),
                                 self.model.find('**/avatar_c_A_middle'),
                                 self.model.find('**/avatar_c_A_middle_over'),
                                 self.model.find('**/avatar_c_A_middle'))
                if av == OTPGlobals.AvatarSlotAvailable:
                    text = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserCreate
                    command = self.__handleCreate
                    state = DGG.NORMAL
                elif av == OTPGlobals.AvatarPendingCreate:
                    text = PLocalizer.AvatarChooserUnderConstruction
                    command = None
                    state = DGG.DISABLED
                    imageColor = Vec4(0.7, 0.7, 0.7, 1)
                elif av == OTPGlobals.AvatarSlotUnavailable:
                    text = PLocalizer.AvatarChooserSlotUnavailable
                    textFg = (0.5, 0.5, 0.5, 1)
                    command = self.popupFeatureBrowser
                    state = DGG.NORMAL
                    imageColor = Vec4(0.7, 0.7, 0.7, 1)
                    textPos = (textPos[0] + 0.034, textPos[1])
                else:
                    avName = av.name
                    text = avName
                    command = self.__handleHighlight
                    state = DGG.NORMAL
                dib = DirectButton(
                    relief=None,
                    parent=subFrame,
                    state=state,
                    text_fg=textFg,
                    text_scale=textScale,
                    text_shadow=PiratesGuiGlobals.TextShadow,
                    text=text,
                    image=image,
                    image_color=imageColor,
                    image_scale=0.37,
                    text_pos=textPos,
                    pos=(x, 0, z),
                    command=command,
                    extraArgs=[subId, slot])
                if text == PLocalizer.AvatarChooserSlotUnavailable:
                    appendMe = DirectFrame(
                        parent=dib,
                        relief=None,
                        pos=(-0.28, 0, textPos[1] - 0.04),
                        state=DGG.DISABLED,
                        geom=subCard.find('**/subscribers_lock'),
                        geom_scale=0.15,
                        geom_pos=(0.06, 0, 0.06))
                avatarButtons.append(dib)

            i += 1

        subCard.removeNode()
        self.isLoaded = 1
        return

    def unload(self):
        if self.isLoaded == 0:
            return

        loader.unloadSfx(self.oceanSfx)
        loader.unloadSfx(self.woodCreaksSfx)
        del self.oceanSfx
        del self.woodCreaksSfx
        loader.unloadModel(self.model)
        self.model.removeNode()
        del self.model
        self.logo.removeNode()
        if self.av:
            self.av.delete()
            del self.av

        if self.ship:
            self.ship.destroy()
            self.ship.removeNode()
            taskMgr.remove('avatarChooserShipRockTask')
            del self.ship

        self.water.delete()
        del self.water
        self.scene.removeNode()
        del self.scene
        self.todManager.disable()
        self.todManager.delete()
        del self.todManager
        cleanupDialog('globalDialog')
        for subFrame in self.subFrames.values():
            subFrame.destroy()

        for buttonList in self.subAvButtons.values():
            for button in buttonList:
                button.destroy()

        del self.subFrames
        del self.subAvButtons
        self.avatarListFrame.destroy()
        self.highlightFrame.destroy()
        self.quitFrame.destroy()
        self.rotateSlider.destroy()
        self.renameButton.destroy()
        self.avName.destroy()
        if self.nonPayerPanel:
            self.nonPayerPanel.destroy()

        del self.nonPayerPanel
        if self.trialNonPayerPanel:
            self.trialNonPayerPanel.destroy()

        del self.trialNonPayerPanel
        if self.gameOptions:
            base.options = self.gameOptions.options
            self.gameOptions.destroy()
            del self.gameOptions

        self.versionLabel.destroy()
        del self.versionLabel
        self.shardPanel.destroy()
        del self.shardPanel
        self.shardPanelBottom.removeNode()
        self.ignoreAll()
        self.isLoaded = 0

    def getChoice(self):
        return self.choice

    def __showHighlightedAvatar(self):
        self.notify.debugCall()
        subId, slot = self.choice
        potAv = base.cr.avList[subId][slot]
        if self.av:
            self.av.cleanupHuman()
            self.av.delete()

        if self.deleteConfirmDialog:
            self.deleteConfirmDialog.destroy()
            self.deleteConfirmDialog = None

        if self.shareConfirmDialog:
            self.shareConfirmDialog.destroy()
            self.shareConfirmDialog = None

        self.av = Pirate.Pirate()
        self.av.setDNAString(potAv.dna)
        self.av.generateHuman(self.av.style.gender, base.cr.human)
        self.av.setPosHpr(-29.69, 46.35, 22.05, 180.0, 0.0, 0.0)
        self.av.reparentTo(self.scene)
        self.av.loop('idle')
        self.av.useLOD(2000)
        self.rotateSlider['value'] = 0
        self.avName['text'] = potAv.dna.getDNAName()
        self.highlightFrame.show()
        if potAv.shared:
            self.shareButton['image'] = (
                self.model.find('**/avatar_c_B_unlock'),
                self.model.find('**/avatar_c_B_unlock'),
                self.model.find('**/avatar_c_B_unlock_over'))

            self.shareButton['text'] = ('', '', PLocalizer.AvatarChooserLocked,
                                        '')
        else:
            self.shareButton['image'] = (
                self.model.find('**/avatar_c_B_lock'),
                self.model.find('**/avatar_c_B_lock'),
                self.model.find('**/avatar_c_B_lock_over'))

            self.shareButton['text'] = ('', '', PLocalizer.AvatarChooserShared,
                                        '')

        if potAv.creator and not potAv.online:
            self.deleteButton['state'] = DGG.NORMAL
            self.shareButton['state'] = DGG.NORMAL
        else:
            self.deleteButton['state'] = DGG.DISABLED
            self.shareButton['state'] = DGG.DISABLED

        if potAv.online:
            self.playButton['text'] = PLocalizer.AvatarChooserAlreadyOnline
            self.playButton['state'] = DGG.DISABLED
        else:
            if not potAv.creator and not potAv.shared:
                self.playButton[
                    'text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserLockedByOwner
                self.playButton['state'] = DGG.DISABLED
            else:
                self.playButton[
                    'text'] = '\x01smallCaps\x01%s\x02' % PLocalizer.AvatarChooserPlay
                self.playButton['state'] = DGG.NORMAL

        self.renameButton.hide()
        if potAv.wishState == 'APPROVED':
            self.blockInput()
            self.finalizeConfirmDialog = PDialog.PDialog(
                text=PLocalizer.AvatarChooserNameAccepted,
                style=OTPDialog.Acknowledge,
                command=self.__handleFinalize)
        else:
            if potAv.wishState == 'DENIED' or potAv.wishState == 'OPEN':
                if self.notifications.get(slot, 0):
                    self.blockInput()
                    if not self.handleDialogOnScreen:
                        self.notify.info('deniedConfirmDialog on screen')
                        self.deniedConfirmDialog = PDialog.PDialog(
                            text=PLocalizer.AvatarChooserPleaseRename,
                            style=OTPDialog.Acknowledge,
                            command=self.__handleDenied)
                    self.handleDialogOnScreen = 1
                self.renameButton.show()

        if not potAv.lastLogout or int(
                time.time() / 60) - potAv.lastLogout > 60:
            potAv.defaultShard = 0

        self.shardPanel['preferredShard'] = potAv.defaultShard
        base.cr.defaultShard = potAv.defaultShard

    def __hideHighlightedAvatar(self):
        if self.av:
            self.av.delete()
            self.av = None

        self.highlightFrame.hide()
        self.rotateSlider.hide()
        self.renameButton.hide()
        self.avName.hide()

    def __handleRename(self):
        self.enterNameMode()

    def __handleHighlight(self, subId, slot):
        self.choice = (subId, slot)
        for button in self.subAvButtons[subId]:
            if button['text'] == PLocalizer.AvatarChooserSlotUnavailable:
                button['text_fg'] = (0.5, 0.5, 0.5, 1)
            else:
                button['text_fg'] = (1, 0.9, 0.7, 0.9)

        self.subAvButtons[subId][slot]['text_fg'] = (1, 1, 1, 1)
        self.__showHighlightedAvatar()

    def __rotateHighlightedAvatar(self):
        if self.av:
            h = self.rotateSlider['value'] + 180
            self.av.setH(h)

    def __handleArrowUp(self):
        if self.gameOptions and not self.gameOptions.isHidden():
            return

        sub = self.choice[0]
        slot = self.choice[1]
        initialSlot = slot
        if not sub:
            return

        numButtons = len(self.subAvButtons[sub])
        av = False
        for index in range(0, numButtons - 1):
            if base.cr.avList.get(sub)[index] not in (
                    OTPGlobals.AvatarSlotUnavailable,
                    OTPGlobals.AvatarSlotAvailable,
                    OTPGlobals.AvatarPendingCreate):
                av = True
                break

        if not av:
            return
        if slot == 0:
            slot = numButtons - 1
        else:
            slot = slot - 1

        while base.cr.avList.get(sub)[slot] in (
                OTPGlobals.AvatarSlotUnavailable,
                OTPGlobals.AvatarSlotAvailable, OTPGlobals.AvatarPendingCreate):
            if slot > 0:
                slot = slot - 1
            else:
                slot = numButtons - 1

        if self.subAvButtons[sub][slot]['state'] == DGG.NORMAL and initialSlot != slot:
            self.__handleHighlight(sub, slot)

    def __handleArrowDown(self):
        if self.gameOptions and not self.gameOptions.isHidden():
            return

        sub = self.choice[0]
        slot = self.choice[1]
        initialSlot = slot
        if not sub:
            return

        numButtons = len(self.subAvButtons[sub])
        av = False
        for index in range(0, numButtons - 1):
            if base.cr.avList.get(sub)[index] not in (
                    OTPGlobals.AvatarSlotUnavailable,
                    OTPGlobals.AvatarSlotAvailable,
                    OTPGlobals.AvatarPendingCreate):
                av = True
                break

        if not av:
            return

        if slot == numButtons - 1:
            slot = 0
        else:
            slot = slot + 1

        while base.cr.avList.get(sub)[slot] in (
                OTPGlobals.AvatarSlotUnavailable,
                OTPGlobals.AvatarSlotAvailable, OTPGlobals.AvatarPendingCreate):
            if slot < numButtons - 1:
                slot = slot + 1
            else:
                slot = 0

        if self.subAvButtons[sub][slot]['state'] == DGG.NORMAL and initialSlot != slot:
            self.__handleHighlight(sub, slot)

    def __handleCreate(self, subId, slot):
        self.choice = (subId, slot)
        base.cr.cleanupWaitingForDatabase()
        base.transitions.fadeOut()
        self.doneStatus = {'mode': 'create'}
        messenger.send(self.doneEvent, [self.doneStatus])

    def __handleShare(self):
        if self.shareConfirmDialog:
            self.shareConfirmDialog.destroy()

        subId, slot = self.choice
        potAv = base.cr.avList[subId][slot]
        name = potAv.dna.getDNAName()
        self.blockInput()
        if potAv.shared:
            self.shareConfirmDialog = PDialog.PDialog(
                text=PLocalizer.AvatarChooserConfirmLock % name,
                style=OTPDialog.TwoChoice,
                command=self.__handleShareConfirmation)
        else:
            self.shareConfirmDialog = PDialog.PDialog(
                text=PLocalizer.AvatarChooserConfirmShare % name,
                style=OTPDialog.TwoChoice,
                command=self.__handleShareConfirmation)

    def __shareAvatarResponse(self, avatarId, subId, shared):
        base.cr.cleanupWaitingForDatabase()
        self.ignore('rejectShareAvatar')
        self.ignore('shareAvatarResponse')
        subId, slot = self.choice
        potAv = base.cr.avList[subId][slot]
        potAv.shared = shared
        if potAv.shared:
            self.shareButton['image'] = (
                self.model.find('**/avatar_c_B_unlock'),
                self.model.find('**/avatar_c_B_unlock'),
                self.model.find('**/avatar_c_B_unlock_over'))

            self.shareButton['text'] = ('', '', PLocalizer.AvatarChooserLocked,
                                        '')
        else:
            self.shareButton['image'] = (
                self.model.find('**/avatar_c_B_lock'),
                self.model.find('**/avatar_c_B_lock'),
                self.model.find('**/avatar_c_B_lock_over'))

            self.shareButton['text'] = ('', '', PLocalizer.AvatarChooserShared,
                                        '')

        self.allowInput()

    def __rejectShareAvatar(self, reasonId):
        self.notify.warning('rejectShareAvatar: %s' % reasonId)
        base.cr.cleanupWaitingForDatabase()
        self.ignore('rejectShareAvatar')
        self.ignore('shareAvatarResponse')
        self.allowInput()

    def __handleEnter(self):
        if self.playButton['state'] == DGG.NORMAL:
            self.__handlePlay()

    def __handlePlay(self):
        if not base.launcher.getPhaseComplete(5):
            if self.notDownloadDialog:
                self.notDownloadDialog.show()
            else:
                self.notDownloadDialog = PDialog.PDialog(
                    text=PLocalizer.AvatarChooserNotDownload,
                    style=OTPDialog.Acknowledge,
                    command=self.__handleNotDownload)

                self.notDownloadDialog.show()

            return

        subId, slot = self.choice
        potAv = base.cr.avList[subId][slot]
        if potAv in (OTPGlobals.AvatarSlotUnavailable,
                     OTPGlobals.AvatarSlotAvailable,
                     OTPGlobals.AvatarPendingCreate):
            return

        self.notify.info(
            'AvatarChooser: wants to play slot: %s avId: %s subId: %s' %
            (slot, potAv.id, subId))
        self.accept('rejectPlayAvatar', self.__rejectPlayAvatar)
        self.accept('playAvatarResponse', self.__playAvatarResponse)
        winInfo = base.win.getProperties()
        x = winInfo.getXSize()
        y = winInfo.getYSize()
        ratio = float(x) / y
        base.emoteGender = base.cr.avList[subId][slot].dna.gender
        base.cr.cleanupWaitingForDatabase()
        self.doneStatus = {'mode': 'chose'}
        messenger.send(self.doneEvent, [self.doneStatus])
        base.transitions.fadeOut()

    def __rejectPlayAvatar(self, reasonId, avatarId):
        self.notify.warning('rejectPlayAvatar: %s' % reasonId)
        self.ignore('rejectPlayAvatar')
        self.ignore('playAvatarResponse')
        base.cr.cleanupWaitingForDatabase()
        self.rejectPlayAvatarDialog = PDialog.PDialog(
            text=PLocalizer.AvatarChooserRejectPlayAvatar,
            style=OTPDialog.Acknowledge,
            command=self.__handleRejectPlayAvatar)

    def __handleRejectPlayAvatar(self, value):
        base.cr.loginFSM.request('shutdown')

    def __playAvatarResponse(self, avatarId, subId, access, founder):
        subId, slot = self.choice
        self.notify.info(
            'AvatarChooser: acquired avatar slot: %s avId: %s subId: %s' %
            (slot, avatarId, subId))
        UserFunnel.loggingAvID('write', avatarId)
        UserFunnel.loggingSubID('write', subId)
        self.ignore('rejectPlayAvatar')
        self.ignore('playAvatarResponse')
        base.cr.cleanupWaitingForDatabase()
        self.doneStatus = {'mode': 'chose'}
        messenger.send(self.doneEvent, [self.doneStatus])
        messenger.send('destroyFeedbackPanel')

    def __handleDelete(self):
        if self.deleteConfirmDialog:
            self.deleteConfirmDialog.destroy()
        subId, slot = self.choice
        potAv = base.cr.avList[subId][slot]
        name = potAv.dna.getDNAName()
        self.blockInput()
        self.deleteConfirmDialog = PDialog.PDialog(
            text=PLocalizer.AvatarChooserConfirmDelete % name,
            style=OTPDialog.YesNo,
            command=self.__handleDeleteConfirmation)

    def __handleDeleteConfirmation(self, value):
        self.deleteConfirmDialog.destroy()
        self.deleteConfirmDialog = None
        if value == DGG.DIALOG_OK:
            subId, slot = self.choice
            potAv = base.cr.avList[subId][slot]
            self.notify.info(
                'AvatarChooser: request delete slot: %s avId: %s subId: %s' %
                (slot, potAv.id, subId))
            self.accept('rejectRemoveAvatar', self.__rejectRemoveAvatar)
            self.accept('removeAvatarResponse', self.__removeAvatarResponse)
            base.cr.csm.sendDeleteAvatar(potAv.id)
            base.cr.waitForDatabaseTimeout(
                requestName='WaitForDeleteAvatarResponse')
            self.blockInput()
        else:
            self.allowInput()

    def __handleShareConfirmation(self, value):
        self.shareConfirmDialog.destroy()
        self.shareConfirmDialog = None
        if value == DGG.DIALOG_OK:
            subId, slot = self.choice
            potAv = base.cr.avList[subId][slot]
            self.notify.info(
                'AvatarChooser: request share slot: %s avId: %s subId: %s' %
                (slot, potAv.id, subId))
            self.accept('rejectShareAvatar', self.__rejectShareAvatar)
            self.accept('shareAvatarResponse', self.__shareAvatarResponse)
            if potAv.shared:
                wantShared = 0
            else:
                wantShared = 1

            base.cr.avatarManager.sendRequestShareAvatar(
                potAv.id, subId, wantShared)
            base.cr.waitForDatabaseTimeout(
                requestName='WaitForShareAvatarResponse')
            self.blockInput()
        else:
            self.allowInput()

    def __removeAvatarResponse(self, avatarId, subId):
        self.ignore('rejectRemoveAvatar')
        self.ignore('removeAvatarResponse')
        base.cr.cleanupWaitingForDatabase()
        base.cr.loginFSM.request('waitForAvatarList')

    def __rejectRemoveAvatar(self, reasonId):
        self.notify.warning('rejectRemoveAvatar: %s' % reasonId)
        self.ignore('rejectRemoveAvatar')
        self.ignore('removeAvatarResponse')
        base.cr.cleanupWaitingForDatabase()
        self.allowInput()

    def updateAvatarList(self):
        self.__hideHighlightedAvatar()
        self.__createAvatarButtons()
        self.subIds = base.cr.avList.keys()
        self.subIds.sort()
        if self.currentSubId not in self.subIds:
            self.notify.warning('subId %s is no longer in family: %s' %
                                (self.currentSubIndex, self.subIds))
            self.currentSubIndex = 0

        self.showSub(self.currentSubIndex)
        subAvs = base.cr.avList[self.currentSubId]
        if len(subAvs) > 0 and subAvs[0] not in (
                OTPGlobals.AvatarSlotUnavailable,
                OTPGlobals.AvatarSlotAvailable, OTPGlobals.AvatarPendingCreate):
            self.__handleHighlight(self.currentSubId, 0)

        if not self.handleDialogOnScreen:
            self.allowInput()

    def __handleOptions(self):
        if self.gameOptions:
            if self.gameOptions.isHidden():
                self.gameOptions.show()
            else:
                self.gameOptions.hide()
        else:
            if base.config.GetBool('want-custom-keys', 0):
                width = 1.8
            else:
                width = 1.6

            height = 1.6
            x = -width / 2
            y = -height / 2
            self.gameOptions = GameOptions(
                'Game Options', x, y, width, height, base.options, chooser=self)
            self.gameOptions.show()

    def __handleQuit(self):
        self.doneStatus = {'mode': 'exit'}
        messenger.send(self.doneEvent, [self.doneStatus])

    def __handleLogoutWithoutConfirm(self):
        base.cr.loginFSM.request('login')

    def __shipRockTask(self, task):
        h = self.ship.getH()
        p = 1.5 * math.sin(task.time * 0.9)
        r = 1.5 * math.cos(task.time * 1.1) + 1.5 * math.cos(task.time * 1.8)
        self.ship.setHpr(h, p, r)
        return Task.cont

    def blockInput(self):
        color = Vec4(0.7, 0.7, 0.7, 0.7)
        for subButtons in self.subAvButtons.values():
            for button in subButtons:
                button['state'] = DGG.DISABLED
                button.setColorScale(color)

        self.renameButton['state'] = DGG.DISABLED
        self.renameButton.setColorScale(color)
        self.quitButton['state'] = DGG.DISABLED
        self.quitButton.setColorScale(color)
        self.logoutButton['state'] = DGG.DISABLED
        self.logoutButton.setColorScale(color)
        self.playButton['state'] = DGG.DISABLED
        self.playButton.setColorScale(color)
        self.shareButton['state'] = DGG.DISABLED
        self.shareButton.setColorScale(color)
        self.deleteButton['state'] = DGG.DISABLED
        self.deleteButton.setColorScale(color)
        self.optionsButton['state'] = DGG.DISABLED
        self.optionsButton.setColorScale(color)
        self.prevSubButton['state'] = DGG.DISABLED
        self.prevSubButton.setColorScale(color)
        self.nextSubButton['state'] = DGG.DISABLED
        self.nextSubButton.setColorScale(color)

    def allowInput(self):
        subId, slot = self.choice
        potAv = base.cr.avList[subId][slot]
        for subButtons in self.subAvButtons.values():
            for button in subButtons:
                if button['text']:
                    button['state'] = DGG.NORMAL
                else:
                    button['state'] = DGG.DISABLED

                button.clearColorScale()

        self.renameButton['state'] = DGG.NORMAL
        self.renameButton.clearColorScale()
        if not self.disableQuit:
            self.quitButton['state'] = DGG.NORMAL
            self.quitButton.clearColorScale()

        self.logoutButton['state'] = DGG.NORMAL
        self.logoutButton.clearColorScale()
        self.playButton['state'] = DGG.NORMAL
        self.playButton.clearColorScale()
        self.shareButton['state'] = DGG.NORMAL
        self.shareButton.clearColorScale()
        self.deleteButton['state'] = DGG.NORMAL
        self.deleteButton.clearColorScale()
        if not self.disableOptions:
            self.optionsButton['state'] = DGG.NORMAL
            self.optionsButton.clearColorScale()

        self.prevSubButton['state'] = DGG.NORMAL
        self.prevSubButton.clearColorScale()
        self.nextSubButton['state'] = DGG.NORMAL
        self.nextSubButton.clearColorScale()
        if potAv not in (OTPGlobals.AvatarSlotUnavailable,
                         OTPGlobals.AvatarSlotAvailable,
                         OTPGlobals.AvatarPendingCreate):
            if potAv.creator and not potAv.online:
                self.deleteButton['state'] = DGG.NORMAL
                self.shareButton['state'] = DGG.NORMAL
            else:
                self.deleteButton['state'] = DGG.DISABLED
                self.shareButton['state'] = DGG.DISABLED
            if potAv.online:
                self.playButton['state'] = DGG.DISABLED
            elif not potAv.creator and not potAv.shared:
                self.playButton['state'] = DGG.DISABLED
            else:
                self.playButton['state'] = DGG.NORMAL

    def __handleFirstAdd(self, value):
        self.firstAddDialog.destroy()
        self.firstAddDialog = None
        self.allowInput()

    def __handleFinalize(self, value):
        subId, slot = self.choice
        self.notifications[slot].removeNode()
        del self.notifications[slot]
        self.finalizeConfirmDialog.destroy()
        potAv = base.cr.avList[subId][slot]
        base.cr.avatarManager.sendRequestFinalize(potAv.id)
        potAv.name = potAv.wishName
        potAv.wishState = 'CLOSED'
        avButton = self.subAvButtons[subId][slot]
        avButton['text'] = potAv.name
        potAv.dna.setName(potAv.wishName)
        avButton.setText()
        self.allowInput()

    def __handleNotDownload(self, value):
        self.notDownloadDialog.destroy()
        self.notDownloadDialog = None
        self.allowInput()

    def __handleDenied(self, value):
        subId, slot = self.choice
        self.notifications[slot].removeNode()
        del self.notifications[slot]
        self.deniedConfirmDialog.destroy()
        self.handleDialogOnScreen = 0
        self.allowInput()

    def enterNameMode(self):
        subId, slot = self.choice
        self.quitFrame.setColorScale(Vec4(1, 1, 1, 0))
        self.highlightFrame.setColorScale(Vec4(1, 1, 1, 0))
        self.avatarListFrame.setColorScale(Vec4(1, 1, 1, 0))
        base.camera.setX(-26)
        self.rotateSlider.setX(-0.7)
        self.avName.show()
        self.avName.setX(-0.68)
        self.rotateSlider.setValue(16)
        self.subFrame.hide()
        av = base.cr.avList[subId][slot]
        base.accept('q', self.exitNameMode)
        base.accept('NameGUIFinished', self.exitNameMode)
        self.renameButton.hide()
        self.nameGui = NameGUI.NameGUI(main=av, independent=True)
        self.nameGui.enter()

    def exitNameMode(self, value):
        subId, slot = self.choice
        if value == 1:
            if self.nameGui.customName:
                base.cr.avList[subId][slot].wishState = 'REQUESTED'
            else:
                potAv = base.cr.avList[subId][slot]
                potAv.name = self.nameGui._getName()
                potAv.wishState = 'CLOSED'
                avButton = self.subAvButtons[subId][slot]
                avButton['text'] = potAv.name
                potAv.dna.setName(potAv.name)
                avButton.setText()

            if self.notifications.get(slot, 0):
                self.notifications[slot].removeNode()
                del self.notifications[slot]
        else:
            self.renameButton.show()

        self.nameGui.unload()
        del self.nameGui
        base.ignore('q')
        base.ignore('NameGUIFinished')
        self.quitFrame.setColorScale(Vec4(1, 1, 1, 1))
        self.highlightFrame.setColorScale(Vec4(1, 1, 1, 1))
        self.avatarListFrame.setColorScale(Vec4(1, 1, 1, 1))
        base.camera.setX(-29)
        self.avName.setX(0)
        self.avName.hide()
        self.subFrame.show()
        self.rotateSlider.setX(0)
        self.rotateSlider.setValue(0)

    def placeNotification(self, slot, pos, style):
        notification = self.exclam.copyTo(self.avatarListFrame)
        self.notifications[slot] = notification
        notification.setPos(pos[0], pos[1], pos[2])
        notification.setScale(0.14)
        notification.setR(25)

    def changeSub(self, delta):
        self.showSub(self.currentSubIndex + delta)

    def showSub(self, index):
        if self.subIds[self.currentSubIndex]:
            numAvs = len(self.subAvButtons[self.subIds[self.currentSubIndex]])
            for slot in range(0, numAvs):
                if self.notifications.get(slot, 0):
                    self.notifications[slot].removeNode()
                    del self.notifications[slot]

        self.currentSubIndex = index
        numSubs = len(self.subIds)
        if self.currentSubIndex <= 0:
            self.currentSubIndex = 0
            self.prevSubButton.hide()
        else:
            self.prevSubButton.show()
        if self.currentSubIndex >= numSubs - 1:
            self.currentSubIndex = numSubs - 1
            self.nextSubButton.hide()
        else:
            self.nextSubButton.show()

        self.currentSubId = self.subIds[self.currentSubIndex]
        subLabelText = '\x01white\x01%s\x02' % base.cr.launcher.getPlayToken()
        self.subLabel['text'] = subLabelText
        for frame in self.subFrames.values():
            frame.hide()

        self.subFrames[self.currentSubId].show()
        anyAvatars = False
        for avList in base.cr.avList.values():
            for av in avList:
                if av not in (OTPGlobals.AvatarSlotUnavailable,
                              OTPGlobals.AvatarSlotAvailable,
                              OTPGlobals.AvatarPendingCreate):
                    anyAvatars = True
                    break

            if anyAvatars:
                break

        avList = base.cr.avList[self.currentSubId]
        for avIdx in range(0, len(avList)):
            if avList[avIdx] not in (OTPGlobals.AvatarSlotUnavailable,
                                     OTPGlobals.AvatarSlotAvailable,
                                     OTPGlobals.AvatarPendingCreate):
                if avList[avIdx].wishState == 'APPROVED':
                    self.placeNotification(
                        avIdx, (0.32, 0, -0.37 - avIdx * 0.095), APPROVED)
                elif avList[avIdx].wishState == 'DENIED' or avList[avIdx].wishState == 'OPEN':
                    self.placeNotification(
                        avIdx, (0.32, 0, -0.37 - avIdx * 0.095), DENIED)

        if anyAvatars:
            self.avatarListFrame.reparentTo(base.a2dTopLeft)
            self.avatarListFrame.setPosHprScale(0.42, 0, -0.3, 0, 0, 0, 1, 1, 1)
        else:
            self.avatarListFrame.reparentTo(base.a2dTopCenter)
            self.avatarListFrame.setPosHprScale(0, 0, -0.3, 0, 0, 0, 1.1, 1.1,
                                                1.1)
            self.rotateSlider.hide()
            self.renameButton.hide()
            self.avName.hide()
            self.shardPanel.hide()
            self.shardPanelBottom.hide()

        subAvs = base.cr.avList[self.currentSubId]
        if len(subAvs) > 0 and subAvs[0] not in (
                OTPGlobals.AvatarSlotUnavailable,
                OTPGlobals.AvatarSlotAvailable, OTPGlobals.AvatarPendingCreate):
            self.__handleHighlight(self.currentSubId, 0)
        else:
            self.__hideHighlightedAvatar()

    def popupTrialPanel(self):
        if not self.trialNonPayerPanel:
            self.trialNonPayerPanel = TrialNonPayerPanel.TrialNonPayerPanel(
                trial=True)
        self.trialNonPayerPanel.show()

    def popupFeatureBrowser(self, subId, slot):
        if not self.nonPayerPanel:
            self.nonPayerPanel = TrialNonPayerPanel.TrialNonPayerPanel(
                trial=False)
        self.nonPayerPanel.show()

    def _stopMouseReadTask(self):
        taskMgr.remove('AvatarChooser-MouseRead')

    def _startMouseReadTask(self):
        self._stopMouseReadTask()
        mouseData = base.win.getPointer(0)
        self.lastMousePos = (mouseData.getX(), mouseData.getY())
        taskMgr.add(self._mouseReadTask, 'AvatarChooser-MouseRead')

    def __rotateHighlightedAvatar(self):
        if self.av:
            h = self.rotateSlider['value'] + 180
            self.av.setH(h)

    def _mouseReadTask(self, task):
        if not base.mouseWatcherNode.hasMouse():
            return

        winSize = (base.win.getXSize(), base.win.getYSize())

        mouseData = base.win.getPointer(0)
        if mouseData.getX() > winSize[0] or mouseData.getY() > winSize[1]:
            return

        dx = mouseData.getX() - self.lastMousePos[0]
        mouseData = base.win.getPointer(0)
        self.lastMousePos = (mouseData.getX(), mouseData.getY())
        if self.av:
            value = self.rotateSlider['value']
            value = max(-180, min(180, value + dx * 0.7))
            self.rotateSlider['value'] = value

        return Task.cont


# okay decompiling .\pirates\login\AvatarChooser.pyc
