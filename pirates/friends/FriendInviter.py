# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.friends.FriendInviter
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.gui.DirectGui import *
from direct.task.Task import Task
from otp.otpbase import OTPGlobals, OTPLocalizer
from otp.uberdog.RejectCode import RejectCode
from pandac.PandaModules import *
from pirates.battle.DistributedBattleNPC import DistributedBattleNPC
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesgui.CheckBox import CheckBox
from pirates.piratesgui.RequestButton import RequestButton


class FriendInviterButton(RequestButton):
    __module__ = __name__

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(FriendInviterButton)


class FriendInviter(GuiPanel.GuiPanel):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendInviter')

    def __init__(self, avId, avName, isPlayerInvite, quickYesNo=True):
        GuiPanel.GuiPanel.__init__(self, 'Invite Friend', 0.5, 0.5)
        self.initialiseoptions(FriendInviter)
        self.setPos(0.15, 0, 0.25)
        self.avId = avId
        self.avName = avName
        self.avDisableName = 'disable-%s' % avId
        self.isPlayerInvite = isPlayerInvite
        self.skipYesNo = quickYesNo
        self.skipCongrats = False
        self.fsm = ClassicFSM.ClassicFSM('FriendInviter', [
         State.State('off', self.enterOff, self.exitOff),
         State.State('getNewFriend', self.enterGetNewFriend, self.exitGetNewFriend),
         State.State('begin', self.enterBegin, self.exitBegin),
         State.State('tooMany', self.enterTooMany, self.exitTooMany),
         State.State('notYet', self.enterNotYet, self.exitNotYet),
         State.State('checkAvailability', self.enterCheckAvailability, self.exitCheckAvailability),
         State.State('notAvailable', self.enterNotAvailable, self.exitNotAvailable),
         State.State('notOpen', self.enterNotOpen, self.exitNotOpen),
         State.State('notAcceptingFriends', self.enterNotAcceptingFriends, self.exitNotAcceptingFriends),
         State.State('wentAway', self.enterWentAway, self.exitWentAway),
         State.State('alreadyFriends', self.enterAlreadyFriends, self.exitAlreadyFriends),
         State.State('alreadyInvited', self.enterAlreadyInvited, self.exitAlreadyInvited),
         State.State('askingNPC', self.enterAskingNPC, self.exitAskingNPC),
         State.State('endFriendship', self.enterEndFriendship, self.exitEndFriendship),
         State.State('friendsNoMore', self.enterFriendsNoMore, self.exitFriendsNoMore),
         State.State('self', self.enterSelf, self.exitSelf),
         State.State('ignored', self.enterIgnored, self.exitIgnored),
         State.State('asking', self.enterAsking, self.exitAsking),
         State.State('yes', self.enterYes, self.exitYes),
         State.State('no', self.enterNo, self.exitNo),
         State.State('otherTooMany', self.enterOtherTooMany, self.exitOtherTooMany),
         State.State('maybe', self.enterMaybe, self.exitMaybe),
         State.State('down', self.enterDown, self.exitDown),
         State.State('cancel', self.enterCancel, self.exitCancel)], 'off', 'off')
        self.message = DirectLabel(parent=self, relief=None, text='', text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.25,
                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                    0.35), textMayChange=1)
        self.context = None
        self.bOk = FriendInviterButton(text=OTPLocalizer.FriendInviterOK, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.2, 0, 0.05)
        self.bOk.hide()
        self.bCancel = FriendInviterButton(text=OTPLocalizer.FriendInviterCancel, command=self.__handleCancel)
        self.bCancel.reparentTo(self)
        self.bCancel.setPos(0.2, 0, 0.05)
        self.bCancel.hide()
        self.bStop = FriendInviterButton(text='Stop', command=self.__handleStop)
        self.bStop.reparentTo(self)
        self.bStop.setPos(0.2, 0, 0.15)
        self.bStop.hide()
        self.bYes = FriendInviterButton(text=OTPLocalizer.FriendInviterYes, command=self.__handleYes)
        self.bYes.reparentTo(self)
        self.bYes.setPos(0.1, 0, 0.05)
        self.bYes.hide()
        self.bNo = FriendInviterButton(text=OTPLocalizer.FriendInviterNo, command=self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.05)
        self.bNo.hide()
        self.fsm.enterInitialState()
        if self.avId == None:
            self.fsm.request('getNewFriend')
        else:
            self.fsm.request('begin')
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.fsm.request('cancel')
        del self.fsm
        GuiPanel.GuiPanel.destroy(self)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterGetNewFriend(self):
        self.message['text'] = OTPLocalizer.FriendInviterClickToon
        self.bCancel.show()
        self.accept('clickedNametag', self.__handleClickedNametag)

    def exitGetNewFriend(self):
        self.bCancel.hide()
        self.ignore('clickedNametag')

    def __handleClickedNametag(self, avatar):
        self.avId = avatar.doId
        self.avName = avatar.getName()
        self.avDisableName = avatar.uniqueName('disable')
        self.fsm.request('begin')

    def enterBegin(self):
        myId = base.localAvatar.doId
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        if self.avId == myId:
            self.fsm.request('self')
        else:
            if self.isPlayerInvite:
                print('isPlayerFriend: %s' % base.cr.playerFriendsManager.isPlayerFriend(self.avId))
                print('isavatarofplayerfriend: %s' % base.cr.playerFriendsManager.findPlayerIdFromAvId(self.avId))
                if base.cr.playerFriendsManager.isAvatarOwnerPlayerFriend(self.avId):
                    self.fsm.request('alreadyFriends')
                elif len(base.cr.playerFriendsManager.playerFriendsList) >= OTPGlobals.MaxFriends:
                    self.fsm.request('tooMany')
                elif self.skipYesNo == True:
                    self.fsm.request('checkAvailability')
                else:
                    self.fsm.request('notYet')
            else:
                if base.cr.avatarFriendsManager.isFriend(self.avId):
                    self.fsm.request('alreadyFriends')
                else:
                    tooMany = len(base.cr.avatarFriendsManager.avatarFriendsList) >= OTPGlobals.MaxFriends
                    if tooMany:
                        self.fsm.request('tooMany')
                    else:
                        if self.skipYesNo == True:
                            self.fsm.request('checkAvailability')
                        else:
                            self.fsm.request('notYet')

    def exitBegin(self):
        self.ignore(self.avDisableName)

    def enterTooMany(self):
        self.message['text'] = PLocalizer.FriendInviterTooMany % (self.avName,)
        self['text_pos'] = (0.0, 0.2)
        self.bCancel.show()

    def exitTooMany(self):
        self.bCancel.hide()

    def enterNotYet(self):
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        self.message['text'] = OTPLocalizer.FriendInviterNotYet % self.avName
        self.bYes.show()
        self.bNo.show()

    def exitNotYet(self):
        self.ignore(self.avDisableName)
        self.bYes.hide()
        self.bNo.hide()

    def enterCheckAvailability(self):
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        handle = base.cr.identifyAvatar(self.avId)
        if not handle:
            self.fsm.request('wentAway')
            return
        if isinstance(handle, DistributedBattleNPC):
            self.fsm.request('askingNPC')
            return
        if self.isPlayerInvite:
            base.cr.playerFriendsManager.sendRequestInvite(self.avId)
        else:
            base.cr.avatarFriendsManager.sendRequestInvite(self.avId)
        self.message['text'] = OTPLocalizer.FriendInviterCheckAvailability % self.avName
        self.accept(OTPGlobals.AvatarFriendConsideringEvent, self.__friendConsidering)
        self.accept(OTPGlobals.AvatarFriendAddEvent, self.__friendAdded)
        self.accept(OTPGlobals.AvatarFriendRejectInviteEvent, self.__friendRejectInvite)
        self.accept(OTPGlobals.PlayerFriendUpdateEvent, self.__friendAdded)
        self.accept(OTPGlobals.PlayerFriendRejectInviteEvent, self.__friendRejectInvite)
        self.bCancel.show()

    def __friendAdded(self, avId, info):
        if self.isPlayerInvite:
            if self.avId == info.avatarId:
                self.info = info
                self.fsm.request('yes')
        else:
            if self.avId == avId:
                self.fsm.request('yes')

    def exitCheckAvailability(self):
        self.ignore(self.avDisableName)
        self.ignore('friendConsidering')
        self.ignore('friendResponse')
        self.ignore(OTPGlobals.AvatarFriendAddEvent)
        self.ignore(OTPGlobals.AvatarFriendRejectInviteEvent)
        self.ignore(OTPGlobals.PlayerFriendAddEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectInviteEvent)
        self.bCancel.hide()

    def enterNotAvailable(self):
        self.message['text'] = OTPLocalizer.FriendInviterNotAvailable % self.avName
        self.context = None
        self.bOk.show()
        return

    def exitNotAvailable(self):
        self.bOk.hide()

    def enterNotOpen(self):
        self.message['text'] = OTPLocalizer.FriendInviterNotOpen % self.avName
        self.context = None
        self.bOk.show()
        return

    def exitNotOpen(self):
        self.bOk.hide()

    def enterNotAcceptingFriends(self):
        self.message['text'] = OTPLocalizer.FriendInviterFriendSaidNoNewFriends % self.avName
        self.context = None
        self.bOk.show()
        return

    def exitNotAcceptingFriends(self):
        self.bOk.hide()

    def enterWentAway(self):
        self.message['text'] = OTPLocalizer.FriendInviterWentAway % self.avName
        if self.context != None:
            self.context = None
        self.bOk.show()
        return

    def exitWentAway(self):
        self.bOk.hide()

    def enterAlreadyFriends(self):
        self.message['text'] = OTPLocalizer.FriendInviterAlready % self.avName
        self['text_pos'] = (0.0, 0.2)
        self.context = None
        self.bStop.show()
        self.bCancel.show()
        return

    def exitAlreadyFriends(self):
        self.message['text'] = ''
        self['text_pos'] = (0.0, 0.13)
        self.bStop.hide()
        self.bCancel.hide()

    def enterAlreadyInvited(self):
        self.message['text'] = OTPLocalizer.FriendInviterAlreadyInvited % self.avName
        self['text_pos'] = (0.0, 0.2)
        self.context = None
        self.bStop.show()
        self.bCancel.show()
        return

    def exitAlreadyInvited(self):
        self.message['text'] = ''
        self['text_pos'] = (0.0, 0.13)
        self.bStop.hide()
        self.bCancel.hide()

    def enterAskingNPC(self):
        self.message['text'] = PLocalizer.FriendInviterAskingNPC % self.avName
        taskMgr.doMethodLater(2.0, self.npcReplies, 'npcFriendship')
        self.bCancel.show()

    def exitAskingNPC(self):
        taskMgr.remove('npcFriendship')
        self.bCancel.hide()

    def npcReplies(self, task):
        self.fsm.request('no')
        return Task.done

    def enterEndFriendship(self):
        self.message['text'] = OTPLocalizer.FriendInviterEndFriendship % self.avName
        self.context = None
        self.bYes.show()
        self.bNo.show()
        return

    def exitEndFriendship(self):
        self.bYes.hide()
        self.bNo.hide()

    def enterFriendsNoMore(self):
        print('enterFriendsNoMore %s %s' % (self.isPlayerInvite, self.avId))
        if self.isPlayerInvite:
            pId = base.cr.playerFriendsManager.findPlayerIdFromAvId(self.avId)
            if pId:
                base.cr.playerFriendsManager.sendRequestRemove(pId)
        else:
            base.cr.avatarFriendsManager.sendRequestRemove(self.avId)
        self.message['text'] = OTPLocalizer.FriendInviterFriendsNoMore % self.avName
        self.bOk.show()
        if not self.isPlayerInvite and not base.cr.identifyAvatar(self.avId):
            messenger.send(self.avDisableName)

    def exitFriendsNoMore(self):
        self.bOk.hide()

    def enterSelf(self):
        self.message['text'] = OTPLocalizer.FriendInviterSelf
        self.context = None
        self.bOk.show()
        return

    def exitSelf(self):
        self.bOk.hide()

    def enterIgnored(self):
        self.message['text'] = OTPLocalizer.FriendInviterIgnored % self.avName
        self.context = None
        self.bOk.show()
        return

    def exitIgnored(self):
        self.bOk.hide()

    def enterAsking(self):
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        self.message['text'] = OTPLocalizer.FriendInviterAsking % self.avName
        self.accept(OTPGlobals.AvatarFriendConsideringEvent, self.__friendConsidering)
        self.accept(OTPGlobals.AvatarFriendAddEvent, self.__friendAdded)
        self.accept(OTPGlobals.AvatarFriendRejectInviteEvent, self.__friendRejectInvite)
        self.accept(OTPGlobals.PlayerFriendUpdateEvent, self.__friendAdded)
        self.accept(OTPGlobals.PlayerFriendRejectInviteEvent, self.__friendRejectInvite)
        self.bCancel.show()

    def exitAsking(self):
        self.ignore(self.avDisableName)
        self.ignore(OTPGlobals.AvatarFriendConsideringEvent)
        self.ignore(OTPGlobals.AvatarFriendAddEvent)
        self.ignore(OTPGlobals.AvatarFriendRejectInviteEvent)
        self.ignore(OTPGlobals.PlayerFriendAddEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectInviteEvent)
        self.bCancel.hide()

    def enterYes(self):
        if self.skipCongrats:
            self.destroy()
        else:
            if self.isPlayerInvite:
                self.message['text'] = OTPLocalizer.FriendInviterPlayerFriendSaidYes % (self.avName, self.info.playerName)
            else:
                self.message['text'] = OTPLocalizer.FriendInviterFriendSaidYes % self.avName
            self.context = None
            self.bOk.show()
        return

    def exitYes(self):
        self.bOk.hide()

    def enterNo(self):
        self.message['text'] = OTPLocalizer.FriendInviterFriendSaidNo % self.avName
        self.context = None
        self.bOk.show()
        return

    def exitNo(self):
        self.bOk.hide()

    def enterOtherTooMany(self):
        self.message['text'] = OTPLocalizer.FriendInviterOtherTooMany % self.avName
        self.context = None
        self.bOk.show()
        return

    def exitOtherTooMany(self):
        self.bOk.hide()

    def enterMaybe(self):
        self.message['text'] = OTPLocalizer.FriendInviterMaybe % self.avName
        self.context = None
        self.bOk.show()
        return

    def exitMaybe(self):
        self.bOk.hide()

    def enterDown(self):
        self.message['text'] = OTPLocalizer.FriendInviterDown
        self.context = None
        self.bOk.show()
        return

    def exitDown(self):
        self.bOk.hide()

    def enterCancel(self):
        if self.context != None:
            self.context = None
        self.fsm.request('off')
        return

    def exitCancel(self):
        pass

    def __handleOk(self):
        self.destroy()

    def __handleCancel(self):
        self.destroy()

    def __handleStop(self):
        self.fsm.request('endFriendship')

    def __handleYes(self):
        if self.fsm.getCurrentState().getName() == 'notYet':
            self.fsm.request('checkAvailability')
        else:
            if self.fsm.getCurrentState().getName() == 'endFriendship':
                self.fsm.request('friendsNoMore')
            else:
                self.destroy()

    def __handleNo(self):
        self.destroy()

    def __handleList(self):
        messenger.send('openFriendsList')

    def __friendConsidering(self, yesNoAlready, context):
        if yesNoAlready == 1:
            self.context = context
            self.fsm.request('asking')
        else:
            if yesNoAlready == 0:
                self.fsm.request('notAvailable')
            else:
                if yesNoAlready == 2:
                    self.fsm.request('alreadyFriends')
                else:
                    if yesNoAlready == 3:
                        self.fsm.request('self')
                    else:
                        if yesNoAlready == 4:
                            self.fsm.request('ignored')
                        else:
                            if yesNoAlready == 6:
                                self.fsm.request('notAcceptingFriends')
                            else:
                                if yesNoAlready == 10:
                                    self.fsm.request('no')
                                else:
                                    if yesNoAlready == 13:
                                        self.fsm.request('otherTooMany')
                                    else:
                                        self.notify.warning('Got unexpected response to friendConsidering: %s' % yesNoAlready)
                                        self.fsm.request('maybe')

    def __friendRejectInvite(self, avId, reason):
        if reason == RejectCode.NO_FRIENDS_LIST:
            pass
        else:
            if reason == RejectCode.FRIENDS_LIST_NOT_HANDY:
                pass
            else:
                if reason == RejectCode.INVITEE_NOT_ONLINE:
                    self.fsm.request('notAvailable')
                else:
                    if reason == RejectCode.ALREADY_INVITED:
                        self.fsm.request('alreadyInvited')
                    else:
                        if reason == RejectCode.ALREADY_YOUR_FRIEND:
                            self.fsm.request('alreadyFriends')
                        else:
                            if reason == RejectCode.FRIENDS_LIST_FULL:
                                self.fsm.request('tooMany')
                            else:
                                if reason == RejectCode.OTHER_FRIENDS_LIST_FULL:
                                    self.fsm.request('otherTooMany')
                                else:
                                    if reason == RejectCode.INVITATION_DECLINED:
                                        self.fsm.request('no')
                                    else:
                                        if reason == RejectCode.MAY_NOT_OPEN_INVITE:
                                            self.notify.warning('May Not Open Invite, switchboard confused %s.' % avId)
                                            self.fsm.request('notOpen')
                                        else:
                                            self.notify.warning('friendRejectInvite: %s unknown reason: %s.' % (avId, reason))

    def __friendResponse(self, yesNoMaybe, context):
        if self.context != context:
            self.notify.warning('Unexpected change of context from %s to %s.' % (self.context, context))
            self.context = context
        if yesNoMaybe == 1:
            self.fsm.request('yes')
        else:
            if yesNoMaybe == 0:
                self.fsm.request('no')
            else:
                if yesNoMaybe == 3:
                    self.fsm.request('otherTooMany')
                else:
                    self.notify.warning('Got unexpected response to friendResponse: %s' % yesNoMaybe)
                    self.fsm.request('maybe')

    def __handleDisableAvatar(self):
        self.fsm.request('wentAway')
# okay decompiling .\pirates\friends\FriendInviter.pyc
