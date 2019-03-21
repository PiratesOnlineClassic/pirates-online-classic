import os
import webbrowser
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import FSM
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.battle import WeaponGlobals
from pirates.reputation import ReputationGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import SkillPage
from pirates.piratesgui import StatusTray
from pirates.piratesgui import ClothingPage
from pirates.piratesgui import TitlesPage
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui import ChestTray
from pirates.piratesgui import ChestPanel
from pirates.piratesgui import GameGui
from pirates.piratesgui import SocialPanel
from pirates.piratesgui import QuestPage
from pirates.piratesgui import ShipPage
from pirates.piratesgui import WeaponPage
from pirates.piratesgui import CollectionPage
from pirates.piratesgui import CollectionMain
from pirates.piratesgui import MapPage
from pirates.piratesgui import TradeInviter
from pirates.piratesgui import TradePanel
from pirates.piratesgui import JournalButton
from pirates.piratesgui import CombatTray
from pirates.piratesgui import FriendsPage
from pirates.piratesgui import CrewPage
from pirates.piratesgui import GuildPage
from pirates.piratesgui import CrewInviter
from pirates.piratesgui import CrewInvitee
from pirates.piratesgui import RadarGui
from pirates.piratesgui import ComboMeter
from pirates.piratesgui.Subtitler import Subtitler
from pirates.piratesgui.TextPrinter import TextPrinter
from pirates.friends import RelationshipChooser
from pirates.friends import FriendInviter
from pirates.friends import IgnoreConfirm
from pirates.friends import GuildInviter
from pirates.friends import FriendInvitee
from pirates.friends import GuildInvitee
from pirates.friends import GuildMember
from pirates.pvp import PVPInviter
from pirates.pvp import PVPInvitee
from pirates.pvp import PVPGlobals
from pirates.pvp import Beacon
from pirates.pirate import PirateAvatarPanel
from pirates.pirate import PlayerPanel
from pirates.piratesgui.ObjectivesPanel import ObjectivesPanel
from pirates.piratesgui.TreasureMapCompletePanel import TreasureMapCompletePanel
from pirates.piratesgui.PVPCompletePanel import PVPCompletePanel
from pirates.pvp.PVPRulesPanel import PVPRulesPanel
from pirates.piratesgui import BarSelectionMenu
from pirates.piratesgui.AttuneMenu import AttuneMenu
from pirates.piratesgui import PVPPanel
from pirates.piratesgui import SheetFrame
from pirates.piratesgui import HighSeasScoreboard
from pirates.piratesgui import HpMeter
from pirates.piratesgui import PiratesTimer
from pirates.piratesgui import PiratesTimerHourglass
from pirates.ship import ShipGlobals
from pirates.uberdog.UberDogGlobals import *
from pirates.piratesgui import MessageStackPanel
from pirates.piratesgui import TrialNonPayerPanel
from pirates.piratesgui import StayTunedPanel
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.uberdog import DistributedInventoryBase
from pirates.economy.EconomyGlobals import *
from pirates.economy import EconomyGlobals
from pirates.piratesgui import LookoutRequestLVL1
from pirates.npc.Townfolk import *
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.reputation import ReputationGlobals
from pirates.reputation import RepChart
from pirates.piratesgui.GameOptions import GameOptions
from pirates.piratesgui.DownloadBlockerPanel import DownloadBlockerPanel
from pirates.piratesgui.TeleportBlockerPanel import TeleportBlockerPanel
from pirates.piratesgui import WorkMeter
from pirates.piratesbase import Freebooter
from pirates.band import BandConstance
from pirates.quest import QuestConstants
from pirates.friends import ReportAPlayer
from pirates.piratesgui import FeedbackPanel
from pirates.piratesgui.SiegeBoard import SiegeBoard
from pirates.speedchat.PSCDecoders import *
from pirates.piratesbase import UserFunnel
from libotp import *
import math

class GuiManager(FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('GuiManager')
    WantClothingPage = base.config.GetBool('want-clothing-page', 0)
    WantTitlesPage = base.config.GetBool('want-titles-page', 0)
    tpMgr = TextPropertiesManager.getGlobalPtr()
    GMgrey = tpMgr.getProperties('grey')
    GMgrey.setGlyphShift(-0.05)
    GMgrey.setGlyphScale(0.9)
    tpMgr.setProperties('GMgrey', GMgrey)
    del tpMgr
    
    def __init__(self, av):
        FSM.FSM.__init__(self, 'GuiManager')
        self.av = av
        self.ignoreAllKeys = False
        self.levelUpIval = None
        self.deathIval = None
        self.oceanIval = None
        self.tmObjectiveList = None
        self.tmCompleteUI = None
        self.showTMCompleteLerp = None
        self.showPVPCompleteLerp = None
        self.gameRulesPanel = None
        self.timer = None
        self.timerHourglass = None
        self.scoreboard = None
        self.relationshipChooser = None
        self.friendInviter = None
        self.friendInvitee = None
        self.guildInviter = None
        self.guildInvitee = None
        self.guildMember = None
        self.crewInviter = None
        self.crewInvitee = None
        self.tradeInviter = None
        self.tradePanel = None
        self.pvpInviter = None
        self.pvpInvitee = None
        self.ignoreConfirm = None
        self.journalButton = None
        self.smokeFader = None
        self.dirtFader = None
        self.smokePanel = None
        self.dirtPanel = None
        self.nonPayerPanel = None
        self.stayTunedPanel = None
        self.workMeter = WorkMeter.WorkMeter()
        self.workMeter.hide()
        self.progressText = None
        self._putBackSocialPanel = 0
        self.gameOptions = None
        self.questPage = None
        self.tmButtonQuick = None
        self.tmButtonSearch = None
        self.chatAllowed = True
        self.chestLock = 0
        self.seaChestAllowed = True
        self.seaChestActive = False
        self.tutorialStatus = PiratesGlobals.TUT_STARTED
        self.skipTutorial = base.config.GetBool('skip-tutorial', 0)
        self.hotkeyButtons = {}
        self.setChatAllowed(True)
        self.setSeaChestAllowed(True)
        self.warningMsg = TextPrinter()
        self.warningMsg.text.reparentTo(aspect2d)
        self.warningMsg.text.setScale(1)
        self.warningMsg.text.setPos(0, 0, -0.485)
        self.warningMsg.text['sortOrder'] = 200
        self.warningMsg.text.setBin('gui-fixed', 0)
        self.warningMsg.text.setDepthTest(0)
        self.warningMsg.text.setDepthWrite(0)
        self.socialPanelReturn = False
        self.questionMarkDisplay = None
        self.feedbackFormActive = False
        self.crewHUDTurnedOff = False
        self.gameGui = GameGui.GameGui(parent = base.a2dTopLeft, state = DGG.DISABLED, relief = None, pos = (-0.2, 0, -0.27), scale = 0.75)
        self.codeShown = 0
        self.messageStack = MessageStackPanel.MessageStackPanel(parent = base.a2dBottomLeft, relief = None, pos = (0.01, 0, 0.6))
        self.__repValues = {}
        self.chestTray = ChestTray.ChestTray(parent = base.a2dBottomRight, parentMgr = self, pos = (-0.131, 0, 0.02), sortOrder = 1)
        self.chestPanel = ChestPanel.ChestPanel(parent = self.chestTray)
        scale = 1.0
        if base.options:
            scale = base.options.getGUIScale()
        
        if self.WantClothingPage:
            self.clothingPage = ClothingPage.ClothingPage()
            self.chestPanel.addPage(self.clothingPage)
        
        self.titlesPage = None
        if self.WantTitlesPage:
            self.titlesPage = TitlesPage.TitlesPage()
            self.chestPanel.addPage(self.titlesPage)
        
        self.mapPage = MapPage.MapPage()
        self.chestPanel.addPage(self.mapPage)
        self.weaponPage = WeaponPage.WeaponPage()
        self.chestPanel.addPage(self.weaponPage)
        self.shipPage = ShipPage.ShipPage()
        self.chestPanel.addPage(self.shipPage)
        self.collectionPage = CollectionPage.CollectionPage()
        self.chestPanel.addPage(self.collectionPage)
        self.collectionMain = CollectionMain.CollectionMain()
        self.chestPanel.addPage(self.collectionMain)
        self.skillPage = SkillPage.SkillPage()
        self.chestPanel.addPage(self.skillPage)
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.combatTray = CombatTray.CombatTray(parent = base.a2dBottomRight)
        self.barSelection = BarSelectionMenu.BarSelectionMenu([], self.combatTray.toggleWeapon)
        self.barSelection.reparentTo(base.a2dBottomCenter)
        self.barSelection.setPos(-0.41, 0, 0.075)
        self.barSelection.setBin('gui-popup', 0)
        self.attuneSelection = AttuneMenu()
        self.attuneSelection.setPos(-0.5, 0, -0.08)
        goldCoin = gui.find('**/treasure_w_coin*')
        self.moneyDisplay = DirectLabel(parent = base.a2dBottomRight, relief = 0, pos = (-0.46, 0, -0.07), scale = 2, geom = goldCoin, geom_scale = 0.18, geom_pos = (0.06, 0, 0.087), text = '', text_font = PiratesGlobals.getPirateBoldOutlineFont(), text_align = TextNode.ACenter, text_scale = 0.02, text_pos = (0.06, 0.045), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1)
        self.moneyDisplay.setName(self.moneyDisplay.uniqueName('moneyDisplay'))
        self.moneyDisplay.flattenStrong()
        if os.getenv('GAME_ENVIRONMENT', 'LIVE') in ['QA', 'DEV', 'TEST']:
            questionMark = gui.find('**/generic_question*')
            self.questionMarkDisplay = DirectButton(parent = base.a2dBottomRight, relief = 0, pos = (-0.32, 0, -0.11), scale = 4.2, geom = questionMark, geom_scale = 0.18, geom_pos = (0.06, 0, 0.087), text = '', textMayChange = 1, command = self.__loadFeedbackPanel)
            self.questionMarkDisplay.setName(self.questionMarkDisplay.uniqueName('questionMarkDisplay'))
            self.questionMarkDisplay.flattenStrong()
            self.questionMarkDisplay.setColor(0.8, 0.7, 0.5, 1)
        
        self.disableOptions = base.config.GetBool('disable-pirates-options', 0)
        if self.disableOptions:
            optionsState = DGG.DISABLED
            optionsHotKeys = []
            optionsKeyLabel = ''
        else:
            optionsState = DGG.NORMAL
            optionsHotKeys = [
                'f7']
            optionsKeyLabel = 'F7'
        self.optionsButton = GuiButton(parent = base.a2dBottomRight, relief = None, hotkeys = optionsHotKeys, hotkeyLabel = optionsKeyLabel, helpText = PLocalizer.OptionsButtonHelp, helpPos = (-0.26, 0, 0.06), helpDelay = 0, helpBin = None, pos = (-0.22, 0, 0.09), canReposition = True, image = gui.find('**/topgui_icon_main_menu'), image_scale = 0.22, sortOrder = 2, command = self.toggleGameOptions, state = optionsState, frameSize = (-0.08, 0.08, -0.08, 0.08))
        if self.disableOptions:
            self.optionsButton.setColorScale(Vec4(0.7, 0.7, 0.7, 0.7))
        else:
            self.optionsButton.hotkeyLabel['text_pos'] = (0.05, -0.07)
        if self.av.getInventory():
            skills = self.av.getInventory().getSkills(self.av.currentWeaponId)
        
        self.combatTray.hideSkills()
        self.accept('localAvatarQuestComplete', self.showQuestCompleteText, extraArgs = [
            PLocalizer.ChatPanelQuestCompletedMsg])
        self.accept('localAvatarQuestUpdate', self.showQuestNotifyText, extraArgs = [
            PLocalizer.ChatPanelQuestUpdatedMsg])
        self.accept('localAvatarQuestItemUpdate', self.showQuestItemNotifyText)
        self.bossMeter = HpMeter.HpMeter(width = 1.2, height = 0.02)
        self.bossMeter.reparentTo(base.a2dTopCenter)
        self.bossMeter.setPos(-0.9, 0, -0.15)
        self.bossMeter.setScale(1.5)
        self.bossMeter.hide()
        self.targetStatusTray = StatusTray.StatusTray(parent = base.a2dTopCenter, pos = (-0.225, 0, -0.25), showSkills = 1)
        self.targetStatusTray.reparentTo(base.a2dTopCenter)
        self.targetStatusTray.hpMeter.setPos(0.04, 0, 0.058)
        self.targetStatusTray.voodooMeter.setPos(0.043, 0, 0.045)
        self.targetStatusTray.voodooMeter.setScale(0.925, 1, 0.325)
        self.targetStatusTray.meterChangeOffset = (-0.3875, 0, -0.192)
        self.shipIcons = loader.loadModel('models/gui/ship_battle')
        self.targetStatusTray.targetFrame2 = DirectFrame(relief = None, parent = self.targetStatusTray, image = self.shipIcons.find('**/ship_battle_speed_bar*'), image_scale = (0.4, 1.0, 0.7), pos = (0.284, 0.0, 0.055), scale = (0.925, 1.0, 0.325))
        self.targetStatusTray.targetFrame = DirectFrame(relief = None, parent = self.targetStatusTray, image = self.shipIcons.find('**/ship_battle_speed_bar*'), image_scale = (0.43, 1.0, 0.7), pos = (0.284, 0.0, 0.078))
        self.targetStatusTray.hideValues = 1
        self.targetStatusTray.hpLabel.hide()
        self.targetStatusTray.voodooLabel.hide()
        self.targetStatusTray.flattenStrong()
        self.targetStatusTray.targetFrame.setBin('fixed', 0)
        self.targetStatusTray.targetFrame2.setBin('fixed', 0)
        self.targetStatusTray.statusEffectsPanel.setScale(0.8)
        self.targetStatusTray.statusEffectsPanel.setPos(-0.15, 0, -0.0525)
        self.targetStatusTray.hide()
        self.targetStatusTray.enemyFrame = DirectFrame(relief = None, parent = self.targetStatusTray, image = self.shipIcons.find('**/ship_battle_dish02*'), image_scale = (0.35, 0.35, 0.35), pos = (-0.25, 0.0, -0.1725))
        self.shipTargetPanel = None
        self.socialPanel = SocialPanel.SocialPanel()
        self.socialPanel.reparentTo(base.a2dBottomRight)
        self.socialPanel.setPos(-0.52, 0.0, 0.15)
        self.socialPanel.hide()
        self.chatPanel = base.chatPanel
        self.friendsPage = FriendsPage.FriendsPage()
        self.socialPanel.addPage(self.friendsPage)
        self.crewPage = CrewPage.CrewPage()
        self.guildPage = GuildPage.GuildPage()
        self.socialPanel.addPage(self.crewPage)
        self.socialPanel.addPage(self.guildPage)
        self.socialPanel.setPage(self.friendsPage)
        self.avatarPanel = None
        self.playerPanel = None
        NametagGlobals.setMasterNametagsActive(1)
        self.accept('gotoAvatar', self.handleGotoAvatar)
        self.accept(PiratesGlobals.AvatarDetailsEvent, self.handleAvatarDetails)
        self.accept(PiratesGlobals.PlayerDetailsEvent, self.handlePlayerDetails)
        self.accept('clickedNametag', self.handleClickedNametag)
        self.accept(BandConstance.BandMakeEvent, self.handleCrewInvite)
        self.accept(BandConstance.BandInvitationEvent, self.handleCrewInvitation)
        self.accept(PiratesGlobals.GuildMakeEvent, self.handleGuildInvite)
        self.accept(PiratesGlobals.GuildInvitationEvent, self.handleGuildInvitation)
        self.accept(PiratesGlobals.FriendMakeEvent, self.handleAvatarFriendInvite)
        self.accept(OTPGlobals.AvatarFriendInvitationEvent, self.handleAvatarFriendInvitation)
        self.accept(OTPGlobals.PlayerFriendInvitationEvent, self.handlePlayerFriendInvitation)
        self.accept(PiratesGlobals.TradeRequestEvent, self.handleTradeInvite)
        self.accept(PiratesGlobals.TradeIncomingEvent, self.handleTradeInvitation)
        self.accept(PiratesGlobals.PVPChallengedEvent, self.handlePVPInvitation)
        self.accept(PiratesGlobals.PVPAcceptedEvent, self.handlePVPAccepted)
        self.accept(OTPGlobals.WhisperIncomingEvent, self.handleWhisperIncoming)
        self.soundWhisper = loader.loadSfx('audio/sfx_gui_whisper.mp3')
        self.radarGui = RadarGui.RadarGui(base.a2dTopRight, self.av, sortOrder = 1)
        self.radarGui.setPos(-(self.radarGui.width), 0, -(self.radarGui.height))
        self.lookoutPopup2DNode = None
        self.lookoutPage = LookoutRequestLVL1.LookoutRequestLVL1(PLocalizer.LookoutPanelTitle, base.cr.matchMaker, self)
        self.chestPanel.addPage(self.lookoutPage)
        self.createLookoutPopup()
        self.accept('highSeasScoreBoardClose', self.removeHighSeasScoreboard)
        self.accept('guiMgrToggleBossMeter', self.toggleBossMeter)
        self.accept('guiMgrToggleSocial', self.toggleSocialPanel)
        self.accept('guiMgrToggleRadar', self.radarGui.toggle)
        self.accept('guiMgrToggleMap', self.showMapPage)
        self.accept('guiMgrToggleWeapons', self.showWeaponPanel)
        if self.WantClothingPage:
            self.accept('guiMgrToggleClothing', self.showClothingPanel)
        
        if self.WantTitlesPage:
            self.accept('guiMgrToggleTitles', self.showTitlesPanel)
        
        self.accept('guiMgrToggleShips', self.showShipPanel)
        self.accept('guiMgrToggleTreasures', self.togglePage, extraArgs = [
            self.collectionMain])
        self.accept('guiMgrToggleLevels', self.showSkillPage)
        self.accept('guiMgrToggleQuest', self.showQuestPanel)
        self.accept('guiMgrToggleLookout', self.showLookoutPanel)
        self.oceanMsg = DirectFrame(parent = self.gameGui, relief = None, text = 'Ocean Zone', text_fg = PiratesGuiGlobals.TextFG2, text_scale = 0.4, text_font = PiratesGlobals.getPirateOutlineFont(), text_shadow = PiratesGuiGlobals.TextShadow, text_align = TextNode.ACenter, frameSize = (-1, 1, -0.5, 0.5), frameColor = (0.5, 0.5, 0.5, 1.0), pos = (2.0, 0, -0.3))
        self.oceanMsg.setScale(0.1)
        self.oceanMsg.hide()
        self.pvpPanel = None
        self.pvpStatus = None
        self.siegeStatus = None
        self.pvpCompleteUI = None
        self.pvpTeamGraphic = None
        self.titler = TextPrinter()
        self.titler.text.setPos(0, 0, 0)
        self.titler.text['text_scale'] = PiratesGuiGlobals.TextScaleTitleJumbo
        self.titler.text.reparentTo(aspect2d)
        self.titler.text.setScale(1)
        self.subtitler = Subtitler()
        self.subtitler.text['text_wordwrap'] = 28
        self.interactionalSubtitler = Subtitler()
        self.progressMsg = TextPrinter()
        self.progressMsg.text.setPos(0, 0, 0.3)
        self.interactionalFrame = None
        self.bg = None
        self.comboMeter = ComboMeter.ComboMeter()
        self.offscreenHitEffects = None
        self.offscreenHitIvals = None
        self.stickySeaChestIcons = []
        self.effectIvals = []
        self.pirateCode = None
        (self.mouseX, self.mouseY) = (0, 0)
        self.reportAPlayer = None
        self.prevTag = None
        self.createPreviewTag()

    def removeHighSeasScoreboard(self):
        self.scoreboard = None

    def setTutorialStatus(self):
        if not self.skipTutorial:
            self.tutorialStatus = self.av.style.getTutorial()
        else:
            self.tutorialStatus = PiratesGlobals.TUT_FINISHED

    def delete(self):
        if self.questionMarkDisplay:
            self.questionMarkDisplay.destroy()
        
        self.hidePVPInstructions()
        self.removePVPStatus()
        self.removePVPUI()
        self.removePVPCompleteUI()
        self.moneyDisplay.destroy()
        self._showMouse()
        self.setChatAllowed(False)
        self.setSeaChestAllowed(False)
        self.ignoreAll()
        if self.pirateCode:
            self.pirateCode.destroy()
        
        self.chestPanel.destroy()
        self.gameGui.destroy()
        self.radarGui.destroy()
        self.combatTray.destroy()
        self.chestTray.destroy()
        self.barSelection.destroy()
        self.attuneSelection.destroy()
        self.comboMeter.destroy()
        self.socialPanel.destroy()
        self.optionsButton.destroy()
        self.removeScoreboard()
        if self.nonPayerPanel:
            self.nonPayerPanel.destroy()
            self.nonPayerPanel = None
        
        if self.stayTunedPanel:
            self.stayTunedPanel.destroy()
            self.stayTunedPanel = None
        
        self.chatPanel = None
        if self.lookoutPage:
            self.lookoutPage.ignore(self.lookoutPopup.getUniqueId())
            self.lookoutPage.destroy()
            self.lookoutPage = None
        
        self.titler.destroy()
        self.subtitler.destroy()
        self.interactionalSubtitler.destroy()
        if self.interactionalFrame:
            self.interactionalFrame.destroy()
        
        self.bossMeter.destroy()
        self.warningMsg.destroy()
        self.progressMsg.destroy()
        self.removeNewQuestIndicator()
        self.targetStatusTray.targetFrame.destroy()
        self.targetStatusTray.enemyFrame.destroy()
        self.targetStatusTray.destroy()
        self.deleteLevelUpText()
        taskMgr.remove('hidePirateCode')
        taskMgr.remove('clearTopTen')
        taskMgr.remove('titles-refresh')
        taskMgr.remove('clearWarning')
        taskMgr.remove('clearTitle')
        taskMgr.remove('clearSubtitle')
        taskMgr.remove('clearProgress')
        if self.oceanIval:
            del self.oceanIval
        
        if self.timer:
            self.timer.destroy()
            self.timer = None
        
        if self.timerHourglass:
            self.timerHourglass.destroy()
            self.timerHourglass = None
        
        if hasattr(self, '_dlBlocker'):
            self._dlBlocker.destroy()
            del self._dlBlocker
        
        if self.tradeInviter:
            self.tradeInviter.destroy()
            del self.tradeInviter
        
        if self.tradePanel:
            self.tradePanel.destroy()
            del self.tradePanel
        
        if self.guildInviter:
            self.guildInviter.destroy()
            del self.guildInviter
        
        if self.guildMember:
            self.guildMember.destroy()
            del self.guildMember
        
        if self.guildInvitee:
            self.guildInvitee.destroy()
            del self.guildInvitee
        
        if self.friendInviter:
            self.friendInviter.destroy()
            del self.friendInviter
        
        if self.friendInvitee:
            self.friendInvitee.destroy()
            del self.friendInvitee
        
        if self.pvpInviter:
            self.pvpInviter.destroy()
            del self.pvpInviter
        
        if self.pvpInvitee:
            self.pvpInvitee.destroy()
            del self.pvpInvitee
        
        if self.crewInviter:
            self.crewInviter.destroy()
            del self.crewInviter
        
        if self.crewInvitee:
            self.crewInvitee.destroy()
            del self.crewInvitee
        
        if self.workMeter:
            self.workMeter.destroy()
            del self.workMeter
        
        if self.avatarPanel:
            self.avatarPanel.destroy()
            del self.avatarPanel
        
        if self.playerPanel:
            self.playerPanel.destroy()
            del self.playerPanel
        
        if self.gameOptions:
            self.gameOptions.destroy()
            del self.gameOptions
        
        NametagGlobals.setMasterNametagsActive(0)
        if self.offscreenHitEffects:
            for effect in self.offscreenHitEffects:
                effect.removeNode()

        del self.offscreenHitEffects
        if self.offscreenHitIvals:
            for ival in self.offscreenHitIvals:
                ival.pause()

        del self.offscreenHitIvals
        del self.av
        self.deleteLookoutPopup()
        for currEffectIval in self.effectIvals:
            currEffectIval.pause()
        
        self.effectIvals = []
        if self.progressText:
            self.showProgressIval.pause()
            self.showProgressIval = None
            self.progressText.destroy()
            self.progressText = None
        
        if self.messageStack:
            self.messageStack.destroy()
            self.messageStack = None
        
        if self.tmButtonQuick:
            self.tmButtonQuick.destroy()
            self.tmButtonQuick = None
        
        if self.tmButtonSearch:
            self.tmButtonSearch.destroy()
            self.tmButtonSearch = None

    def toggleBossMeter(self):
        if self.bossMeter.isHidden():
            self.bossMeter.show()
        else:
            self.bossMeter.hide()
    
    def updateBossMeter(self, hp, maxHp):
        self.bossMeter.update(hp, maxHp)

    def showBossMeter(self):
        if self.bossMeter:
            self.bossMeter.show()

    def hideBossMeter(self):
        if self.bossMeter:
            self.bossMeter.hide()

    def initQuestPage(self):
        if not self.questPage:
            self.questPage = QuestPage.QuestPage()
            self.questPage.updateQuestTitles()
            self.questPage.hide()
            self.chestPanel.addPage(self.questPage, index = 6)
            self.showBlackPearlButtonsForTest()
    
    def toggleShipPageVis(self):
        self.shipPage.toggleVis()
    
    def updateUnspent(self, category, value):
        if self.skillPage:
            self.skillPage.updateUnspent(category, value)
        
        if localAvatar.isWeaponDrawn:
            self.combatTray.initCombatTray(WeaponGlobals.getRepId(localAvatar.currentWeaponId))
    
    def updateSkillUnlock(self, skillId, amt):
        if self.skillPage:
            self.skillPage.updateSkillUnlock(skillId)
        
        if localAvatar.isWeaponDrawn:
            self.combatTray.initCombatTray(WeaponGlobals.getRepId(localAvatar.currentWeaponId))
    
    def updateTonic(self, tonicId):
        self.combatTray.updateBestTonic()
        tonicButton = self.weaponPage.tonicButtons.get(tonicId)
        if tonicButton:
            tonicButton.update()

    def updateShipRepairKit(self, kitId):
        self.combatTray.updateShipRepairKits()
    
    def updateReputation(self, category, value):
        totalReputation = 0
        inv = self.av.getInventory()
        if inv:
            for repCat in ReputationGlobals.getReputationCategories():
                totalReputation += self.av.getInventory().getReputation(repCat)
            
        else:
            self.notify.warning('updateReputation: inventory not created')
        self.gameGui.repMeter.update(totalReputation)
        if self.skillPage.getRep() == category:
            self.skillPage.repMeter.update(value)
        
        weaponPanel = self.weaponPage.weaponPanels.get(category)
        if weaponPanel and weaponPanel.repMeter:
            weaponPanel.repMeter.update(value)
        
        self.combatTray.updateWeaponRep(category, value)
        self.barSelection.updateRep(category, value)
        oldValue = self.__repValues.get(category, None)
        self.__repValues[category] = value
        if inv:
            vtLevel = inv.getStackQuantity(InventoryType.Vitae_Level)
            vtCost = inv.getStackQuantity(InventoryType.Vitae_Cost)
            vtLeft = inv.getStackQuantity(InventoryType.Vitae_Left)
            self.gameGui.updateVitae(vtLevel, vtCost, vtLeft)

    def setEquippedWeapons(self, equippedWeapons):
        if equippedWeapons:
            if self.combatTray:
                self.combatTray.setEquippedWeapons(equippedWeapons)

    def cleanupEquippedWeapons(self):
        if self.combatTray:
            self.combatTray.cleanupEquippedWeapons()

    def setCurrentWeapon(self, currentWeapon, isWeaponDrawn):
        if self.combatTray:
            self.combatTray.setCurrentWeapon(currentWeapon, isWeaponDrawn)

    def refreshInventoryWeapons(self, newWeaponId = None):
        equipped = []
        for weaponId in localAvatar.equippedWeapons:
            if weaponId:
                equipped.append(weaponId)
        
        self.barSelection.update(equipped)
        currentWeapon = localAvatar.guiMgr.combatTray.weaponId
        if currentWeapon and currentWeapon not in equipped:
            skillCategory = getSkillCategory(currentWeapon)
            for weapon in equipped:
                if equipped and getSkillCategory(weapon) == skillCategory and localAvatar.guiMgr.combatTray:
                    localAvatar.l_setCurrentWeapon(weapon, localAvatar.isWeaponDrawn)
                    break
        
        self.weaponPage.refreshList()
    
    def listenMoney(self, coins):
        self.setMoney(coins)
    
    def deleteLevelUpText(self):
        if not self.levelUpIval:
            return
        
        if self.levelUpIval:
            self.levelUpIval.pause()
            self.levelUpIval = None
        
        self.levelUpLabel.destroy()
        self.levelUpCategoryLabel.destroy()
        self.levelUpText.removeNode()
        del self.levelUpSfx

    def createLevelUpText(self):
        if self.levelUpIval:
            return
        
        self.levelUpSfx = loader.loadSfx('audio/treasure_whoosh.mp3')
        self.levelUpSfx.setVolume(0.5)
        self.levelUpText = NodePath('levelUpText')
        self.levelUpLabel = DirectLabel(parent = self.levelUpText, relief = None, text = '', text_font = PiratesGlobals.getPirateOutlineFont(), text_fg = (0.1, 0.7, 0.1, 1), scale = 0.25)
        self.levelUpCategoryLabel = DirectLabel(parent = self.levelUpText, relief = None, text = '', text_font = PiratesGlobals.getPirateOutlineFont(), text_fg = (0.1, 0.7, 0.1, 1), scale = 0.125, pos = (0, 0, -0.125))
        self.levelUpIval = Sequence(Func(self.levelUpSfx.play), Func(self.levelUpText.reparentTo, aspect2d), Parallel(LerpPosInterval(self.levelUpText, 5, pos = Point3(0, 0, 0.3), startPos = Point3(0, 0, -0.3)), Sequence(LerpColorScaleInterval(self.levelUpText, 0.5, colorScale = VBase4(1, 1, 1, 1), startColorScale = VBase4(1, 1, 1, 0)), Wait(4), LerpColorScaleInterval(self.levelUpText, 0.5, colorScale = VBase4(1, 1, 1, 0), startColorScale = VBase4(1, 1, 1, 1)))), Func(self.levelUpText.detachNode))

    def showLevelUpText(self, category, level):
        if self.pageOpen(self.skillPage):
            self.togglePage(self.skillPage)
        
        self.skillPage.update(category)
        self.createLevelUpText()
        self.levelUpLabel['text'] = PLocalizer.LevelUp
        categoryName = PLocalizer.InventoryTypeNames[category]
        if category == InventoryType.OverallRep:
            self.levelUpCategoryLabel['text_fg'] = (1.0, 1.0, 0.2, 1)
            self.levelUpLabel['text_fg'] = (1.0, 1.0, 0.1, 1)
        elif category == InventoryType.PVPTotalInfamyLand or category == InventoryType.PVPTotalInfamySea:
            self.levelUpCategoryLabel['text_fg'] = (1.0, 0.2, 0.2, 1)
            self.levelUpLabel['text_fg'] = (1.0, 0.1, 0.1, 1)
        else:
            self.levelUpCategoryLabel['text_fg'] = (0.1, 0.7, 0.2, 1)
            self.levelUpLabel['text_fg'] = (0.1, 0.7, 0.1, 1)
        self.levelUpCategoryLabel['text'] = '%s Level %s' % (categoryName, level)
        self.levelUpIval.pause()
        self.levelUpIval.start()
        msg = PLocalizer.ChatPanelLevelUpMsg % (categoryName, level)
        base.chatAssistant.receiveGameMessage(msg)
        levelUpReward = ''
        stats = RepChart.getLevelUpStats(category)
        if stats[0] > 0:
            levelUpReward += PLocalizer.LevelUpHPIncrease % stats[0]
        
        if stats[1] > 0:
            levelUpReward += PLocalizer.LevelUpVoodooIncrease % stats[1]
        
        skills = RepChart.getLevelUpSkills(category, level)
        for skillId in skills[0]:
            pointName = PLocalizer.getInventoryTypeName(skillId)
            levelUpReward += PLocalizer.LevelUpSkillPoint % pointName
        
        for skillId in skills[1]:
            skillName = PLocalizer.getInventoryTypeName(skillId)
            levelUpReward += PLocalizer.LevelUpSkillUnlock % skillName
        
        if levelUpReward:
            levelUpReward = PLocalizer.ChatPanelLevelUpMsg % (categoryName, level) + '\n' + levelUpReward
            self.messageStack.addTextMessage(levelUpReward, icon = ('reputation', category))
        
        if self.skillPage.tabBar:
            self.skillPage.tabBar.stash()

    def showQuestItemNotifyText(self, quest, item, note):
        if self.tutorialStatus < PiratesGlobals.TUT_GOT_SEACHEST:
            return None
        
        msg = PLocalizer.QuestItemNotifications[note]
        if note == QuestConstants.QuestItemNotification.AlreadyFound and note == QuestConstants.QuestItemNotification.ValidAttempt or note == QuestConstants.QuestItemNotification.InvalidAttempt:
            itemName = PLocalizer.QuestItemNames[item][1]
        else:
            itemName = PLocalizer.QuestItemNames[item][0]
        if note == QuestConstants.QuestItemNotification.ProgressMadeGoalMet and note == QuestConstants.QuestItemNotification.ProgressMadeGoalUnmet or note == QuestConstants.QuestItemNotification.InvalidAttempt:
            itemName = '%s%s' % (itemName[0].capitalize(), itemName[1:])
        
        self.messageStack.addTextMessage(msg % itemName, icon = ('quests', None))
        (msg, color) = quest.getProgressMsg()
        if msg:
            self.createProgressMsg(msg, color)
        return None

    def showQuestAddedText(self, quest):
        self.av.queueStoryQuest(quest)
        if self.tutorialStatus < PiratesGlobals.TUT_GOT_SEACHEST:
            return None
        
        inv = self.av.getInventory()
        message = PLocalizer.ChatPanelQuestAddedMsg
        localizerText = PLocalizer.QuestStrings.get(quest.questId)
        if localizerText:
            title = localizerText.get('title', quest.questId)
            message += '\n%s' % title
        
        self.messageStack.addTextMessage(message, icon = ('quests', None))
        self.createNewQuestIndicator(quest)
        UserFunnel.logSubmit(0, 'quest_assigned_%s' % quest.questId)
        UserFunnel.logSubmit(1, 'quest_assigned_%s' % quest.questId)
        return None
    
    def showQuestNotifyText(self, message, quest):
        if self.tutorialStatus < PiratesGlobals.TUT_GOT_SEACHEST:
            return
        
        (msg, color) = quest.getProgressMsg()
        if msg:
            self.createProgressMsg(msg, color)

    def showQuestCompleteText(self, message, quest):
        if self.tutorialStatus < PiratesGlobals.TUT_GOT_SEACHEST:
            return None
        
        localizerText = PLocalizer.QuestStrings.get(quest.questId)
        if localizerText:
            title = localizerText.get('title', quest.questId)
            message += '\n%s' % title
        
        self.messageStack.addTextMessage(message, icon = ('quests', None))
        (msg, color) = quest.getProgressMsg()
        if msg:
            self.createProgressMsg(msg, color)
        return None

    def handleTopTen(self, stuff):
        self.topTen = DirectFrame(parent = aspect2d, relief = DGG.FLAT, frameSize = (-0.8, 0.8, -0.7, 0.6), frameColor = PiratesGuiGlobals.FrameColor, pos = (0, 0, 0), text = 'Reputation Top Ten', text_align = TextNode.ACenter, text_scale = 0.04, text_fg = (0.9, 1, 0.9, 1), text_pos = (0, 0.5, 0))
        count = len(stuff)
        for person in stuff:
            slot = DirectFrame(parent = self.topTen, relief = DGG.FLAT, frameSize = (-0.5, 0.5, -0.035, 0.045), frameColor = (1, 1, 1, 1), pos = (0, 0, 0.5 + -0.1 * count), text = '%10d    %s' % (person[2], person[1]), text_scale = 0.04)
            count -= 1
        
        taskMgr.doMethodLater(15.0, self.dismissTopTen, 'clearTopTen')

    def dismissTopTen(self, task):
        self.topTen.hide()
        self.topTen.destroy()

    def handleClickedNametag(self, avatar):
        return self.handleAvatarDetails(avatar.getDoId())

    def handleAvatarDetails(self, avId, posByMouse = True):
        self.clearIdentityPanels()
        self.avatarPanel = PirateAvatarPanel.PirateAvatarPanel(avId)
        if posByMouse:
            pos = base.mouseWatcherNode.getMouse()
            self.avatarPanel.setPos(pos.getX(), pos.getY(), pos.getY())
            self.avatarPanel.wrtReparentTo(aspect2d, sort = 0)
        else:
            self.avatarPanel.reparentTo(aspect2d, sort = 0)
            self.avatarPanel.setPos(0.25, 0, 0.25)
        self.avatarPanel.setScale(1)
        self.avatarPanel.constrainToScreen()
        base.idp = self.avatarPanel

    def hideAvatarDetails(self):
        if self.avatarPanel:
            self.avatarPanel.destroy()
            self.avatarPanel = None

    def handlePlayerDetails(self, playerId):
        self.clearIdentityPanels()
        self.playerPanel = PlayerPanel.PlayerPanel(playerId)
        self.playerPanel.reparentTo(base.a2dTopLeft)
        self.playerPanel.setPos(0.5, 0, -0.7)

    def hidePlayerDetails(self):
        if self.playerPanel:
            self.playerPanel.destroy()
            self.playerPanel = None
    
    def clearIdentityPanels(self):
        if self.avatarPanel:
            self.avatarPanel.destroy()
        
        if self.playerPanel:
            self.playerPanel.destroy()
    
    def handleGotoAvatar(self, avId, avName = None):
        if not launcher.canLeaveFirstIsland():
            self.showDownloadBlocker(DownloadBlockerPanel.Reasons.TELEPORT)
            return
        
        base.cr.teleportMgr.queryAvatarForTeleport(avId)

    def handleRelationships(self, avId, avName, playerId = None):
        if self.relationshipChooser:
            self.relationshipChooser.destroy()
        
        self.relationshipChooser = RelationshipChooser.RelationshipChooser(avId, avName, playerId)
        self.relationshipChooser.setPos(-0.75, 0, -0.295)

    def handleAvatarFriendInvite(self, avId, avName):
        if self.friendInviter:
            self.friendInviter.destroy()
        
        av = base.cr.doId2do.get(avId)
        if av:
            avName = av.getName()
        
        self.friendInviter = FriendInviter.FriendInviter(avId, avName, False)
        self.friendInviter.setPos(-0.75, 0, -0.15)
    
    def handlePlayerFriendInvite(self, avId, avName):
        pInfo = base.cr.playerFriendsManager.findPlayerInfoFromAvId(avId)
        if pInfo:
            avName = pInfo.playerName
        
        if self.friendInviter:
            self.friendInviter.destroy()
        
        self.friendInviter = FriendInviter.FriendInviter(avId, avName, True)
        self.friendInviter.setPos(-0.75, 0, -0.15)

    def handleAvatarFriendInvitation(self, avId, avName = 'Unknown'):
        if self.friendInvitee:
            self.friendInvitee.destroy()
        
        self.friendInvitee = FriendInvitee.FriendInvitee(avId, avName, False)
        if not self.friendInvitee.isEmpty():
            self.friendInvitee.setPos(-0.75, 0, -0.15)

    def handlePlayerFriendInvitation(self, avId, avName = 'Unknown'):
        if self.friendInvitee:
            self.friendInvitee.destroy()
        
        self.friendInvitee = FriendInvitee.FriendInvitee(avId, avName, True)
        if not self.friendInvitee.isEmpty():
            self.friendInvitee.setPos(-0.75, 0, -0.15)

    def handleGuildInviteAccept(self, avid):
        if not self.guildInviter:
            return
        
        self.guildInviter.guildAcceptInvite(avid)
    
    def handleGuildInviteReject(self, avid, reason):
        if not self.guildInviter:
            return
        
        self.guildInviter.guildRejectInvite(avid, reason)

    def handleGuildInvite(self, avId, avName):
        if self.guildInviter:
            self.guildInviter.destroy()
        
        self.guildInviter = GuildInviter.GuildInviter(avId, avName)
        self.guildInviter.setPos(-0.75, 0, -0.15)

    def handleGuildMember(self, avId, avName, guildId, canpromote, candemote, cankick):
        if self.guildMember:
            self.guildMember.destroy()
        
        self.guildMember = GuildMember.GuildMember(avId, avName, guildId, canpromote, candemote, cankick)
        self.guildMember.setPos(-0.75, 0, -0.15)

    def handleGuildInvitation(self, avId, avName, guildId, guildname):
        if self.guildInvitee:
            self.guildInvitee.destroy()
        
        self.guildInvitee = GuildInvitee.GuildInvitee(avId, avName, guildId, guildname)
        self.guildInvitee.setPos(-0.75, 0, -0.15)

    def handleCrewInvite(self, avId, avName):
        if self.crewInviter:
            self.crewInviter.destroy()
        
        self.crewInviter = CrewInviter.CrewInviter()
        self.crewInviter.inviteAvatar(avId, avName)

    def handleCrewLeave(self):
        if self.crewInviter:
            self.crewInviter.destroy()
        
        self.crewInviter = CrewInviter.CrewInviter(self.av.doId, self.av.getName())
        self.crewInviter.setPos(-0.75, 0, -0.15)

    def handleCrewInvitation(self, avId, avName = 'Unknown'):
        if self.crewInvitee:
            self.crewInvitee.destroy()
        
        self.crewInvitee = CrewInvitee.CrewInvitee(avId, avName)
        if not self.crewInvitee.isEmpty():
            self.crewInvitee.setPos(-0.75, 0, -0.15)

    def handleTradeInvite(self, avId, avName):
        if self.tradeInviter:
            self.tradeInviter.destroy()
        
        self.tradeInviter = TradeInviter.TradeInviter(avId, avName)
        self.tradeInviter.setPos(-0.75, 0, -0.15)
    
    def handleTradeInvitation(self, trade):
        if self.tradePanel:
            self.tradePanel.destroy()
        
        self.tradePanel = TradePanel.TradePanel(trade)
        self.tradePanel.setPos(base.a2dLeft, 0, -0.15)
    
    def handlePVPInvite(self, avId, avName):
        if self.pvpInviter:
            self.pvpInviter.destroy()
        
        self.pvpInviter = PVPInviter.PVPInviter(avId, avName)
        self.pvpInviter.setPos(-0.75, 0, -0.15)
    
    def handlePVPInvitation(self, avId, avName = 'Unknown'):
        if self.pvpInvitee:
            self.pvpInvitee.destroy()
        
        self.pvpInvitee = PVPInvitee.PVPInvitee(avId, avName)
        self.pvpInvitee.setPos(-0.75, 0, -0.15)

    def handlePVPAccepted(self, avId, avName = 'Unknown'):
        if self.pvpInvitee:
            self.pvpInvitee.destroy()
            self.pvpInvitee = None
        elif self.pvpInviter:
            self.pvpInviter.destroy()
            self.pvpInviter = None
    
    def handleIgnore(self, avId, avName):
        if self.ignoreConfirm:
            self.ignoreConfirm.destroy()
        
        self.ignoreConfirm = IgnoreConfirm.IgnoreConfirm(avId, avName)
        self.ignoreConfirm.setPos(-0.75, 0, -0.15)

    def handleReport(self, playerId, avId, avName):
        if self.reportAPlayer:
            self.reportAPlayer.destroy()
        
        self.reportAPlayer = ReportAPlayer.ReportAPlayer(playerId, avId, avName)

    def handleWhisperIncoming(self, senderId, msgText):
        if base.cr.avatarFriendsManager.checkIgnored(senderId):
            return
        
        sender = base.cr.identifyAvatar(senderId)
        if sender:
            senderName = sender.getName()
        else:
            self.notify.warning('handleWhisperIncoming: senderId: %s not found' % senderId)
            senderName = 'Unknown'
        whisperType = WhisperPopup.WTNormal
        base.chatAssistant.receiveAvatarWhisperTypedChat(msgText, senderId)
        if self.soundWhisper:
            base.playSfx(self.soundWhisper)

    def showTMUI(self, tm):
        if self.tmObjectiveList == None:
            self.createObjectiveList(tm)
        
        self.tmObjectiveList.show()

    def hideTMUI(self):
        if self.tmObjectiveList:
            self.tmObjectiveList.cleanup()
            self.tmObjectiveList.hide()
            del self.tmObjectiveList
            self.tmObjectiveList = None

    def createObjectiveList(self, tm):
        self.tmObjectiveList = ObjectivesPanel('Treasure Map Objectives', tm)
        self.tmObjectiveList.setPos(base.a2dLeft, 0, 0.45)

    def showTMCompleteUI(self, tm, results):
        return
        if self.tmCompleteUI == None:
            self.createTMCompleteUI(tm, results)
        
        self.tmCompleteUI.setAlphaScale(0)
        self.tmCompleteUI.show()
        if self.showTMCompleteLerp:
            self.showTMCompleteLerp.pause()
        
        self.showTMCompleteLerp = LerpColorScaleInterval(self.tmCompleteUI, 1, Vec4(1, 1, 1, 1))
        self.showTMCompleteLerp.start()

    def hideTMCompleteUI(self):
        if self.showTMCompleteLerp:
            self.showTMCompleteLerp.pause()
            self.showTMCompleteLerp = None
        
        if self.tmCompleteUI:
            self.tmCompleteUI.hide()

    def createTMCompleteUI(self, tm, results):
        self.tmCompleteUI = TreasureMapCompletePanel('Treasure Map Complete', tm, results)
        self.tmCompleteUI.setPos(-1.25, 0, -0.82)

    def showPVPInstructions(self, title, instructions):
        if not self.gameRulesPanel:
            self.gameRulesPanel = PVPRulesPanel('PVPRulesPanel', title, instructions)

    def hidePVPInstructions(self):
        if self.gameRulesPanel:
            self.gameRulesPanel.destroy()
            self.gameRulesPanel = None

    def createPVPStatus(self, holder):
        if self.pvpStatus is None:
            self.pvpStatus = SheetFrame.SheetFrame(PiratesGuiGlobals.PVPCompletePageWidth, PiratesGuiGlobals.PVPCompletePageHeight, PLocalizer.PVPPanelTitle, holder)
            self.pvpStatus.setPos(-1.25, 0, -0.82)
            self.pvpStatus.hide()

    def showPVPStatus(self):
        if self.pvpStatus != None:
            self.pvpStatus.show()

    def hidePVPStatus(self):
        if self.pvpStatus:
            self.pvpStatus.hide()

    def removePVPStatus(self):
        if self.pvpStatus:
            self.pvpStatus.hide()
            self.pvpStatus.destroy()
            self.pvpStatus = None
        

    def removeScoreboard(self):
        if self.scoreboard:
            self.scoreboard.hide()
            self.scoreboard.destroy()
            self.scoreboard = None

    def createSiegeStatus(self, holder):
        if self.siegeStatus is None:
            self.siegeStatus = SiegeBoard(holder)
    
    def showSiegeStatus(self):
        if self.siegeStatus != None:
            self.siegeStatus.show()

    def hideSiegeStatus(self):
        if self.siegeStatus:
            self.siegeStatus.hide()

    def removeSiegeStatus(self):
        if self.siegeStatus:
            self.siegeStatus.destroy()
            self.siegeStatus = None

    def showPVPTimer(self, pvpInstance):
        if pvpInstance.hasTimeLimit():
            timeRemaining = pvpInstance.getTimeLimit() - globalClock.getRealTime() - pvpInstance.gameStartTime
            self.setTimer(timeRemaining, alarmTime = 10)
            self._oldTimerPos = self.timer.getPos()
            self.timer.setPos(0.4, 0, 1.5)

    def createPVPUI(self, holder):
        if self.pvpPanel is None:
            self.pvpPanel = PVPPanel.PVPPanel(PLocalizer.PVPPanelTitle, holder)
            self.pvpPanel.reparentTo(base.a2dLeftCenter)
            self.pvpPanel.setPos(0, 0, 0)
            self.pvpPanel.hide()

    def showPVPUI(self):
        if self.pvpPanel != None:
            self.pvpPanel.show()

    def showPVPTeamIcon(self, team):
        if self.pvpTeamGraphic:
            self.pvpTeamGraphic.removeNode()
            self.pvpTeamGraphic = None
        
        if team > 0:
            self.pvpTeamGraphic = Beacon.getBeaconModel()
            self.pvpTeamGraphic.reparentTo(base.a2dBottomLeft)
            self.pvpTeamGraphic.setColor(PVPGlobals.getTeamColor(team))
            self.pvpTeamGraphic.setScale(0.2)
            self.pvpTeamGraphic.setPos(0.15, 0, 1.5)
    
    def hidePVPUI(self):
        if self.pvpPanel != None:
            self.pvpPanel.hide()
    
    def removePVPUI(self):
        if self.pvpPanel:
            if self.timer:
                self.timer.setPos(self._oldTimerPos)
            
            self.timerExpired()
            if self.pvpTeamGraphic:
                self.pvpTeamGraphic.removeNode()
            
            self.pvpTeamGraphic = None
            self.pvpPanel.cleanup()
            self.pvpPanel.destroy()
            self.pvpPanel = None

    def createPVPCompleteUI(self, pvpInstance):
        if self.pvpCompleteUI is None:
            self.pvpCompleteUI = PVPCompletePanel('Game Complete', pvpInstance)
            self.pvpCompleteUI.setPos(-1.25, 0, -0.82)
            if self.pvpStatus:
                self.pvpStatus.wrtReparentTo(self.pvpCompleteUI)
                self.pvpStatus.setPos(0.01, 0, 0.01)
                self.pvpStatus.show()

    def showPVPCompleteUI(self):
        self.pvpCompleteUI.setAlphaScale(0)
        self.pvpCompleteUI.show()
        if self.showPVPCompleteLerp:
            self.showPVPCompleteLerp.pause()
        
        self.showPVPCompleteLerp = LerpColorScaleInterval(self.pvpCompleteUI, 1, Vec4(1, 1, 1, 1))
        self.showPVPCompleteLerp.start()

    def setPVPResult(self, type, rank, teams, tie):
        if teams == 2:
            if tie:
                self.pvpCompleteUI.setOutcome(PLocalizer.PVPTied)
            elif rank == 1:
                self.pvpCompleteUI.setOutcome(PLocalizer.PVPWon)
            else:
                self.pvpCompleteUI.setOutcome(PLocalizer.PVPLost)
        elif type == 'player':
            self.pvpCompleteUI.setOutcome('%s%s' % (PLocalizer.PVPYourRank, rank))
        elif type == 'team':
            self.pvpCompleteUI.setOutcome('%s%s' % (PLocalizer.PVPYourTeamRank, rank))

    def hidePVPCompleteUI(self):
        if self.showPVPCompleteLerp:
            self.showPVPCompleteLerp.pause()
            self.showPVPCompleteLerp = None
        
        if self.pvpCompleteUI:
            self.pvpCompleteUI.hide()

    def removePVPCompleteUI(self):
        if self.pvpCompleteUI:
            self.pvpCompleteUI.hide()
            self.pvpCompleteUI.destroy()
            self.pvpCompleteUI = None

    def hideTrays(self):
        self.combatTray.hide()
        self.gameGui.hide()
        self.chestTray.hide()
        self.setSeaChestAllowed(False, close = True)
        self.radarGui.hide()
        self.targetStatusTray.hide()
        if not self.socialPanel.isHidden():
            self.socialPanel.hide()
            self._putBackSocialPanel = 1
        
        self.socialPanel.hide()
        self.chatPanel.hide()
        self.av.chatMgr.stop()
        self.av.stopChat()
        self.setChatAllowed(False, close = True)
        self.moneyDisplay.hide()
        if self.questionMarkDisplay:
            self.questionMarkDisplay.hide()
        
        self.optionsButton.hide()
        self.clearIdentityPanels()
        if self.av.getCrewShip():
            self.av.getCrewShip().hideStatusDisplay()
            self.av.getCrewShip().hideTargets()
        
        if self.prevTag:
            self.prevTag.hide()
        
        if self.tmButtonQuick:
            self.tmButtonQuick.hide()
        
        if self.tmButtonSearch:
            self.tmButtonSearch.hide()
        
        if self.questPage:
            self.questPage.trackedQuestLabel.hide()
        
        if self.crewPage.crewHUD.hudOn:
            self.crewPage.crewHUD.setHUDOff()
            self.crewHUDTurnedOff = True

    def showTrays(self):
        self.setTutorialStatus()
        self.optionsButton.show()
        if self.questPage and len(self.questPage.trackedQuestLabel['text']):
            self.questPage.trackedQuestLabel.show()
        
        if self.tutorialStatus >= PiratesGlobals.TUT_GOT_SEACHEST:
            self.chestTray.show()
            self.setSeaChestAllowed(True)
        
        if self.tutorialStatus >= PiratesGlobals.TUT_MET_JOLLY_ROGER:
            self.combatTray.show()
            self.gameGui.show()
            self.chatPanel.show()
            self.av.chatMgr.start()
            self.av.startChat()
            self.setChatAllowed(True)
            self.moneyDisplay.show()
            if self.questionMarkDisplay:
                self.questionMarkDisplay.show()
            
            if self._putBackSocialPanel:
                self.socialPanel.show()
                self._putBackSocialPanel = 0
            
            if self.av.getCrewShip() and self.av.getCrewShip() == self.av.getShip():
                self.av.getCrewShip().showStatusDisplay()
                self.av.getCrewShip().showTargets()
            
            if self.prevTag and not Freebooter.AllAccessHoliday:
                self.prevTag.show()

        if self.tutorialStatus >= PiratesGlobals.TUT_GOT_COMPASS:
            self.radarGui.show()
            if self.tmButtonQuick and base.cr.teleportMgr.inInstanceType != PiratesGlobals.INSTANCE_TM:
                self.tmButtonQuick.show()
            
            if self.tmButtonSearch and base.cr.teleportMgr.inInstanceType != PiratesGlobals.INSTANCE_TM:
                self.tmButtonSearch.show()
        
        if self.crewHUDTurnedOff:
            self.crewPage.crewHUD.setHUDOn()
            self.crewHUDTurnedOff = False

    def getTray(self, gearId):
        categoryType = InventoryId.getCategory(gearId)
        gearRepId = WeaponGlobals.getRepId(gearId)
        if categoryType == ReputationGlobals.WEAPON_CATEGORY:
            if gearRepId == InventoryType.CannonRep:
                pass
        return None

    def setTimer(self, time, showMinutes = 1, mode = None, titleText = '', titleFg = None, infoText = '', cancelText = '', cancelCallback = None, timerExpiredCallback = None, alarmTime = 5):
        self.timerExpired()
        self.timer = PiratesTimer.PiratesTimer(showMinutes = showMinutes, mode = mode, titleText = titleText, titleFg = titleFg, infoText = infoText, cancelText = cancelText, cancelCallback = cancelCallback, alarmTime = alarmTime)
        self.timer.reparentTo(base.a2dBottomLeft)
        self.timer.setPos(0.32, 0, 1.2)
        self.timer.show()
        if timerExpiredCallback:
            self.timer.countdown(time, timerExpiredCallback)
        else:
            self.timer.countdown(time, self.timerExpired)
    
    def timerExpired(self):
        if self.timer:
            self.timer.destroy()
            self.timer = None

    def cancelTimer(self, mode):
        if self.timer and self.timer.mode == mode:
            self.timerExpired()

    def setHourglassTimer(self, time, showMinutes = 1, mode = None, titleText = '', titleFg = None, infoText = '', cancelText = '', cancelCallback = None, timerExpiredCallback = None):
        self.hourglassTimerExpired()
        timer = PiratesTimerHourglass.PiratesTimerHourglass(showMinutes = showMinutes, mode = mode, titleText = titleText, titleFg = titleFg, infoText = infoText, cancelText = cancelText, cancelCallback = cancelCallback)
        self.timerHourglass = timer
        timer.reparentTo(base.a2dBottomLeft)
        timer.setPos(0.13, 0, 1.2)
        timer.setScale(0.2)
        timer.show()
        if timerExpiredCallback:
            timer.countdown(time, timerExpiredCallback)
        else:
            timer.countdown(time, self.hourglassTimerExpired)

    def hourglassTimerExpired(self):
        if self.timerHourglass:
            self.timerHourglass.destroy()
            self.timerHourglass = None

    def cancelHourglassTimer(self, mode):
        if self.timerHourglass and self.timerHourglass.mode == mode:
            self.hourglassTimerExpired()

    def createSubtitle(self, text, color = None):
        self.subtitler.showText(text, color)
        taskMgr.remove('clearSubtitle')
        
        def clearSubtitle(event):
            self.subtitler.clearText()

        taskMgr.doMethodLater(2.0, clearSubtitle, 'clearSubtitle')

    def createTitle(self, text, color = None):
        self.titler.fadeInText(text, color)
        taskMgr.remove('clearTitle')
        self.titler.text['text_scale'] = PiratesGuiGlobals.TextScaleTitleJumbo
        self.titler.text['text_font'] = PiratesGlobals.getPirateOutlineFont()
        self.titler.text['text_shadow'] = PiratesGuiGlobals.TextShadow
        position = Vec3(0.0, 0.0, 0.0)
        self.titler.text.setPos(position)
        
        def clearTitle(event):
            self.titler.fadeOutText()

        taskMgr.doMethodLater(3.0, clearTitle, 'clearTitle')

    def createWarning(self, text, color = PiratesGuiGlobals.TextFG6, duration = 2.0):
        self.warningMsg.showText(text, color)
        taskMgr.remove('clearWarning')
        
        def clearWarningMsg(event):
            self.warningMsg.clearText()

        taskMgr.doMethodLater(duration, clearWarningMsg, 'clearWarning')
    
    def createProgressMsg(self, text, color = None):
        self.progressMsg.showText(text, color)
        taskMgr.remove('clearProgress')
        
        def clearProgressMsg(event):
            self.progressMsg.clearText()

        taskMgr.doMethodLater(5.0, clearProgressMsg, 'clearProgress')

    def createInteractionalSubtitle(self, text, avatar, audio = None, color = None):
        if self.interactionalFrame == None:
            self.interactionalFrame = DirectFrame(parent = aspect2d, relief = DGG.FLAT, state = DGG.DISABLED, frameSize = (-0.8, 0.8, -0.1, 0.1), frameColor = (0, 0, 0, 0), pos = (0.125, 0, 0.79))
        else:
            self.interactionalFrame.show()
        if self.bg == None:
            self.bg = loader.loadModel('models/misc/square_drop_shadow')
            self.bg.reparentTo(self.interactionalFrame)
            self.bg.setTransparency(1)
            self.bg.setColorScale(1, 1, 1, 0.85)
            self.bg.setScale(0.32, 0.032000000000000001, 0.2)
            self.bg.setHpr(0, 90, 0)
            self.interactionalSubtitler.text.reparentTo(self.interactionalFrame)
            self.interactionalSubtitler.text.setScale(1)
            self.interactionalSubtitler.text['text_wordwrap'] = 28
        
        self.interactionalSubtitler.showText(text, color)
        textBounds = self.interactionalSubtitler.text.component('text0').textNode.getFrameActual()
        self.interactionalSubtitler.text.setPos(0, 0, (-(textBounds[3] + textBounds[2]) / 2) * self.interactionalSubtitler.text['text_scale'][1])
        avatar.playCurrentDialogue(audio, 0)

    def clearInteractionalSubtitle(self):
        self.interactionalSubtitler.showText('')
        if self.interactionalFrame:
            self.interactionalFrame.hide()

    def createNewQuestIndicator(self, quest):
        if self.tutorialStatus < PiratesGlobals.TUT_GOT_SEACHEST:
            return
        
        if self.journalButton:
            self.journalButton.addNewQuest()
            self.journalButton['extraArgs'] = [
                quest]
            return
        
        self.journalButton = JournalButton.JournalButton(parent = base.a2dBottomRight, command = self.viewJournal, pos = (-0.12, 0, 0.27), scale = 0.9, extraArgs = [
            quest])
        self.journalButton.addNewQuest()
    
    def viewJournal(self, quest):
        self.showQuestPanel()
        self.questPage.titleList.select(quest.getQuestId())
    
    def removeNewQuestIndicator(self):
        if self.journalButton:
            self.journalButton.removeNewQuest()
            if self.journalButton.questCounter <= 0:
                self.journalButton.destroy()
                self.journalButton = None
    
    def createHighSeasScoreboard(self, portName, missionData, playerData, ship):
        self.scoreboard = HighSeasScoreboard.HighSeasScoreboard(portName, missionData, playerData, ship)
        self.scoreboard.setPos(-(self.scoreboard.width) / 2.0, 0, -0.95)

    def loadOffscreenHitEffects(self):
        if self.offscreenHitEffects:
            return
        
        onColor = Vec4(1, 0, 0, 0.7)
        offColor = Vec4(1, 0, 0, 0)
        left = loader.loadModel('models/textureCards/offscreenFlash')
        left.reparentTo(base.a2dLeftCenter, -1)
        left.setColor(onColor)
        left.setScale(4, 0, 9)
        left.setPosHpr(0.2, 0, 0, 0, 0, 0)
        left.hide()
        left.flattenStrong()
        left.setName('leftHitFlash')
        right = loader.loadModel('models/textureCards/offscreenFlash')
        right.reparentTo(base.a2dRightCenter, -1)
        right.setColor(onColor)
        right.setScale(4, 0, 9)
        right.setPosHpr(-0.2, 0, 0, 0, 0, 180)
        right.hide()
        right.flattenStrong()
        right.setName('rightHitFlash')
        bottom = loader.loadModel('models/textureCards/offscreenFlash')
        bottom.reparentTo(base.a2dBottomCenter, -1)
        bottom.setColor(onColor)
        bottom.setScale(4, 0, 10)
        bottom.setPosHpr(0, 0, 0.25, 0, 0, -90)
        bottom.hide()
        bottom.flattenStrong()
        bottom.setName('bottomHitFlash')
        top = loader.loadModel('models/textureCards/offscreenFlash')
        top.reparentTo(base.a2dTopCenter, -1)
        top.setColor(onColor)
        top.setScale(4, 0, 10)
        top.setPosHpr(0, 0, -0.25, 0, 0, 90)
        top.hide()
        top.flattenStrong()
        top.setName('topHitFlash')
        self.offscreenHitEffects = [
            left,
            bottom,
            right,
            top]
        flashLeft = Sequence(Func(left.show), LerpColorInterval(left, 0.2, onColor, offColor), LerpColorInterval(left, 0.4, offColor, onColor), Func(left.hide))
        flashRight = Sequence(Func(right.show), LerpColorInterval(right, 0.2, onColor, offColor), LerpColorInterval(right, 0.4, offColor, onColor), Func(right.hide))
        flashBottom = Sequence(Func(bottom.show), LerpColorInterval(bottom, 0.2, onColor, offColor), LerpColorInterval(bottom, 0.4, offColor, onColor), Func(bottom.hide))
        flashTop = Sequence(Func(top.show), LerpColorInterval(top, 0.2, onColor, offColor), LerpColorInterval(top, 0.4, offColor, onColor), Func(top.hide))
        self.offscreenHitIvals = [
            flashLeft,
            flashBottom,
            flashRight,
            flashTop]
    
    def hitFromOffscreen(self, attacker):
        self.loadOffscreenHitEffects()
        pos = attacker.getPos(self.av)
        distance = attacker.getDistance(self.av)
        angle = rad2Deg(math.atan2(pos[0], pos[1]))
        if not distance > 6.0:
            if hasattr(self.av, 'gameFSM') or self.av.gameFSM.state == 'Cannon' or self.av.gameFSM.state == 'ShipPilot':
                if angle < -135 or angle > 135:
                    self.offscreenHitIvals[1].start()
                elif angle < -45:
                    self.offscreenHitIvals[0].start()
                elif angle > 45:
                    self.offscreenHitIvals[2].start()
                elif self.av.gameFSM.state == 'Cannon' or self.av.gameFSM.state == 'ShipPilot':
                    self.offscreenHitIvals[3].start()

    def createLookoutPopup(self):
        self.lookoutPopup = NametagGroup()
        self.lookoutPopup.setColorCode(NametagGroup.CCToonBuilding)
        self.lookoutPopup.setAvatar(base.a2dBottomRight)
        self.lookoutPopup2D = NametagFloat2d()
        self.lookoutPopup2D.setContents(Nametag.CSpeech | Nametag.CThought)
        self.lookoutPopup2D.setActive(True)
        self.lookoutPopup.addNametag(self.lookoutPopup2D)
        self.lookoutPopup2DNode = base.a2dBottomRight.attachNewNode(self.lookoutPopup2D.upcastToPandaNode())
        self.lookoutPopup2DNode.setPosHprScale(-0.6, 0, 0.18, 0, 0, 0, 0.04, 0.04, 0.04)
        self.lookoutPopup2DNode.setColorScale(0.92, 0.82, 0.65, 1.0)
        self.lookoutPopup.setFont(PiratesGlobals.getInterfaceFont())
        self.lookoutPopup.manage(base.marginManager)
        self.lookoutPopup.setActive(True)
        self.lookoutPage.accept(self.lookoutPopup.getUniqueId(), self.lookoutPage.msgClick)

    def deleteLookoutPopup(self):
        self.lookoutPopup.unmanage(base.marginManager)
        self.lookoutPopup.removeNametag(self.lookoutPopup2D)
        del self.lookoutPopup
        del self.lookoutPopup2D
        del self.lookoutPopup2DNode

    def moveLookoutPopup(self, chestOpen = True):
        if self.lookoutPopup2DNode:
            if chestOpen:
                self.lookoutPopup2DNode.setPos(-1.7, 0, 0.18)
            else:
                self.lookoutPopup2DNode.setPos(-0.6, 0, 0.18)

    def loadPirateCode(self):
        if self.pirateCode:
            return
        
        self.pirateCode = BorderFrame(parent = base.a2dLeftCenter, frameSize = (0, 1.0, 0, 0.3), pos = (0.25, 0, 0), scale = 0.75)
        self.pirateCode.setName(self.pirateCode.uniqueName('PirateCodeBorderFrame'))
        codeMessage1 = DirectLabel(parent = self.pirateCode, relief = None, text = PLocalizer.PirateCodeWarning1, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), pos = (0.5, 0, 0.18), text_scale = 0.08)
        codeMessage2 = DirectLabel(parent = self.pirateCode, relief = None, text = PLocalizer.PirateCodeWarning2, text_fg = (1, 1, 1, 1), text_shadow = (0, 0, 0, 1), pos = (0.49, 0, 0.09), text_scale = 0.08)
        self.pirateCode.hide()
        self.pirateCodeDialog = base.loadSfx('audio/dialog/will_turner_7.2.b.mp3')

    def showPirateCode(self):
        if not self.pirateCode:
            self.loadPirateCode()
        
        if not self.codeShown:
            self.codeShown = 1
            self.pirateCode.show()
            base.playSfx(self.pirateCodeDialog)
            taskMgr.remove('hidePirateCode')
            taskMgr.doMethodLater(5.0, self.hidePirateCode, 'hidePirateCode')

    def hidePirateCode(self, task = None):
        if not self.pirateCode:
            return
        
        self.pirateCode.hide()
        self.pirateCodeDialog.stop()

    def toggleSocialPanel(self, args = None):
        if self.ignoreAllKeys:
            return
        
        if self.socialPanel.isHidden():
            self.socialPanel.show()
            if self.seaChestActive:
                localAvatar.guiMgr.hideSeaChest()
            
        else:
            self.socialPanel.hide()

    def showWeaponPanel(self, args = None):
        self.togglePage(self.weaponPage, args)
    
    def showSubCollection(self, args = None, setKey = None):
        self.collectionMain.hide(False)
        self.collectionPage.refreshList(setKey)
        self.collectionPage.show()

    def showCollectionMain(self, args = None):
        self.collectionPage.hide()
        self.collectionMain.show()
    
    def showCollectionPanel(self, args = None):
        self.togglePage(self.collectionPage, args)
    
    def showClothingPanel(self, args = None):
        self.togglePage(self.clothingPage, args)
    
    def showTitlesPanel(self, args = None):
        if self.titlesPage:
            self.titlesPage.refresh()
        
        self.togglePage(self.titlesPage, args)

    def showShipPanel(self, args = None):
        self.togglePage(self.shipPage, args)

    def showQuestPanel(self, args = None):
        self.initQuestPage()
        if self.togglePage(self.questPage, args):
            messenger.send('questPageOpened')
            if not self.questPage.trackedQuestLabel.isHidden():
                self.questPage.updateQuestTitles()
            
        else:
            messenger.send('questPageClosed')
        self.removeNewQuestIndicator()

    def showLookoutPanel(self, args = None):
        if not launcher.canLeaveFirstIsland():
            self.showDownloadBlocker(DownloadBlockerPanel.Reasons.LOOKOUT)
        elif self.pageOpen(self.lookoutPage):
            messenger.send('lookoutClosed')
        else:
            messenger.send('lookoutOpened')
        self.lookoutPage.toggleVis(False)
        self.togglePage(self.lookoutPage, args)

    def showDownloadBlocker(self, reason = None):
        if hasattr(self, '_dlBlocker'):
            self._dlBlocker.destroy()
        
        self._dlBlocker = DownloadBlockerPanel(reason)
        self._dlBlocker.setPos(0.1, 0, -0.4)
        self._dlBlocker.show()

    def showTeleportBlocker(self):
        if hasattr(self, '_tpBlocker'):
            self._tpBlocker.destroy()
        
        self._tpBlocker = TeleportBlockerPanel()
        self._tpBlocker.setPos(0.1, 0, -0.4)
        self._tpBlocker.show()

    def showMapPage(self, args = None):
        self.togglePage(self.mapPage, args)

    def showSkillPage(self, args = None):
        result = self.togglePage(self.skillPage, args)
        if result:
            messenger.send('skillPanelOpened')
        else:
            messenger.send('skillPanelClosed')

    def togglePage(self, page, args = None):
        if base.cr.tutorial:
            if not self.questPage or page != self.questPage:
                return False
            
            if self.av.style.tutorial < PiratesGlobals.TUT_GOT_SEACHEST:
                if self.av.gameFSM.state != 'Dialog':
                    return False

        if self.pageOpen(page):
            self.hideSeaChest()
            return False
        elif self.seaChestAllowed:
            self.showSeaChest(page)
            return True
        else:
            return False
    
    def pageOpen(self, page):
        if self.chestPanel.getCurPage() == page and self.chestPanel.isActive():
            return 1
        else:
            return 0

    def setMoney(self, money):
        self.moneyDisplay['text'] = '\x01white\x01%s\x02' % money

    def setUIScale(self, scale):
        base.a2dTopCenter.setScale(scale)
        base.a2dBottomCenter.setScale(scale)
        base.a2dLeftCenter.setScale(scale)
        base.a2dRightCenter.setScale(scale)
        base.a2dTopLeft.setScale(scale)
        base.a2dTopRight.setScale(scale)
        base.a2dBottomLeft.setScale(scale)
        base.a2dBottomRight.setScale(scale)
    
    def setChatAllowed(self, allowed, close = False):
        self.chatAllowed = allowed
        if self.chatAllowed:
            pass

        if close:
            pass

    def setSeaChestAllowed(self, allowed, close = False, priority = 0, reset = False):
        if priority >= self.chestLock:
            self.chestLock = priority
            self.seaChestAllowed = allowed
            if self.seaChestAllowed:
                self.accept(PiratesGlobals.SeaChestHotkey, self.toggleSeaChest)
            else:
                self.ignore(PiratesGlobals.SeaChestHotkey)
                if close:
                    self.hideSeaChest()

        if reset:
            self.chestLock = 0

    def isSeaChestAllowed(self):
        return self.seaChestAllowed

    def _showCursor(self):
        wp = WindowProperties()
        wp.setCursorHidden(0)
        base.win.requestProperties(wp)
        base.graphicsEngine.openWindows()

    def _showMouse(self):
        localAvatar.cameraFSM.disableMouseControl()
        self.combatTray.disableMouseDrawsWeapon()
        self._showCursor()
        base.win.movePointer(0, self.mouseX, self.mouseY)

    def _hideCursor(self):
        wp = WindowProperties()
        wp.setCursorHidden(1)
        base.win.requestProperties(wp)
        base.graphicsEngine.openWindows()
    
    def _hideMouse(self, moveToCenter = True):
        localAvatar.cameraFSM.enableMouseControl()
        self.combatTray.enableMouseDrawsWeapon()
        self._hideCursor()
        if moveToCenter and base.mouseWatcherNode.hasMouse():
            self.mouseX = base.win.getPointer(0).getX()
            self.mouseY = base.win.getPointer(0).getY()
            base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)

    def showSeaChest(self, page = None):
        if page:
            self.chestPanel.setPage(page)
        
        if not self.seaChestActive:
            self.seaChestActive = True
            self.chestPanel.slideOpen()
            self.chestTray.slideOpen()
            self.hideStickySeaChestIcons()
            messenger.send('seachestOpened')
            self.removeNewQuestIndicator()
            self.hidePrevPanel()
        
        if not self.socialPanel.isHidden():
            self.socialPanel.hide()
            self.socialPanelReturn = True

    def hideSeaChest(self):
        if self.seaChestActive:
            self.seaChestActive = False
            self.chestPanel.slideClose()
            self.chestTray.slideClose()
            self.showStickySeaChestIcons()
            self.showPrevPanel()
            messenger.send('seachestClosed')
        
        if self.socialPanelReturn:
            self.socialPanel.show()
            self.socialPanelReturn = False

    def enterWorldMode(self):
        self.enterMouseLook()

    def enterMouseLook(self):
        self.setTutorialStatus()
        if self.tutorialStatus >= PiratesGlobals.TUT_GOT_COMPASS:
            self.setChatAllowed(True)
        
        if self.tutorialStatus >= PiratesGlobals.TUT_GOT_SEACHEST:
            self.setSeaChestAllowed(True)
        
        messenger.send('GuiManagerWorldMode')
        if self.gameOptions:
            self.gameOptions.hide()

    def filterWorldMode(self, request, args):
        return self.filterMouseLook(request, args)

    def filterMouseLook(self, request, args):
        return self.defaultFilter(request, args)

    def exitWorldMode(self):
        self.exitMouseLook()
    
    def exitMouseLook(self):
        pass
    
    def enterPopup(self):
        self.setChatAllowed(False)
        self.setSeaChestAllowed(False)
    
    def filterPopup(self, request, args):
        return self.defaultFilter(request, args)
    
    def exitPopup(self):
        pass
    
    def enterInterface(self, extraArgs = [True, True]):
        (allowChat, allowSeaChest) = extraArgs
        self.setChatAllowed(allowChat, close = not allowChat)
        self.setSeaChestAllowed(allowSeaChest, close = not allowChat)

    def filterInterface(self, request, args):
        return self.defaultFilter(request, args)

    def exitInterface(self):
        pass

    def enterCutscene(self):
        self.hideTrays()
    
    def filterCutscene(self, request, args):
        return self.defaultFilter(request, args)
    
    def exitCutscene(self):
        self.showTrays()

    def toggleSeaChest(self):
        if self.seaChestActive:
            self.hideSeaChest()
        elif self.isSeaChestAllowed():
            self.showSeaChest()

    def hideStickySeaChestIcons(self):
        for currIcon in self.stickySeaChestIcons:
            currIcon.hide()

    def showStickySeaChestIcons(self):
        for currIcon in self.stickySeaChestIcons:
            currIcon.show()

    def addStickySeaChestIcon(self, iconType):
        pass

    def createReceiveEffect(self, uiItem, explain = False):
        if not explain:
            startPos = uiItem.getPos()
            finalPos = Point3(-0.4, 0, -0.4)
            startScale = uiItem.getScale()
            finalScale = Point3(1.0, 1.0, 1.0)
        else:
            uiItem.setScale(0, 0, 0)
            uiItem.setPos(-2, 0, -1.2)
            uiItem.setColorScale(1, 1, 1, 0)
            startPos = uiItem.getPos()
            finalPos = Point3(-0.8, 0, -1.0)
            startScale = uiItem.getScale()
            finalScale = Point3(2, 2, 2)
        receiveDelay = 0.35
        placeDelay = 0.7
        displayIval = Sequence(Parallel(LerpScaleInterval(uiItem, duration = receiveDelay, scale = startScale, blendType = 'easeOut'), LerpColorScaleInterval(uiItem, receiveDelay, Vec4(1, 1, 1, 1), blendType = 'easeIn')), Wait(0.5), Parallel(LerpPosInterval(uiItem, duration = placeDelay, pos = finalPos, blendType = 'easeIn'), LerpScaleInterval(uiItem, duration = placeDelay, scale = finalScale, blendType = 'easeIn')))
        displayIval.start()
        self.addEffectIval(displayIval)

    def addEffectIval(self, ival):
        self.effectIvals.append(ival)

    def clearIvals(self):
        for currEffectIval in self.effectIvals:
            currEffectIval.finish()
        
        self.effectIvals = []

    def toggleGameOptions(self, args = None):
        if self.gameOptions:
            if self.gameOptions.isHidden():
                self.gameOptions.show()
            else:
                self.gameOptions.hide()
        elif base.config.GetBool('want-custom-keys', 0):
            width = 1.8
        else:
            width = 1.6
        height = 1.6
        x = -width / 2
        y = -height / 2
        self.gameOptions = GameOptions('Game Options', x, y, width, height, base.options)
        self.gameOptions.show()
        base.options = self.gameOptions.options

    def showDirtPanel(self):
        if not self.dirtPanel:
            self.createDirtPanel()
        
        if self.dirtFader:
            self.dirtFader.pause()
            self.dirtFader = None
        
        self.dirtPanel.setAlphaScale(1.0)
        self.dirtPanel.show()

    def hideDirtPanel(self):
        if self.dirtPanel is None:
            return
        
        fadeOut = LerpFunctionInterval(self.dirtPanel.setAlphaScale, fromData = self.dirtPanel.getColorScale()[3], toData = 0, duration = 0.3)
        self.dirtFader = Sequence(fadeOut, Func(self.dirtPanel.hide))
        self.dirtFader.start()

    def createSmokePanel(self):
        card = loader.loadModelCopy('models/effects/blinders')
        smokeTex = card.find('**/effectSmokeBlind')
        card.removeNode()
        del card
        self.smokePanel = DirectFrame(parent = aspect2d, relief = None, frameSize = (-4, 4, -4.0, 4.0), frameColor = (0.5, 0.5, 0.5, 0.85), sortOrder = 25, pos = (0, 0, 0.25), image = smokeTex, image_scale = 4.0, suppressMouse = 0, suppressKeys = 0)
        self.smokePanel.hide()

    def createDirtPanel(self):
        card = loader.loadModelCopy('models/effects/blinders')
        dirtTex = card.find('**/effectDirtBlind')
        card.removeNode()
        del card
        self.dirtPanel = DirectFrame(parent = aspect2d, relief = None, frameSize = (-4, 4, -4.0, 4.0), frameColor = (0.5, 0.5, 0.5, 0.85), sortOrder = 25, pos = (0, 0, 0.25), image = dirtTex, image_scale = 4.0, suppressMouse = 0, suppressKeys = 0)
        self.dirtPanel.hide()

    def showSmokePanel(self):
        if not self.smokePanel:
            self.createSmokePanel()
        
        if self.smokeFader:
            self.smokeFader.pause()
            self.smokeFader = None
        
        self.smokePanel.setAlphaScale(1.0)
        self.smokePanel.show()

    def hideSmokePanel(self):
        if self.smokePanel is None:
            return
        
        fadeOut = LerpFunctionInterval(self.smokePanel.setAlphaScale, fromData = self.smokePanel.getColorScale()[3], toData = 0, duration = 0.3)
        self.smokeFader = Sequence(fadeOut, Func(self.smokePanel.hide))
        self.smokeFader.start()
    
    def showQuestProgress(self, questProgress):
        if not self.progressText:
            self.progressText = DirectLabel(parent = base.a2dBottomCenter, relief = None, text = '', text_pos = (0, 0.06), text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, pos = (0, 0, 0.1))
            self.showProgressIval = Sequence(Func(self.progressText.clearColorScale), Func(self.progressText.show), Wait(4.0), LerpColorScaleInterval(self.progressText, 1.0, colorScale = Vec4(1, 1, 1, 0), startColorScale = Vec4(1, 1, 1, 1)), Func(self.progressText.hide))
        
        if not questProgress:
            progressText = PLocalizer.DidNotFindQuestItem
            self.progressText['text'] = progressText
            self.showProgressIval.start()
    
    def toggleGuiForNpcInteraction(self, state):
        self.setTutorialStatus()
        if state == 0:
            self.hideSeaChest()
            self.gameGui.hide()
            self.chatPanel.hide()
            self.radarGui.hide()
            self.combatTray.hide()
            self.moneyDisplay.hide()
            if self.questionMarkDisplay:
                self.questionMarkDisplay.hide()
            
            self.optionsButton.hide()
            self.chestTray.hideChestButton()
            if not self.socialPanel.isHidden():
                self.socialPanel.hide()
                self._putBackSocialPanel = 1
            
            if self.tmButtonQuick:
                self.tmButtonQuick.hide()
            
            if self.tmButtonSearch:
                self.tmButtonSearch.hide()
            
            if self.questPage:
                self.questPage.trackedQuestLabel.hide()
            
            if self.crewPage.crewHUD.hudOn:
                self.crewPage.crewHUD.setHUDOff()
                self.crewHUDTurnedOff = True
            
        elif self.tutorialStatus >= PiratesGlobals.TUT_MET_JOLLY_ROGER:
            self.gameGui.show()
            self.chatPanel.show()
            self.combatTray.show()
            self.moneyDisplay.show()
            if self.questionMarkDisplay:
                self.questionMarkDisplay.show()
            
            self.optionsButton.show()
            self.chestTray.showChestButton()
            if self._putBackSocialPanel:
                self.socialPanel.show()
                self._putBackSocialPanel = 0
            
            if self.questPage and len(self.questPage.trackedQuestLabel['text']):
                self.questPage.trackedQuestLabel.show()

        if self.tutorialStatus >= PiratesGlobals.TUT_GOT_COMPASS:
            self.radarGui.show()
            if self.tmButtonQuick:
                self.tmButtonQuick.show()
            
            if self.tmButtonSearch:
                self.tmButtonSearch.show()

        if self.crewHUDTurnedOff:
            self.crewPage.crewHUD.setHUDOn()
            self.crewHUDTurnedOff = False
    
    def showStayTuned(self, quest = None, focus = None):
        if not self.stayTunedPanel:
            self.stayTunedPanel = StayTunedPanel.StayTunedPanel()
        
        if focus is not None:
            self.stayTunedPanel.setPicFocus(focus)
        
        if quest is not None:
            self.stayTunedPanel.show(quest)
        else:
            self.stayTunedPanel.show()

    def showNonPayer(self, quest = None, focus = None):
        if not __dev__ and localAvatar.isPaid:
            return
        
        if not self.nonPayerPanel:
            self.nonPayerPanel = TrialNonPayerPanel.TrialNonPayerPanel(trial = False)
        
        if quest is not None:
            self.nonPayerPanel.show(quest)
        else:
            self.nonPayerPanel.show()

    def flashOceanMsg(self, oceanZoneName):
        self.oceanMsg.show()
        self.oceanMsg['text'] = PLocalizer.EnterOceanZone % oceanZoneName
        self.oceanMsg.setScale(0.1, 0.1, 0.1)
        self.oceanIval = Sequence(LerpScaleInterval(self.oceanMsg, duration = 2.0, scale = Point3(0.45, 0.45, 0.45), blendType = 'easeOut'), LerpScaleInterval(self.oceanMsg, duration = 3.0, scale = Point3(0.1, 0.1, 0.1), blendType = 'easeOut'), Func(self.oceanMsg.hide))
        self.oceanIval.start()

    def createPreviewTag(self):
        if Freebooter.AllAccessHoliday:
            return
        
        if os.getenv('GAME_SHOW_ADDS') != 'NO':
            return
        
        self.prevTag = DirectFrame(parent = base.a2dTopRight, relief = None, pos = (-0.25, 0, -0.63), scale = 0.8, sortOrder = 0)
        gui2 = loader.loadModelCopy('models/textureCards/basic_unlimited')
        self.imageOne = DirectFrame(parent = self.prevTag, relief = None, image = gui2.find('**/but_message_panel_border'), image_scale = (1, 1, 0.95), scale = 0.4)
        self.titleText1 = DirectLabel(parent = self.prevTag, relief = None, text = PLocalizer.PreviewTitle1, text_align = TextNode.ACenter, text_scale = 0.09, text_fg = PiratesGuiGlobals.TextFG1, text_font = PiratesGlobals.getPirateFont(), text_shadow = PiratesGuiGlobals.TextShadow, pos = (0.0, 0, 0.08))
        self.titleText2 = DirectLabel(parent = self.prevTag, relief = None, text = PLocalizer.PreviewTitle2, text_align = TextNode.ACenter, text_scale = 0.07, text_fg = PiratesGuiGlobals.TextFG1, text_font = PiratesGlobals.getPirateFont(), text_shadow = PiratesGuiGlobals.TextShadow, pos = (0.0, 0, -0.01))
        norm_geom = gui2.find('**/but_nav')
        over_geom = gui2.find('**/but_nav_over')
        down_geom = gui2.find('**/but_nav_down')
        dsbl_geom = gui2.find('**/but_nav_disabled')
        self.upgradeButton = DirectButton(parent = self.prevTag, relief = None, geom = (norm_geom, down_geom, over_geom), pos = (0.0, 0, -0.11), scale = 0.8, command = base.popupBrowser, extraArgs = [
            PLocalizer.URL_UpgradeNow], text = PLocalizer.FirstAddUpgrade, text_fg = PiratesGuiGlobals.TextFG1, text_font = PiratesGlobals.getInterfaceFont(), text_shadow = PiratesGuiGlobals.TextShadow, text_scale = 0.05, text_wordwrap = 9, text_pos = (0, 0.01))

    def showPrevPanel(self):
        if self.prevTag and not Freebooter.AllAccessHoliday:
            self.prevTag.show()

    def hidePrevPanel(self):
        if self.prevTag:
            self.prevTag.hide()

    def showBlackPearlButtonsForTest(self):
        
        def inventoryReceived(inventory):
            if inventory:
                self.invRequest = None
                tms = inventory.getTreasureMapsList()
                for currTm in tms:
                    if currTm.mapId == PiratesGlobals.GAME_STYLE_TM_BLACK_PEARL:
                        currTm.sendUpdate('requestIsEnabled')
                        self.addTreasureMapButtons(currTm)
                        break

        DistributedInventoryBase.DistributedInventoryBase.getInventory(localAvatar.getInventoryId(), inventoryReceived)

    def addTreasureMapButtons(self, tm):
        if os.getenv('GAME_ENVIRONMENT', 'LIVE') in ['QA', 'DEV', 'TEST']:
            helpPos = (-0.26, 0, 0.095)
            self.tmButtonQuick = GuiButton(parent = base.a2dTopRight, text = PLocalizer.PlayTMNow, text_align = TextNode.ACenter, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0.0, -0.01), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 40, image_scale = (0.45, 1, 0.25), command = self.questPage.startTreasureMap, extraArgs = [
                tm], pos = (-0.65, 0, -0.23), helpText = PLocalizer.PlayTMNowHelp, helpPos = helpPos)
            self.tmButtonSearch = GuiButton(parent = base.a2dTopRight, text = PLocalizer.PlayTMLookout, text_align = TextNode.ACenter, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0.0, -0.01), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 40, image_scale = (0.45, 1, 0.25), command = self.questPage.startTreasureMap, extraArgs = [
                tm,
                False], pos = (-0.65, 0, -0.33), helpText = PLocalizer.PlayTMLookoutHelp, helpPos = helpPos)
            self.tmButtonQuick.setColorScale(1, 1, 1, 0.75)
            self.tmButtonSearch.setColorScale(1, 1, 1, 0.75)

    def __loadFeedbackPanel(self):
        FeedbackPanel.FeedbackPanel()
    
    def setIgnoreAllKeys(self, ignore):
        self.ignoreAllKeys = ignore


