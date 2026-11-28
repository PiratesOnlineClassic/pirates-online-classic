import time

from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import PyDatagram
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from otp.distributed.MsgTypes import *
from otp.otpbase import OTPGlobals
from otp.uberdog.RejectCode import RejectCode


class AvatarFriendsOperationFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarFriendsOperationFSM')

    def __init__(self, mgr, avId):
        FSM.__init__(self, self.__class__.__name__)
        self.mgr = mgr
        self.air = mgr.air
        self.avId = avId

    def enterOff(self):
        self.mgr.operations.discard(self)
        if self.mgr.avatarId2OnlineFsm.get(self.avId) is self:
            del self.mgr.avatarId2OnlineFsm[self.avId]

    def getAvatarClassName(self):
        return self.mgr.getAvatarClassName()


class AvatarOnlineFSM(AvatarFriendsOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarOnlineFSM')

    def enterStart(self, accountId):
        self.accountId = accountId
        self.pendingFriends = set()
        self.deletedFriends = set()
        self.demand('QueryAvatar')

    def enterQueryAvatar(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.avId, self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if self.state != 'QueryAvatar':
            return

        if dclass != self.air.dclassesByName[self.getAvatarClassName()]:
            self.notify.warning('Avatar %d came online, but has no avatar object!' % self.avId)
            self.demand('Off')
            return

        name = fields.get('setName', ('',))[0]
        friendsList = fields.get('setFriendsList', ([],))[0]
        self.mgr.avatarCameOnline(self.avId, self.accountId, name, friendsList)
        self.demand('QueryFriends')

    def enterQueryFriends(self):
        friendIds = self.mgr.getFriendIds(self.avId)
        for friendId in friendIds:
            if friendId in self.mgr.onlineAvatars:
                self.mgr.d_updateAvatarFriend(self.avId, friendId)
                continue

            self.pendingFriends.add(friendId)

        for friendId in list(self.pendingFriends):
            self.air.dbInterface.queryObject(self.air.dbId, friendId,
                lambda dclass, fields, friendId=friendId: self.__handleFriend(friendId, dclass, fields))

        if not self.pendingFriends:
            self.demand('NotifyFriends')

    def __handleFriend(self, friendId, dclass, fields):
        if self.state != 'QueryFriends':
            return

        self.pendingFriends.discard(friendId)
        if dclass == self.air.dclassesByName[self.getAvatarClassName()]:
            self.mgr.avatarId2Name[friendId] = fields.get('setName', ('',))[0]
            self.mgr.d_updateAvatarFriend(self.avId, friendId)
        else:
            self.notify.warning('Friend %d of avatar %d no longer exists.' % (friendId, self.avId))
            self.deletedFriends.add(friendId)

        if not self.pendingFriends:
            self.demand('NotifyFriends')

    def enterNotifyFriends(self):
        if self.deletedFriends:
            # The friend's avatar was deleted, take it off our list:
            self.mgr.pruneFriends(self.avId, self.deletedFriends)

        # Let everybody who has us on their list know that we're here:
        for friendId in self.mgr.getFriendIds(self.avId):
            if friendId not in self.mgr.onlineAvatars:
                continue

            if self.avId in self.mgr.getFriendIds(friendId):
                self.mgr.d_updateAvatarFriend(friendId, self.avId)

        self.demand('Off')


class RemoveOfflineFriendFSM(AvatarFriendsOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('RemoveOfflineFriendFSM')

    def enterStart(self, friendId):
        self.friendId = friendId
        self.demand('QueryAvatar')

    def enterQueryAvatar(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.avId, self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if self.state != 'QueryAvatar':
            return

        if dclass != self.air.dclassesByName[self.getAvatarClassName()]:
            self.demand('Off')
            return

        friendsList = fields.get('setFriendsList', ([],))[0]
        newFriendsList = [entry for entry in friendsList if entry[0] != self.friendId]
        if len(newFriendsList) != len(friendsList):
            self.mgr.d_setFriendsList(self.avId, newFriendsList)

        self.demand('Off')


class AvatarFriendsManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarFriendsManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.onlineAvatars = {}
        self.avatarId2Name = {}
        self.avatarId2Friends = {}
        self.invitations = set()
        self.operations = set()
        self.avatarId2OnlineFsm = {}

    def getAvatarClassName(self):
        return 'DistributedPlayerPirateUD'

    def runOperation(self, fsmType, avId, *args):
        fsm = fsmType(self, avId)
        self.operations.add(fsm)
        fsm.request('Start', *args)

    # Presence:

    def comingOnline(self, avId, accountId):
        # Called by the ClientServicesManager once the avatar has been
        # activated and handed to its owner.
        self.goingOffline(avId)

        fsm = AvatarOnlineFSM(self, avId)
        self.operations.add(fsm)
        self.avatarId2OnlineFsm[avId] = fsm
        fsm.request('Start', accountId)

    def avatarCameOnline(self, avId, accountId, name, friendsList):
        self.onlineAvatars[avId] = accountId
        self.avatarId2Name[avId] = name
        self.avatarId2Friends[avId] = [(entry[0], entry[1]) for entry in friendsList]

        # Should the client disconnect, the Client Agent will tell us:
        self.addOfflinePostRemove(avId, accountId)

    def addOfflinePostRemove(self, avId, accountId):
        datagramCleanup = self.dclass.aiFormatUpdate('avatarOffline', self.doId,
            self.doId, self.air.ourChannel, [avId])

        datagram = PyDatagram()
        datagram.addServerHeader(self.GetAccountConnectionChannel(accountId),
            self.air.ourChannel, CLIENTAGENT_ADD_POST_REMOVE)
        datagram.addBlob(datagramCleanup.getMessage())
        self.air.send(datagram)

    def avatarOffline(self, avId):
        # Sent to us by the Client Agent as a post remove.
        self.goingOffline(avId)

    def goingOffline(self, avId):
        fsm = self.avatarId2OnlineFsm.get(avId)
        if fsm:
            fsm.demand('Off')

        if avId not in self.onlineAvatars:
            return

        del self.onlineAvatars[avId]

        for inviterId, inviteeId in list(self.invitations):
            if inviterId == avId:
                self.invitations.discard((inviterId, inviteeId))
                self.d_retractInvite(inviteeId, avId)
            elif inviteeId == avId:
                self.invitations.discard((inviterId, inviteeId))
                self.d_rejectInvite(inviterId, avId, RejectCode.INVITEE_NOT_ONLINE)

        for friendId in self.getFriendIds(avId):
            if friendId in self.onlineAvatars and avId in self.getFriendIds(friendId):
                self.d_updateAvatarFriend(friendId, avId)

        self.avatarId2Friends.pop(avId, None)

    def avatarDeleted(self, avId, friendsList):
        # Called by the ClientServicesManager once an avatar has been deleted,
        # none of its friends should have it on their list anymore:
        self.goingOffline(avId)
        for friendId in [entry[0] for entry in friendsList]:
            self.removeFriend(friendId, avId)
            if self.isOnline(friendId):
                self.d_removeAvatarFriend(friendId, avId)

        self.avatarId2Name.pop(avId, None)

    def isOnline(self, avId):
        return avId in self.onlineAvatars

    def declareFriend(self, avId, friendId):
        # Teleport queries and responses are sent straight to the friend's
        # avatar object, which the client may not be able to see. Declare
        # the friend's avatar to the client so the Client Agent lets those
        # field updates through.
        dclass = self.air.dclassesByName[self.getAvatarClassName()]
        datagram = PyDatagram()
        datagram.addServerHeader(self.GetPuppetConnectionChannel(avId),
            self.air.ourChannel, CLIENTAGENT_DECLARE_OBJECT)
        datagram.addUint32(friendId)
        datagram.addUint16(dclass.getNumber())
        self.air.send(datagram)

    def undeclareFriend(self, avId, friendId):
        datagram = PyDatagram()
        datagram.addServerHeader(self.GetPuppetConnectionChannel(avId),
            self.air.ourChannel, CLIENTAGENT_UNDECLARE_OBJECT)
        datagram.addUint32(friendId)
        self.air.send(datagram)

    # Friends lists:

    def getFriendIds(self, avId):
        return [entry[0] for entry in self.avatarId2Friends.get(avId, [])]

    def isFriend(self, avId, otherAvId):
        return otherAvId in self.getFriendIds(avId)

    def getFriendInfo(self, avId):
        online = self.isOnline(avId)
        return (self.avatarId2Name.get(avId, ''),
                avId,
                '',
                int(online),
                1,
                0,
                1,
                '',
                '',
                int(time.time()))

    def d_setFriendsList(self, avId, friendsList):
        dclass = self.air.dclassesByName[self.getAvatarClassName()]
        if self.isOnline(avId):
            # The avatar is active on the DBSS; update it there so both the
            # AI and owner hear about it:
            datagram = dclass.aiFormatUpdate('setFriendsList', avId, avId,
                self.air.ourChannel, [friendsList])
            self.air.send(datagram)
        else:
            self.air.dbInterface.updateObject(self.air.dbId, avId, dclass,
                {'setFriendsList': (friendsList,)})

    def addFriend(self, avId, friendId):
        friendsList = self.avatarId2Friends.setdefault(avId, [])
        if friendId not in self.getFriendIds(avId):
            friendsList.append((friendId, 0))

        self.d_setFriendsList(avId, friendsList)

    def pruneFriends(self, avId, friendIds):
        friendsList = [entry for entry in self.avatarId2Friends.get(avId, []) if entry[0] not in friendIds]
        self.avatarId2Friends[avId] = friendsList
        self.d_setFriendsList(avId, friendsList)
        for friendId in friendIds:
            self.air.writeServerEvent('avatarFriendPruned', avId=avId, friendId=friendId)

    def removeFriend(self, avId, friendId):
        if avId not in self.avatarId2Friends:
            self.runOperation(RemoveOfflineFriendFSM, avId, friendId)
            return

        friendsList = [entry for entry in self.avatarId2Friends[avId] if entry[0] != friendId]
        self.avatarId2Friends[avId] = friendsList
        self.d_setFriendsList(avId, friendsList)

    def makeFriends(self, avId, otherAvId):
        self.addFriend(avId, otherAvId)
        self.addFriend(otherAvId, avId)
        self.air.writeServerEvent('avatarFriendAdded', avId=avId, friendId=otherAvId)

        self.d_updateAvatarFriend(avId, otherAvId)
        self.d_updateAvatarFriend(otherAvId, avId)

    def breakFriends(self, avId, otherAvId):
        self.removeFriend(avId, otherAvId)
        self.removeFriend(otherAvId, avId)
        self.air.writeServerEvent('avatarFriendRemoved', avId=avId, friendId=otherAvId)

        self.d_removeAvatarFriend(avId, otherAvId)
        if self.isOnline(avId):
            self.undeclareFriend(avId, otherAvId)

        if self.isOnline(otherAvId):
            self.d_removeAvatarFriend(otherAvId, avId)
            self.undeclareFriend(otherAvId, avId)

    # Client requests:

    def requestInvite(self, otherAvId):
        avId = self.air.getAvatarIdFromSender()
        if not self.isOnline(avId):
            self.notify.warning('requestInvite from avatar %d who is not online!' % avId)
            return

        if avId == otherAvId:
            self.d_rejectInvite(avId, otherAvId, RejectCode.ALREADY_FRIENDS_WITH_SELF)
            return

        if (otherAvId, avId) in self.invitations:
            # They asked us first; this is our acceptance.
            self.invitations.discard((otherAvId, avId))
            if not self.isOnline(otherAvId):
                self.d_rejectInvite(avId, otherAvId, RejectCode.INVITEE_NOT_ONLINE)
                return

            if len(self.getFriendIds(avId)) >= OTPGlobals.MaxFriends:
                self.d_rejectInvite(avId, otherAvId, RejectCode.FRIENDS_LIST_FULL)
                self.d_rejectInvite(otherAvId, avId, RejectCode.OTHER_FRIENDS_LIST_FULL)
                return

            if len(self.getFriendIds(otherAvId)) >= OTPGlobals.MaxFriends:
                self.d_rejectInvite(avId, otherAvId, RejectCode.OTHER_FRIENDS_LIST_FULL)
                self.d_rejectInvite(otherAvId, avId, RejectCode.FRIENDS_LIST_FULL)
                return

            self.makeFriends(avId, otherAvId)
            return

        if self.isFriend(avId, otherAvId):
            self.d_rejectInvite(avId, otherAvId, RejectCode.ALREADY_YOUR_FRIEND)
            return

        if not self.isOnline(otherAvId):
            self.d_rejectInvite(avId, otherAvId, RejectCode.INVITEE_NOT_ONLINE)
            return

        if len(self.getFriendIds(avId)) >= OTPGlobals.MaxFriends:
            self.d_rejectInvite(avId, otherAvId, RejectCode.FRIENDS_LIST_FULL)
            return

        if len(self.getFriendIds(otherAvId)) >= OTPGlobals.MaxFriends:
            self.d_rejectInvite(avId, otherAvId, RejectCode.OTHER_FRIENDS_LIST_FULL)
            return

        if (avId, otherAvId) in self.invitations:
            self.d_rejectInvite(avId, otherAvId, RejectCode.ALREADY_INVITED)
            return

        self.invitations.add((avId, otherAvId))
        self.d_invitationFrom(otherAvId, avId, self.avatarId2Name.get(avId, ''))
        self.d_friendConsidering(avId, otherAvId)

    def requestRemove(self, otherAvId):
        avId = self.air.getAvatarIdFromSender()
        if not self.isOnline(avId):
            self.notify.warning('requestRemove from avatar %d who is not online!' % avId)
            return

        if (otherAvId, avId) in self.invitations:
            # We're declining their invitation.
            self.invitations.discard((otherAvId, avId))
            self.d_rejectInvite(otherAvId, avId, RejectCode.INVITATION_DECLINED)
            return

        if (avId, otherAvId) in self.invitations:
            # We changed our mind about inviting them.
            self.invitations.discard((avId, otherAvId))
            self.d_retractInvite(otherAvId, avId)
            return

        if not self.isFriend(avId, otherAvId):
            self.d_rejectRemove(avId, otherAvId, RejectCode.ALREADY_NOT_YOUR_FRIEND)
            return

        self.breakFriends(avId, otherAvId)

    # Senders:

    def d_invitationFrom(self, avId, inviterId, inviterName):
        self.sendUpdateToAvatarId(avId, 'invitationFrom', [inviterId, inviterName])

    def d_friendConsidering(self, avId, inviteeId):
        self.sendUpdateToAvatarId(avId, 'friendConsidering', [inviteeId])

    def d_retractInvite(self, avId, inviterId):
        if self.isOnline(avId):
            self.sendUpdateToAvatarId(avId, 'retractInvite', [inviterId])

    def d_rejectInvite(self, avId, otherAvId, reason):
        if self.isOnline(avId):
            self.sendUpdateToAvatarId(avId, 'rejectInvite', [otherAvId, reason])

    def d_rejectRemove(self, avId, otherAvId, reason):
        self.sendUpdateToAvatarId(avId, 'rejectRemove', [otherAvId, reason])

    def d_updateAvatarFriend(self, avId, friendId):
        if not self.isOnline(avId):
            return

        if self.isOnline(friendId):
            self.declareFriend(avId, friendId)

        self.sendUpdateToAvatarId(avId, 'updateAvatarFriend', [friendId, self.getFriendInfo(friendId)])

    def d_removeAvatarFriend(self, avId, friendId):
        self.sendUpdateToAvatarId(avId, 'removeAvatarFriend', [friendId])

    def d_updateAvatarName(self, avId, name):
        # Lets the friends of an avatar know they have a new name.
        self.avatarId2Name[avId] = name
        for friendId in self.getFriendIds(avId):
            if self.isOnline(friendId):
                self.sendUpdateToAvatarId(friendId, 'updateAvatarName', [avId, name])
