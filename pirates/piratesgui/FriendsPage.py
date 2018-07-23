from pirates.piratesgui import GuiButton
from direct.fsm import StateData
from direct.gui.DirectGui import *
from direct.showbase.ShowBaseGlobal import *
from direct.task import Task
from otp.friends import FriendSecret
from otp.friends.FriendInfo import FriendInfo
from otp.otpbase import OTPGlobals
from panda3d.core import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PirateMemberList, PiratesGuiGlobals, SocialPage


class FriendsPage(SocialPage.SocialPage):

    NumVisible = 6

    def __init__(self):
        SocialPage.SocialPage.__init__(self, PLocalizer.FriendsPageTitle)
        self.initialiseoptions(FriendsPage)
        charGui = loader.loadModel('models/gui/char_gui')
        self.membersList = PirateMemberList.PirateMemberList(10, self, 'FOOLIO HC', height=0.62, memberWidth=0.48)
        self.membersList.setPos(0.001, 0.0, 0.05)
        self.accept(OTPGlobals.AvatarFriendAddEvent, self.addAvatarFriend)
        self.accept(OTPGlobals.AvatarFriendUpdateEvent, self.updateAvatarFriend)
        self.accept(OTPGlobals.AvatarFriendRemoveEvent, self.removeAvatarFriend)
        self.accept(OTPGlobals.PlayerFriendAddEvent, self.addPlayerFriend)
        self.accept(OTPGlobals.PlayerFriendUpdateEvent, self.updatePlayerFriend)
        self.accept(OTPGlobals.PlayerFriendRemoveEvent, self.removePlayerFriend)
        charGui.removeNode()
        self.headingLabel = DirectLabel(parent=self, relief=None, state=DGG.NORMAL, text=PLocalizer.FriendsListLabel, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                          0.0), text_fg=PiratesGuiGlobals.TextFG1, pos=(0.24,
                                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                                        0.694))
        self.maintainNormalButtonState()
        return

    def destroy(self):
        self.stopMaintainNormalButtonState()
        self.ignoreAll()
        self.membersList.destroy()
        SocialPage.SocialPage.destroy(self)

    def addAvatarFriend(self, avId, info):
        self.membersList.addMember(avId, None, PirateMemberList.MODE_FRIEND_AVATAR, info)
        return

    def addPlayerFriend(self, playerId, info):
        self.membersList.addMember(info.avatarId, playerId, PirateMemberList.MODE_FRIEND_PLAYER, info)

    def addAvatarFriends(self, friendData):
        for friendDetail in friendData:
            avId = friendDetail[0]
            info = friendDetail[1]
            self.membersList.addMember(avId, None, PirateMemberList.MODE_FRIEND_AVATAR, info)

        return

    def addPlayerFriends(self, friendData):
        for friendDetail in friendData:
            playerId = friendDetail[0]
            info = friendDetail[1]
            self.membersList.addMember(info.avatarId, playerId, PirateMemberList.MODE_FRIEND_PLAYER, info)

    def updateAvatarFriend(self, avId, info):
        self.membersList.addMember(avId, None, PirateMemberList.MODE_FRIEND_AVATAR, info)
        return

    def updatePlayerFriend(self, playerId, info):
        self.membersList.addMember(None, playerId, PirateMemberList.MODE_FRIEND_PLAYER, info)
        return

    def removeAvatarFriend(self, avId):
        self.membersList.removeMember(avId, None, PirateMemberList.MODE_FRIEND_AVATAR)
        return

    def removePlayerFriend(self, playerId):
        self.membersList.removeMember(None, playerId, PirateMemberList.MODE_FRIEND_PLAYER)
        return

    def maintainNormalButtonState(self):
        taskMgr.remove('friendsMaintainNormalButtonState')
        taskMgr.doMethodLater(15, self.friendsMaintainNormalButtonState, 'friendsMaintainNormalButtonState')

    def stopMaintainNormalButtonState(self):
        taskMgr.remove('friendsMaintainNormalButtonState')

    def friendsMaintainNormalButtonState(self, task):
        for friendButton in self.membersList.members:
            friendButton['state'] = DGG.NORMAL

        return Task.again
