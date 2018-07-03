# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.ChestTray
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import GuiTray, PiratesGuiGlobals, QuestPage
from pirates.piratesgui.GuiButton import GuiButton
from pirates.reputation import ReputationGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


class ChestTray(GuiTray.GuiTray):
    
    WantClothingPage = base.config.GetBool('want-clothing-page', 0)
    WantTitlesPage = base.config.GetBool('want-titles-page', 0)

    def __init__(self, parent, parentMgr, **kw):
        GuiTray.GuiTray.__init__(self, parent, 0.6, 0.12, **kw)
        self.initialiseoptions(ChestTray)
        self.state = 0
        self.buttonsParent = self.attachNewNode(ModelNode('ChestTray.buttonsParent'), sort=1)
        self.stickyButtonsParent = self.attachNewNode(ModelNode('ChestTray.stickyButtonsParent'), sort=1)
        self.stickyButtonsParent.setPos(0, 0, 0.02)
        self.buttons = []
        self.guiMgr = parentMgr
        self.buildShowHideButtonsIvals()
        self.openSfx = loader.loadSfx('audio/sfx_gui_seachest-open.mp3')
        self.openSfx.setVolume(0.4)
        self.closeSfx = loader.loadSfx('audio/sfx_gui_seachest-close.mp3')
        self.closeSfx.setVolume(0.4)
        gui = loader.loadModel('models/gui/toplevel_gui')
        gui_main = loader.loadModel('models/gui/gui_main')
        helpPos = (
         -0.26, 0, 0.06)
        helpDelay = 0
        buttonImages = gui.find('**/topgui_icon_box')
        buttonColors = (
         VBase4(0.7, 0.7, 0.7, 1), VBase4(0.8, 0.8, 0.8, 1), VBase4(1.0, 1.0, 1.0, 1), VBase4(0.6, 0.6, 0.6, 1))
        buttonOptions = {'image': buttonImages, 'geom': None, 'relief': None, 'frameSize': (0, 0.12, 0, 0.12), 'image_scale': 0.315, 'image_pos': (0.06, 0, 0.06), 'image0_color': buttonColors[0], 'image1_color': buttonColors[1], 'image2_color': buttonColors[2], 'image3_color': buttonColors[3], 'geom_scale': 0.12, 'geom_pos': (0.06, 0, 0.06), 'command': self.togglePanel}
        extraHeight = 0
        if self.WantTitlesPage:
            extraHeight = 0.12
        buttonOptions['geom'] = gui.find('**/friend_button_over')
        buttonOptions['geom_scale'] = 0.12
        self.socialButton = GuiButton(parent=self.buttonsParent, hotkeys=['f', 'shift-f'], hotkeyLabel='F', helpText=PLocalizer.SocialButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleSocial'], pos=(0.01, 0, 1.16 + extraHeight), **buttonOptions)
        self.buttons.append(self.socialButton)
        buttonOptions['geom'] = gui.find('**/compass_small_button_open_over')
        buttonOptions['geom_scale'] = 0.09
        self.radarButton = GuiButton(parent=self.buttonsParent, hotkeys=['c', 'shift-c'], hotkeyLabel='C', helpText=PLocalizer.RadarButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleRadar'], pos=(0.01, 0, 1.04 + extraHeight), **buttonOptions)
        self.buttons.append(self.radarButton)
        buttonPosZ = 0.88
        buttonHeight = 0.12
        if self.WantTitlesPage:
            buttonPosZ += buttonHeight
        buttonOptions['geom'] = gui_main.find('**/world_map_icon')
        buttonOptions['geom_scale'] = 0.095
        self.mapButton = GuiButton(parent=self.buttonsParent, hotkeys=['m', 'shift-m'], hotkeyLabel='M', helpText=PLocalizer.MapButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleMap'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons.append(self.mapButton)
        buttonPosZ -= buttonHeight
        buttonOptions['geom'] = gui.find('**/topgui_icon_weapons')
        buttonOptions['geom_scale'] = 0.18
        self.inventoryButton = GuiButton(parent=self.buttonsParent, hotkeys=['i', 'shift-i'], hotkeyLabel='I', helpText=PLocalizer.WeaponButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleWeapons'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons.append(self.inventoryButton)
        buttonPosZ -= buttonHeight
        buttonOptions['geom'] = gui.find('**/topgui_icon_skills')
        buttonOptions['geom_scale'] = 0.18
        self.levelButton = GuiButton(parent=self.buttonsParent, hotkeys=['k', 'shift-k'], hotkeyLabel='K', helpText=PLocalizer.SkillButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleLevels'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons.append(self.levelButton)
        buttonPosZ -= buttonHeight
        if self.WantClothingPage:
            buttonOptions['geom'] = gui.find('**/topgui_icon_clothing')
            buttonOptions['geom_scale'] = 0.17
            self.clothingButton = GuiButton(parent=self.buttonsParent, helpText=PLocalizer.ClothingButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleClothing'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
            self.buttons.append(self.clothingButton)
            buttonPosZ -= buttonHeight
        if self.WantTitlesPage:
            buttonOptions['geom'] = gui.find('**/topgui_icon_treasure')
            buttonOptions['geom_scale'] = 0.17
            self.titlesButton = GuiButton(parent=self.buttonsParent, hotkeys=['b', 'shift-b'], hotkeyLabel='B', helpText=PLocalizer.TitlesButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleTitles'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
            self.buttons.append(self.titlesButton)
            buttonPosZ -= buttonHeight
        buttonOptions['geom'] = gui.find('**/topgui_icon_ship')
        buttonOptions['geom_scale'] = 0.2
        self.shipsButton = GuiButton(parent=self.buttonsParent, hotkeys=['h', 'shift-h'], hotkeyLabel='H', helpText=PLocalizer.ShipsButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleShips'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons.append(self.shipsButton)
        buttonPosZ -= buttonHeight
        buttonOptions['geom'] = gui.find('**/topgui_icon_treasure')
        buttonOptions['geom_scale'] = 0.16
        self.treasuresButton = GuiButton(parent=self.buttonsParent, hotkeys=['u', 'shift-u'], hotkeyLabel='U', helpText=PLocalizer.TreasuresButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleTreasures'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons.append(self.treasuresButton)
        buttonPosZ -= buttonHeight
        buttonOptions['geom'] = gui.find('**/topgui_icon_journal')
        buttonOptions['geom_scale'] = 0.18
        self.questButton = GuiButton(parent=self.buttonsParent, hotkeys=['j', 'shift-j'], hotkeyLabel='J', helpText=PLocalizer.QuestButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleQuest'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons.append(self.questButton)
        buttonPosZ -= buttonHeight
        self.lookoutButtonNormal = gui.find('**/telescope_button')
        self.lookoutButtonLight = gui.find('**/telescope_button_over')
        self.lookoutButtonSearch3o = gui.find('**/lookout_icon_over_03')
        buttonOptions['geom'] = None
        self.lookoutButton = GuiButton(parent=self.buttonsParent, hotkeys=['l', 'shift-l'], hotkeyLabel='L', helpText=PLocalizer.LookoutButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleLookout'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons.append(self.lookoutButton)
        buttonPosZ -= buttonHeight
        self.lookoutButtonImage = OnscreenImage(parent=self.stickyButtonsParent, image=self.lookoutButtonLight, scale=0.09, pos=(0.065,
                                                                                                                                 0.0,
                                                                                                                                 0.215))
        self.lookoutButtonImage.sourceImage = self.lookoutButtonLight
        self.chestButtonClosed = gui.find('**/treasure_chest_closed_over')
        self.chestButtonOpen = gui.find('**/treasure_chest_open_over')
        self.chestButton = GuiButton(command=self.toggle, parent=self, relief=None, image=self.chestButtonClosed, image_scale=0.15, image_pos=(0.05,
                                                                                                                                               0,
                                                                                                                                               0.06), scale=1.2)
        self.chestHotkeyText = DirectLabel(parent=self.chestButton, relief=None, text='Tab', text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(0.11,
                                                                                                                                                                                0.0), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), textMayChange=1)
        self.buttonsParent.hide()
        self.buttonsParent.setPos(0.2, 0, 0.02)
        self.stickyButtonsParent.hide()
        self.stickyButtonsParent.setPos(0.2, 0, 0.02)
        gui.removeNode()
        return

    def destroy(self):
        self.showButtonsIval.pause()
        del self.showButtonsIval
        self.hideButtonsIval.pause()
        del self.hideButtonsIval
        self.buttonsParent.removeNode()
        del self.buttonsParent
        self.stickyButtonsParent.removeNode()
        del self.stickyButtonsParent
        for button in self.buttons:
            button.destroy()

        del self.buttons
        loader.unloadSfx(self.openSfx)
        loader.unloadSfx(self.closeSfx)
        del self.openSfx
        del self.closeSfx
        GuiTray.GuiTray.destroy(self)

    def togglePanel(self, message, args=None):
        messenger.send(message, [args])

    def toggle(self):
        if not self.isHidden():
            messenger.send(PiratesGlobals.SeaChestHotkey)
            if localAvatar.guiMgr.questPage:
                chestPanel = localAvatar.guiMgr.chestPanel
                if chestPanel.currPageIndex:
                    currPage = chestPanel.pages[chestPanel.currPageIndex]
                    if isinstance(currPage, QuestPage.QuestPage):
                        if not currPage.trackedQuestLabel.isHidden():
                            currPage.updateQuestTitles()

    def isOpen(self):
        return self.state

    def showButtons(self):
        if self.hideButtonsIval.isPlaying():
            self.hideButtonsIval.finish()
        self.showButtonsIval.start()

    def hideButtons(self):
        if self.showButtonsIval.isPlaying():
            self.showButtonsIval.finish()
        for button in self.buttons:
            button.hideDetails()

        self.hideButtonsIval.start()

    def slideOpen(self):
        if not self.state:
            self.openSfx.play()
        self.state = 1
        self.chestButton['image'] = self.chestButtonOpen
        self.showButtons()
        if localAvatar.guiMgr.questPage:
            chestPanel = localAvatar.guiMgr.chestPanel
            if chestPanel.currPageIndex:
                currPage = chestPanel.pages[chestPanel.currPageIndex]
                if isinstance(currPage, QuestPage.QuestPage):
                    if not currPage.trackedQuestLabel.isHidden():
                        currPage.updateQuestTitles()

    def slideClose(self):
        if self.state:
            self.closeSfx.play()
        self.state = 0
        self.chestButton['image'] = self.chestButtonClosed
        self.hideButtons()

    def buildShowHideButtonsIvals(self, includeSticky=True):
        showSequence = Sequence(Func(self.buttonsParent.show))
        showParallel = Parallel(LerpPosInterval(self.buttonsParent, 0.2, pos=Point3(0, 0, 0.02), startPos=self.buttonsParent.getPos, blendType='easeOut'))
        if includeSticky:
            showSequence.append(Func(self.stickyButtonsParent.show))
            showParallel.append(LerpPosInterval(self.stickyButtonsParent, 0.2, pos=Point3(0, 0, 0.02), startPos=self.stickyButtonsParent.getPos, blendType='easeOut'))
        showSequence.append(showParallel)
        self.showButtonsIval = showSequence
        hideParallel = Parallel(LerpPosInterval(self.buttonsParent, 0.2, pos=Point3(0.2, 0, 0.02), startPos=self.buttonsParent.getPos, blendType='easeIn'))
        hideSequence = Sequence(hideParallel, Func(self.buttonsParent.hide))
        if includeSticky:
            hideSequence.append(Func(self.stickyButtonsParent.hide))
            hideParallel.append(LerpPosInterval(self.stickyButtonsParent, 0.2, pos=Point3(0.2, 0, 0.02), startPos=self.stickyButtonsParent.getPos, blendType='easeIn'))
        hideSequence.append(hideParallel)
        self.hideButtonsIval = hideSequence

    def hideChestButton(self):
        self.chestButton.hide()

    def showChestButton(self):
        self.chestButton.show()
# okay decompiling .\pirates\piratesgui\ChestTray.pyc
