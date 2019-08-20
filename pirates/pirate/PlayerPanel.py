from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.avatar import Avatar
from otp.friends import FriendSecret
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.pirate import IdentityPanel

class PlayerPanel(IdentityPanel.IdentityPanel):
    
    def __init__(self, pId):
        self.width = 0.5
        self.pId = pId
        friendInfo = base.cr.playerFriendsManager.getFriendInfo(self.pId)
        self.pName = friendInfo.playerName + '\n\n' + friendInfo.avatarName
        self.avId = base.cr.playerFriendsManager.findAvIdFromPlayerId(self.pId)
        IdentityPanel.IdentityPanel.__init__(self, pId, self.pName, self.width, 0.2)
        self.initialiseoptions(PlayerPanel)
    
    def load(self):
        IdentityPanel.IdentityPanel.load(self)
        self.whisperButton = self.chain.premakeButton(PLocalizer.AvatarPanelWhisper, self.__handleWhisper)
        self.showAvatarButton = self.chain.premakeButton(PLocalizer.AvatarPanelAvatar, self.__handleShowAvatar)
        self.closeButton = self.chain.premakeButton(PLocalizer.lClose, self.hide)
        self.chain.makeButtons()
        gui = loader.loadModelCopy('models/gui/toplevel_gui')
        self.x = gui.find('**/generic_x')
        xLabel = DirectLabel(parent = self.closeButton, relief = None, image = self.x, image_scale = 0.35, image_color = PiratesGuiGlobals.ButtonColor3[0])
        xLabel.setPos(-0.09, 0.0, 0.036)
    
    def determineButtonState(self):
        IdentityPanel.IdentityPanel.determineButtonState(self)
        self.whisperButton['state'] = DGG.DISABLED
        self.showAvatarButton['state'] = DGG.DISABLED
        if self.pId:
            pInfo = base.cr.playerFriendsManager.getFriendInfo(self.pId)
            self.avId = base.cr.playerFriendsManager.findAvIdFromPlayerId(self.pId)
            if pInfo.location == 'Pirates' and pInfo.isOnline():
                self.whisperButton['state'] = DGG.NORMAL
                if self.avId:
                    self.showAvatarButton['state'] = DGG.NORMAL

    def destroy(self):
        IdentityPanel.IdentityPanel.destroy(self)

    def __handleShowAvatar(self):
        friendInfo = base.cr.playerFriendsManager.getFriendInfo(self.pId)
        if friendInfo.avatarId:
            localAvatar.guiMgr.handleAvatarDetails(friendInfo.avatarId, False)

    def __handleRelationships(self):
        base.localAvatar.guiMgr.handleRelationships(None, self.pName, self.pId)

    def __handleList(self):
        messenger.send('guiMgrToggleSocial')
    
    def __handleWhisper(self):
        localAvatar.chatMgr.activateWhisperChat(self.pId, True)
    
    def __handleSecrets(self):
        localAvatar.chatMgr.noWhisper()
        FriendSecret.showFriendSecret()
    
    def __handleFriend(self):
        localAvatar.chatMgr.noWhisper()
        localAvatar.guiMgr.handlePlayerFriendInvite(self.pId, self.pName)
    
    def closePanel(self):
        self.destroy()


