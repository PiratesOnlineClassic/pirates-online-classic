# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.PirateMemberList
from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import StateData
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import SocialPage
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import TeleportConfirm
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPGlobals
from otp.friends.FriendInfo import FriendInfo
from pirates.piratesbase import Freebooter
from pirates.band import BandConstance
import GuiButton
from direct.showbase.DirectObject import *
import copy
MODE_FRIEND_AVATAR = 0
MODE_FRIEND_PLAYER = 1
MODE_CREW = 2
MODE_GUILD = 3
MODE_CREW_HUD = 4
MODE_CREW_HUD_SEA = 5

class PirateMemberButton(GuiButton.GuiButton):
    __module__ = __name__
    memberImageColor = (Vec4(0.31, 0.3, 0.3, 1), Vec4(0.41, 0.4, 0.4, 1), Vec4(0.41, 0.4, 0.4, 1), Vec4(0.21, 0.2, 0.2, 1))
    OnlineTextColor = (1, 1, 1, 1)
    OnlineButtonColor = VBase4(0.7, 0.7, 0.7, 1.0)
    OfflineButtonColor = VBase4(0.3, 0.3, 0.3, 1.0)
    OnlineSubtextColor = (0.8, 0.8, 0.8, 1)
    OfflineTextColor = (0.45, 0.45, 0.45, 1)
    LocalTextColor = PiratesGuiGlobals.TextFG1

    def __init__(self, owner, avId, playerId, mode, modeInfo=None):
        self.avId = avId
        self.playerId = playerId
        self.avName = None
        self.mode = mode
        self.modeInfo = modeInfo
        self.owner = owner
        self.hp = 0
        self.maxHp = 0
        self.online = False
        if self.mode in [MODE_CREW, MODE_CREW_HUD, MODE_CREW_HUD_SEA]:
            text = modeInfo.name
            self.avname = text
            self.hp = modeInfo.hp
            self.maxHp = modeInfo.maxHp
        if self.mode == MODE_CREW_HUD:
            GuiButton.GuiButton.__init__(self, parent=self.owner.memberFrame.getCanvas(), text='', text_scale=PiratesGuiGlobals.TextScaleMed, text_pos=(0.01, self.owner.memberOffset), text_align=TextNode.ALeft, text_fg=self.OfflineTextColor, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, text_wordwrap=40, image_scale=(self.owner.memberWidth, 1.0, self.owner.memberHeight * 2.62), image_pos=(0.31, 0.0, self.owner.memberHeight * 0.5), command=self.handlePress, image=None)
            self.hpMeter = DirectWaitBar(parent=self, relief=DGG.RAISED, borderWidth=(0.004,
                                                                                      0.004), range=self.maxHp, value=self.hp, frameColor=(0.05,
                                                                                                                                           0.05,
                                                                                                                                           0.05,
                                                                                                                                           1), barColor=(0.1,
                                                                                                                                                         0.7,
                                                                                                                                                         0.1,
                                                                                                                                                         1), pos=(0.15,
                                                                                                                                                                  0,
                                                                                                                                                                  0.012), frameSize=(0,
                                                                                                                                                                                     0.25,
                                                                                                                                                                                     0,
                                                                                                                                                                                     0.02), text='%s/%s' % (self.hp, self.maxHp), text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleTiny, text_fg=PiratesGuiGlobals.TextFG3, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.27,
                                                                                                                                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                                                                                                                                0.005), textMayChange=1)
            self.statusLabel = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(1.53,
                                                                                                                                                                0.02), text_fg=self.OnlineSubtextColor, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1)
        else:
            if self.mode == MODE_CREW_HUD_SEA:
                GuiButton.GuiButton.__init__(self, parent=self.owner.memberFrame.getCanvas(), text='', text_scale=PiratesGuiGlobals.TextScaleMed, text_pos=(0.01, self.owner.memberOffset), text_align=TextNode.ALeft, text_fg=self.OfflineTextColor, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, text_wordwrap=40, image_scale=(self.owner.memberWidth, 1.0, self.owner.memberHeight * 2.62), image_pos=(0.31, 0.0, self.owner.memberHeight * 0.5), command=self.handlePress, image=None)
                self.hpMeter = DirectWaitBar(parent=self, relief=DGG.RAISED, borderWidth=(0.004,
                                                                                          0.004), range=self.maxHp, value=self.hp, frameColor=(0.05,
                                                                                                                                               0.05,
                                                                                                                                               0.05,
                                                                                                                                               1), barColor=(0.1,
                                                                                                                                                             0.7,
                                                                                                                                                             0.1,
                                                                                                                                                             1), pos=(0.15,
                                                                                                                                                                      0,
                                                                                                                                                                      0.012), frameSize=(0,
                                                                                                                                                                                         0.25,
                                                                                                                                                                                         0,
                                                                                                                                                                                         0.02), text='%s/%s' % (self.hp, self.maxHp), text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleTiny, text_fg=PiratesGuiGlobals.TextFG3, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.27,
                                                                                                                                                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                                                                                                                                                    0.005), textMayChange=1, scale=0.8)
                self.statusLabel = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(1.53,
                                                                                                                                                                    0.02), text_fg=self.OnlineSubtextColor, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, scale=0.8)
            else:
                GuiButton.GuiButton.__init__(self, parent=self.owner.memberFrame.getCanvas(), text='', text_scale=PiratesGuiGlobals.TextScaleMed, text_pos=(0.01, self.owner.memberOffset), text_align=TextNode.ALeft, text_fg=self.OfflineTextColor, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, text_wordwrap=40, image_scale=(self.owner.memberWidth, 1.0, self.owner.memberHeight * 2.62), image_pos=(0.21, 0.0, self.owner.memberHeight * 0.5), command=self.handlePress)
                self.hpMeter = DirectWaitBar(parent=self, relief=DGG.RAISED, borderWidth=(0.004,
                                                                                          0.004), range=self.maxHp, value=self.hp, frameColor=(0.05,
                                                                                                                                               0.05,
                                                                                                                                               0.05,
                                                                                                                                               1), barColor=(0.1,
                                                                                                                                                             0.7,
                                                                                                                                                             0.1,
                                                                                                                                                             1), pos=(0.01,
                                                                                                                                                                      0,
                                                                                                                                                                      0.012), frameSize=(0,
                                                                                                                                                                                         0.25,
                                                                                                                                                                                         0,
                                                                                                                                                                                         0.02), text='%s/%s' % (self.hp, self.maxHp), text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleTiny, text_fg=PiratesGuiGlobals.TextFG3, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.256,
                                                                                                                                                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                                                                                                                                                    0.005), textMayChange=1)
                self.statusLabel = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(0.03,
                                                                                                                                                                    0.02), text_fg=self.OnlineSubtextColor, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1)
        self.initialiseoptions(PirateMemberButton)
        self.hpMeter.hide()
        self.statusLabel.hide()
        gui = loader.loadModel('models/gui/toplevel_gui')
        shipImage = (
         gui.find('**/topgui_icon_ship'), gui.find('**/topgui_icon_ship'), gui.find('**/topgui_icon_ship'))
        self.shipIcon = DirectButton(parent=self, relief=None, image=shipImage, image0_color=VBase4(1.0, 1.0, 1.0, 1.0), image1_color=VBase4(0.4, 0.4, 0.4, 1.0), image2_color=VBase4(0.0, 0.9, 0.0, 1.0), image_scale=0.1, pos=(0.35,
                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                 0.035), command=self.handleShipPress)
        self.shipIcon.shipId = None
        self.shipIcon.hide()
        icon = loader.loadModel('models/gui/compass_main')
        self.onlineIcon = icon.find('**/icon_sphere').copyTo(self)
        self.onlineIcon.setPos(0.395, 0, 0.035)
        self.onlineIcon.setScale(0.2)
        self.onlineIcon.hide()
        self.accept('press-wheel_up-%s' % self.guiId, self.owner.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.guiId, self.owner.mouseWheelDown)
        self.update()
        return

    def destroy(self):
        GuiButton.GuiButton.destroy(self)
        self.modeInfo = None
        self.ignoreAll()
        return

    def __cmp__(self, other):
        if other is None:
            return -1
        if self.online and not other.online:
            return -1
        else:
            if not self.online and other.online:
                return 1
        if self.mode == MODE_CREW or self.mode == MODE_CREW_HUD or self.mode == MODE_CREW_HUD_SEA:
            if not hasattr(other, 'modeInfo') or not other.modeInfo:
                return 1
            elif self.modeInfo:
                if self.modeInfo.isManager:
                    return -1
                elif other.modeInfo.isManager:
                    return 1
        if self.mode == MODE_GUILD:
            if not hasattr(other, 'modeInfo') or not other.modeInfo:
                return 1
            elif self.modeInfo:
                if self.modeInfo[2] > other.modeInfo[2]:
                    return -1
                elif self.modeInfo[2] < other.modeInfo[2]:
                    return 1
        if not hasattr(other, 'avId'):
            return 1
        if self.mode == MODE_FRIEND_PLAYER and other.mode == MODE_FRIEND_AVATAR:
            return -1
        else:
            if self.mode == MODE_FRIEND_AVATAR and other.mode == MODE_FRIEND_PLAYER:
                return 1
            else:
                return cmp(self['text'].lower(), other['text'].lower())
        return

    def updateGuild(self):
        if self.mode == MODE_GUILD:
            rank = localAvatar.getGuildRank()
            self.modeInfo = [self.modeInfo[0], self.modeInfo[1], rank, self.modeInfo[3]]
        self.update()

    def updateShip(self, shipId, shipHasSpace=0):
        if shipId:
            self.shipIcon.show()
        else:
            self.shipIcon.hide()

    def updateOnline(self, status):
        self.onlineIcon.show()
        if status:
            self.onlineIcon.setColor(0.1, 1.0, 0.1, 0.6)
        else:
            self.onlineIcon.setColor(0.6, 0.1, 0.1, 0.6)

    def updateHp(self, hp, maxHp):
        self.hp = hp
        self.maxHp = maxHp
        self.hpMeter['text'] = '%s/%s' % (hp, maxHp)
        self.hpMeter['range'] = maxHp
        self.hpMeter['value'] = hp
        hpFraction = float(hp) / float(maxHp)
        if hpFraction >= 0.5:
            self.hpMeter['barColor'] = (0.1, 0.7, 0.1, 1)
        else:
            if hpFraction >= 0.25:
                self.hpMeter['barColor'] = (1.0, 1.0, 0.1, 1)
            else:
                self.hpMeter['barColor'] = (1.0, 0.0, 0.0, 1)

    def update(self, modeInfo=None):
        if modeInfo:
            self.modeInfo = modeInfo
        text = 'AV %s' % self.avId
        friendInfo = None
        statusText = 'status HC'
        online = False
        text_cap = 22
        state = DGG.NORMAL
        text_fg = self.OnlineTextColor
        buttonColor = self.OnlineButtonColor
        statusTextFg = self.OnlineSubtextColor
        self.ignore('Guild Status Updated')
        if self.mode == MODE_FRIEND_AVATAR:
            friendInfo = base.cr.avatarFriendsManager.getFriendInfo(self.avId)
            text = friendInfo.getName()
            self.avName = text
            self.statusLabel.hide()
            self.shipIcon.setPos(0.35, 0, 0.035)
            shipId = base.cr.avatarFriendsManager.getShipId(self.avId)
            if shipId:
                self.shipIcon.shipId = shipId
                state = base.cr.avatarFriendsManager.getShipId2State(shipId)
                self.updateShip(shipId, state)
                text_cap = 18
            else:
                self.updateShip(None)
        else:
            if self.mode == MODE_FRIEND_PLAYER:
                friendInfo = base.cr.playerFriendsManager.getFriendInfo(self.playerId)
                text = friendInfo.playerName
                self.avName = text
                self.statusLabel.hide()
                self.shipIcon.setPos(0.35, 0, 0.035)
                shipId = base.cr.playerFriendsManager.getShipId(self.playerId)
                if shipId:
                    self.shipIcon.shipId = shipId
                    state = base.cr.playerFriendsManager.getShipId2State(shipId)
                    self.updateShip(shipId, state)
                    text_cap = 18
                else:
                    self.updateShip(None)
            else:
                if self.mode == MODE_CREW or self.mode == MODE_CREW_HUD or self.mode == MODE_CREW_HUD_SEA:
                    text = self.modeInfo.name
                    self.avName = text
                    self.updateHp(self.modeInfo.hp, self.modeInfo.maxHp)
                    self.statusLabel.hide()
                    self.hpMeter.show()
                    self.shipIcon.setPos(0.395, 0, 0.04)
                else:
                    if self.mode == MODE_GUILD:
                        if self.avId == localAvatar.doId:
                            self.accept('Guild Status Updated', self.updateGuild)
                        text = self.modeInfo[1]
                        statusText = self.getGuildRankName(self.modeInfo[2])
                    else:
                        return
        if self.mode in [MODE_FRIEND_AVATAR, MODE_FRIEND_PLAYER, MODE_GUILD]:
            if self.avId == localAvatar.doId:
                online = True
            else:
                if friendInfo:
                    online = friendInfo.isOnline()
                else:
                    if self.mode == MODE_GUILD:
                        online = self.modeInfo[3]
            self.updateOnline(online)
            if online:
                text_fg = self.OnlineTextColor
            else:
                text_fg = self.OfflineTextColor
                buttonColor = self.OfflineButtonColor
                self.updateShip(None)
            self.online = online
        if len(text) > text_cap:
            text = text[0:text_cap]
        if self.mode == MODE_GUILD:
            self.statusLabel['text'] = statusText
            self.statusLabel.show()
            if self.avId == localAvatar.doId:
                state = DGG.DISABLED
                text_fg = self.LocalTextColor
        if self.mode == MODE_CREW_HUD:
            self.configure(state=state, text=text, text_fg=text_fg, image_color=buttonColor, text_pos=(0.15,
                                                                                                       0.04,
                                                                                                       3.45))
        else:
            if self.mode == MODE_CREW_HUD_SEA:
                self.configure(state=state, text=text, text_fg=text_fg, image_color=buttonColor, text_pos=(0.15,
                                                                                                           0.04,
                                                                                                           1.5), text_scale=0.0375)
            else:
                self.configure(state=state, text=text, text_fg=text_fg, image_color=buttonColor)
        return

    def handleShipPress(self):
        TC = TeleportConfirm.TeleportConfirm(self.avId, self.avName)
        TC.setPos(-0.75, 0, -0.3)

    def handlePress(self):
        if self.mode == MODE_FRIEND_PLAYER:
            messenger.send(PiratesGlobals.PlayerDetailsEvent, [self.playerId])
        else:
            if self.mode in (MODE_FRIEND_AVATAR, MODE_GUILD, MODE_CREW, MODE_CREW_HUD, MODE_CREW_HUD_SEA):
                messenger.send(PiratesGlobals.AvatarDetailsEvent, [self.avId, False])

    def getGuildRankName(self, rank):
        if rank == 3:
            statusText = PLocalizer.GuildRankLeader
        else:
            if rank == 2:
                statusText = PLocalizer.GuildRankSubLead
            else:
                statusText = PLocalizer.GuildRankMember
        return statusText

    def updateGuildRank(self, rank):
        self.statusLabel['text'] = self.getGuildRankName(rank)


class PirateMemberList(DirectObject):
    __module__ = __name__

    def __init__(self, numShown, parent, title=None, height=0.6, memberHeight=0.065, memberOffset=0.021, memberWidth=0.45, bottom=0, hud=False, width=0.48):
        if hasattr(self, 'initialized'):
            self.arrangeMembers()
            return
        self.shown = numShown
        self.memberHeight = memberHeight
        self.memberWidth = memberWidth
        self.memberOffset = memberOffset
        self.title = title
        self.width = width
        self.bottom = bottom
        self.height = height
        self.hud = hud
        self.baseFrame = DirectFrame(relief=None, parent=parent)
        if self.hud:
            self.baseFrame['state'] = DGG.DISABLED
        self.members = []
        self.setup()
        self.arrangeMembers()
        self.initialized = 1
        self.show()
        return

    def mouseWheelUp(self, task=None):
        if len(self.members) > self.shown:
            amountScroll = self.shown / (1.0 * len(self.members))
            self.memberFrame.verticalScroll['value'] -= amountScroll

    def mouseWheelDown(self, task=None):
        if len(self.members) > self.shown:
            amountScroll = self.shown / (1.0 * len(self.members))
            self.memberFrame.verticalScroll['value'] += amountScroll

    def countMembers(self):
        return len(self.members)

    def show(self):
        self.baseFrame.show()
        self.accept('press-wheel_up-%s' % self.memberFrame.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.memberFrame.guiId, self.mouseWheelDown)
        self.accept('press-wheel_up-%s' % self.memberFrame.verticalScroll.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.memberFrame.verticalScroll.guiId, self.mouseWheelDown)
        self.accept('press-wheel_up-%s' % self.memberFrame.verticalScroll.thumb.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.memberFrame.verticalScroll.thumb.guiId, self.mouseWheelDown)
        self.accept('press-wheel_up-%s' % self.memberFrame.verticalScroll.incButton.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.memberFrame.verticalScroll.incButton.guiId, self.mouseWheelDown)
        self.accept('press-wheel_up-%s' % self.memberFrame.verticalScroll.decButton.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.memberFrame.verticalScroll.decButton.guiId, self.mouseWheelDown)
        self.accept('socailPanelWheelUp', self.mouseWheelUp)
        self.accept('socailPanelWheelDown', self.mouseWheelDown)

    def hide(self):
        self.baseFrame.hide()
        self.ignoreAll()

    def destroy(self):
        for member in self.members:
            member.destroy()

        self.baseFrame.destroy()
        del self.members
        self.ignoreAll()

    def setPos(self, x, y, z):
        self.baseFrame.setPos(x, y, z)

    def setup(self):
        charGui = loader.loadModel('models/gui/char_gui')
        knob = (charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over'))
        self.memberFrame = DirectScrolledFrame(parent=self.baseFrame, relief=None, state=DGG.NORMAL, manageScrollBars=0, autoHideScrollBars=1, frameSize=(0, self.width, self.bottom, self.height), canvasSize=(0, self.width - 0.05, self.bottom + 0.025, self.height - 0.025), verticalScroll_relief=None, verticalScroll_frameSize=(0, PiratesGuiGlobals.ScrollbarSize, self.bottom, self.height), verticalScroll_image=charGui.find('**/chargui_slider_small'), verticalScroll_image_scale=(self.height - self.bottom + 0.05, 1, 0.75), verticalScroll_image_hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      90), verticalScroll_image_pos=(self.width - PiratesGuiGlobals.ScrollbarSize * 0.5 - 0.004, 0, (self.bottom + self.height) * 0.5), verticalScroll_image_color=(0.61,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    0.6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    0.6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    1), verticalScroll_thumb_image=knob, verticalScroll_thumb_relief=None, verticalScroll_thumb_image_scale=0.3, verticalScroll_resizeThumb=0, horizontalScroll_relief=None, sortOrder=5)
        if self.hud:
            self.memberFrame['state'] = DGG.DISABLED
        self.memberFrame.verticalScroll.incButton.destroy()
        self.memberFrame.verticalScroll.decButton.destroy()
        self.memberFrame.horizontalScroll.incButton.destroy()
        self.memberFrame.horizontalScroll.decButton.destroy()
        self.memberFrame.horizontalScroll.hide()
        self.memberFrame.show()
        return

    def addMember(self, avId, playerId, mode, modeInfo=None):
        self.removeMember(avId, playerId, mode)
        texcolor = (0.9, 1, 0.9, 1)
        fcolor = PiratesGuiGlobals.ButtonColor5
        addMe = PirateMemberButton(self, avId, playerId, mode, modeInfo)
        self.members.append(addMe)
        self.arrangeMembers()
        if mode == MODE_GUILD and len(self.members) > 0:
            self.accept('guildMemberOnlineStatus', self.updateGuildMemberOnline)
        return addMe

    def updateGuildMemberOnline(self, avId, onlineStatus):
        for member in self.members:
            if member.avId == avId:
                member.modeInfo[3] = onlineStatus
                member.update()

    def updateGuildMemberRank(self, avId, rank):
        for member in self.members:
            if member.avId == avId:
                member.updateGuildRank(rank)

    def updateAll(self):
        for index in range(len(self.members)):
            self.members[index].update()

    def removeMember(self, avId, playerId, mode):
        removeIndex = None
        for index in range(len(self.members)):
            if self.members[index].avId == avId and mode == MODE_FRIEND_AVATAR:
                removeIndex = index
            elif mode == MODE_FRIEND_PLAYER:
                if self.members[index].playerId == playerId:
                    removeIndex = index
            elif self.members[index].avId == avId and mode == self.members[index].mode:
                removeIndex = index

        if removeIndex != None:
            self.members[removeIndex].destroy()
            del self.members[removeIndex]
            self.removeMember(avId, playerId, mode)
        self.arrangeMembers()
        if mode == MODE_GUILD and len(self.members) == 0:
            self.ignore('guildMemberOnlineStatus')
        return

    def arrangeMembers(self):
        numMembers = len(self.members)
        if numMembers == 0:
            return
        self.members.sort()
        self.memberFrame['canvasSize'] = (
         0, 0.0, 0, numMembers * self.memberHeight)
        self.placement = self.memberHeight * numMembers
        for index in range(numMembers):
            self.placement -= self.memberHeight
            self.members[index].setPos(0.02, 0, self.placement)

    def clearMembers(self):
        while len(self.members) > 0:
            self.members[0].destroy()
            del self.members[0]
# okay decompiling .\pirates\piratesgui\PirateMemberList.pyc
