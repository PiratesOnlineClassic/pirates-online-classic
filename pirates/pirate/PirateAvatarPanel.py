from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.avatar import Avatar
from otp.otpbase import OTPGlobals
from pirates.friends import PirateFriendSecret
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter
from pirates.pirate import IdentityPanel
from pirates.band import DistributedBandMember
from pirates.piratesgui import TeleportConfirm
GUILDRANK_GM = 3
GUILDRANK_OFFICER = 2
GUILDRANK_MEMBER = 1

class PirateAvatarPanel(IdentityPanel.IdentityPanel):
    
    def __init__(self, avId):
        self.width = 0.5
        self.avId = avId
        self.avName = ''
        self.askingShard = False
        self.TC = None
        member = None
        info = None
        handle = base.cr.identifyAvatar(avId)
        av = base.cr.doId2do.get(avId)
        self.avName = handle.getName()
        self.pId = base.cr.playerFriendsManager.findPlayerIdFromAvId(self.avId)
        if self.pId:
            info = base.cr.playerFriendsManager.getFriendInfo(self.pId)
            self.avName = self.avName + '\n\n' + info.playerName
        elif av:
            self.pId = av.DISLid
        
        IdentityPanel.IdentityPanel.__init__(self, avId, self.avName, self.width, 0.2)
        self.initialiseoptions(PirateAvatarPanel)
        self.avDisableName = 'disable-%s' % self.avId
        self.accept(self.avDisableName, self.determineButtonState)
        self.accept('AvatarIgnoreChange', self.__newIgnore)
        self.accept('generate-%s' % self.avId, self.determineButtonState)
        self.accept('AvatarChange', self.determineButtonState)
        self.accept('AvOnShard%s' % avId, self.__onShard)
        self.accept('kickedFromGuild-%s' % avId, self.__handleRemovedFromGuild)
        self.askingShard = False
        self.determineButtonState()
        if self.titleLabel:
            self.titleLabel['text_scale'] = 0.045
            if Freebooter.getPaidStatus(avId):
                if Freebooter.getFounderStatus(avId):
                    self.titleLabel['text_fg'] = (1, 1, 1, 1)
                    self.titleLabel['text_font'] = PiratesGlobals.getPirateOutlineFont()
                    oldNameText = self.titleLabel['text']
                    self.titleLabel['text'] = '\x05goldFounderIcon\x05 \x01goldFounder\x01%s\x02' % oldNameText
                else:
                    self.titleLabel['text_fg'] = (0.4, 0.3, 0.95, 1)
            else:
                self.titleLabel['text_fg'] = (0.5, 0.5, 0.5, 1)
        
        self.accept('guildMemberUpdated', self.handleGuildMemberUpdated)

    
    def load(self):
        IdentityPanel.IdentityPanel.load(self)
        self.crewButton = self.chain.premakeButton(PLocalizer.AvatarPanelCrew, self.__handleCrew)
        self.friendStart = self.chain.premakeButton(PLocalizer.AvatarPanelRelationships, self.__handleAvatarFriend)
        self.goToButton = self.chain.premakeButton(PLocalizer.AvatarPanelGoTo, self.__handleGoto)
        self.guildButton = self.chain.premakeButton(PLocalizer.AvatarPanelGuild, self.__handleGuild)
        self.ignoreButton = self.chain.premakeButton(PLocalizer.AvatarPanelIgnore, self.__handleIgnore)
        self.reportButton = self.chain.premakeButton(PLocalizer.AvatarPanelReport, self.__handleReport)
        self.showPlayerButton = self.chain.premakeButton(PLocalizer.AvatarPanelPlayer, self.__handleShowPlayer)
        self.challengeButton = self.chain.premakeButton(PLocalizer.AvatarPanelSkirmish, self.__handleChallenge)
        self.whisperButton = self.chain.premakeButton(PLocalizer.AvatarPanelWhisper, self.__handleWhisper)
        self.closeButton = self.chain.premakeButton(PLocalizer.lClose, self.hide)
        self.chain.makeButtons()
        self.showPlayerButton['state'] = DGG.DISABLED
        self.crewButton['state'] = DGG.DISABLED
        self.guildButton['state'] = DGG.DISABLED
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.x = gui.find('**/generic_x')
        xLabel = DirectLabel(parent = self.closeButton, relief = None, image = self.x, image_scale = 0.35, image_color = PiratesGuiGlobals.ButtonColor3[0])
        xLabel.setPos(-0.09, 0.0, 0.036)

    def destroy(self):
        if self.TC:
            self.TC.destroy()
            self.TC = None
        
        self.ignoreAll()
        IdentityPanel.IdentityPanel.destroy(self)
    
    def __handleShowPlayer(self):
        if self.pId:
            localAvatar.guiMgr.handlePlayerDetails(self.pId)
    
    def __handleRelationships(self):
        base.localAvatar.guiMgr.handleRelationships(self.avId, self.avName)
    
    def __handleAvatarFriend(self):
        base.localAvatar.guiMgr.handleAvatarFriendInvite(self.avId, self.avName)

    def __handlePlayerFriend(self):
        base.localAvatar.guiMgr.handlePlayerFriendInvite(self.avId, self.avName)

    def __handleGoto(self):
        if self.TC:
            self.TC.destroy()
            self.TC = None
        
        self.TC = TeleportConfirm.TeleportConfirm(self.avId, self.avName)
        self.TC.setPos(-0.75, 0, -0.3)
    
    def __handleTrade(self):
        base.localAvatar.guiMgr.handleTradeInvite(self.avId, self.avName)

    def __handleChallenge(self):
        base.localAvatar.guiMgr.handlePVPInvite(self.avId, self.avName)

    def __handleWhisper(self):
        base.localAvatar.chatMgr.activateWhisperChat(self.avId, 0)

    def __handleSecrets(self):
        PirateFriendSecret.showFriendSecret()
    
    def __handleGuild(self):
        options = base.cr.guildManager.getOptionsFor(self.avId)
        if options:
            base.localAvatar.guiMgr.handleGuildMember(self.avId, self.avName, localAvatar.guildId, options[0], options[1], options[2])
        else:
            base.localAvatar.guiMgr.handleGuildInvite(self.avId, self.avName)
    
    def __handleRemovedFromGuild(self):
        pass
    
    def __handleCrew(self):
        base.localAvatar.guiMgr.handleCrewInvite(self.avId, self.avName)

    def __handleIgnore(self):
        base.localAvatar.guiMgr.handleIgnore(self.avId, self.avName)

    def __handleReport(self):
        if not self.pId:
            av = base.cr.doId2do.get(self.avId)
            if av:
                self.pId = av.DISLid
            else:
                self.pId = 0
        
        base.localAvatar.guiMgr.handleReport(self.pId, self.avId, self.avName)

    def __handleGenerateAvatar(self, avatar):
        pass

    def __handleDisableAvatar(self):
        self.destroy()

    def __handleList(self):
        messenger.send('guiMgrToggleSocial')

    def closePanel(self):
        self.destroy()
    
    def __newIgnore(self, avId = None):
        ignoreText = PLocalizer.AvatarPanelIgnore
        if base.cr.avatarFriendsManager.checkIgnored(self.avId):
            ignoreText = PLocalizer.AvatarPanelStopIgnore
        
        self.ignoreButton['text'] = ignoreText
        self.determineButtonState()

    def askShard(self, avId):
        if not self.askingShard:
            self.askingShard = True
            localAvatar.askAvOnShard(avId)
    
    def __onShard(self, onShard = True):
        self.askingShard = False
        if onShard:
            self.crewButton['state'] = DGG.NORMAL
            self.guildButton['state'] = DGG.NORMAL
            self.checkGuildRank(True)
        else:
            self.crewButton['state'] = DGG.DISABLED
            if not base.cr.guildManager.isInGuild(self.avId):
                self.guildButton['state'] = DGG.DISABLED

    def determineButtonState(self, extra = None):
        IdentityPanel.IdentityPanel.determineButtonState(self)
        if self.avId:
            infoPlayer = base.cr.playerFriendsManager.findPlayerInfoFromAvId(self.avId)
            if infoPlayer:
                self.showPlayerButton['state'] = DGG.NORMAL
            
            handle = base.cr.identifyAvatar(self.avId)
            online = handle and handle.isOnline()
            self.askShard(self.avId)
            if not base.cr.avatarFriendsManager.checkIgnored(self.avId):
                self.whisperButton['state'] = DGG.NORMAL
                self.goToButton['state'] = DGG.NORMAL
                self.challengeButton['state'] = DGG.NORMAL
                self.checkGuildRank()
                inPVP = base.cr.activeWorld and base.cr.activeWorld.getType() == PiratesGlobals.INSTANCE_PVP
                inSameCrew = DistributedBandMember.DistributedBandMember.areSameCrew(localAvatar.doId, self.avId)
                if not online:
                    self.crewButton['state'] = DGG.DISABLED
                    self.guildButton['state'] = DGG.DISABLED
                    self.whisperButton['state'] = DGG.DISABLED
                    self.goToButton['state'] = DGG.DISABLED
                    self.challengeButton['state'] = DGG.DISABLED
                elif inPVP or inSameCrew:
                    self.challengeButton['state'] = DGG.DISABLED
                
            else:
                self.crewButton['state'] = DGG.DISABLED
                self.guildButton['state'] = DGG.DISABLED
                self.whisperButton['state'] = DGG.DISABLED
                self.showPlayerButton['state'] = DGG.DISABLED
                self.goToButton['state'] = DGG.DISABLED
                self.challengeButton['state'] = DGG.DISABLED
            self.checkGuildRank()
        else:
            self.self.crewButton['state'] = DGG.DISABLED
            self.whisperButton['state'] = DGG.DISABLED
            self.goToButton['state'] = DGG.DISABLED
            self.challengeButton['state'] = DGG.DISABLED
            self.ignoreButton['state'] = DGG.DISABLED
            self.reportButton['state'] = DGG.DISABLED
            self.showPlayerButton['state'] = DGG.DISABLED

    def checkGuildRank(self, onlyDisable = False):
        if not base.localAvatar.getGuildId() or base.localAvatar.getGuildRank() < GUILDRANK_OFFICER:
            self.guildButton['state'] = DGG.DISABLED
        elif not onlyDisable:
            self.guildButton['state'] = DGG.NORMAL
    
    def handleGuildMemberUpdated(self, avId):
        self.checkGuildRank()

    def constrainToScreen(self):
        height = self.getHeight()
        width = self.getWidth()
        cHeight = self.chain.getHeight()
        pos = self.getPos(aspect2d)
        x = max(min(pos[0], base.a2dRight - width), base.a2dLeft)
        z = max(min(pos[2], base.a2dTop - height), base.a2dBottom + cHeight)
        return self.setPos(aspect2d, x, 0, z)


