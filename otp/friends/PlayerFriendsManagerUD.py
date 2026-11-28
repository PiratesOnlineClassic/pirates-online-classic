import json
import random
import time

import semidbm

from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import PyDatagram
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from otp.distributed.MsgTypes import *
from otp.otpbase import OTPGlobals
from otp.chat import ChatFilter
from otp.uberdog.RejectCode import RejectCode


SecretChars = 'abcdefghijkmnpqrstuvwxyz23456789'
SecretLength = 6


class PlayerOnlineFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayerOnlineFSM')

    def __init__(self, mgr, avId):
        FSM.__init__(self, self.__class__.__name__)
        self.mgr = mgr
        self.air = mgr.air
        self.avId = avId

    def enterStart(self, accountId):
        self.accountId = accountId
        self.demand('QueryAvatar')

    def enterQueryAvatar(self):
        self.air.dbInterface.queryObject(self.air.dbId, self.avId, self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if self.state != 'QueryAvatar':
            return

        if dclass != self.air.dclassesByName[self.mgr.getAvatarClassName()]:
            self.notify.warning('Avatar %d came online, but has no avatar object!' % self.avId)
            self.demand('Off')
            return

        avatarName = fields.get('setName', ('',))[0]
        playerName = fields.get('setAccountName', ('',))[0]
        self.mgr.playerCameOnline(self.accountId, self.avId, avatarName, playerName)
        self.demand('Off')

    def enterOff(self):
        if self.mgr.avatarId2OnlineFsm.get(self.avId) is self:
            del self.mgr.avatarId2OnlineFsm[self.avId]


class PlayerFriendsManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayerFriendsManagerUD')

    SecretLifetime = 60 * 60 * 48
    MaxSecrets = 20

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.account2avatar = {}
        self.avatar2account = {}
        self.invitations = set()
        self.avatarId2OnlineFsm = {}
        self.dbm = None

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        # Player friendships belong to the account rather than any one
        # pirate, so we keep them alongside the account bridge:
        filename = config.GetString('player-friends-filename', 'astron/databases/player-friends')
        self.dbm = semidbm.open(filename, 'c')
        self.SecretLifetime = config.GetInt('player-friends-secret-lifetime', self.SecretLifetime)
        self.MaxSecrets = config.GetInt('player-friends-max-secrets', self.MaxSecrets)

    def delete(self):
        if self.dbm is not None:
            self.dbm.close()
            self.dbm = None

        DistributedObjectGlobalUD.delete(self)

    def getAvatarClassName(self):
        return 'DistributedPlayerPirateUD'

    # Storage:

    def __load(self, key):
        key = key.encode()
        if key not in self.dbm:
            return None

        return json.loads(self.dbm[key].decode())

    def __store(self, key, value):
        self.dbm[key.encode()] = json.dumps(value).encode()
        if getattr(self.dbm, 'sync', None):
            self.dbm.sync()

    def __erase(self, key):
        key = key.encode()
        if key in self.dbm:
            del self.dbm[key]
            if getattr(self.dbm, 'sync', None):
                self.dbm.sync()

    def getAccount(self, accountId):
        account = self.__load('account-%d' % accountId)
        if account is None:
            account = {
                'friends': [],
                'secrets': [],
                'avatarId': 0,
                'avatarName': '',
                'playerName': ''
            }

        return account

    def storeAccount(self, accountId, account):
        self.__store('account-%d' % accountId, account)

    def getFriendIds(self, accountId):
        return self.getAccount(accountId)['friends']

    def isFriend(self, accountId, otherAccountId):
        return otherAccountId in self.getFriendIds(accountId)

    # Presence:

    def comingOnline(self, avId, accountId):
        # Called by the ClientServicesManager once the avatar has been
        # activated and handed to its owner.
        self.goingOffline(avId)
        if accountId in self.account2avatar:
            self.goingOffline(self.account2avatar[accountId])

        fsm = PlayerOnlineFSM(self, avId)
        self.avatarId2OnlineFsm[avId] = fsm
        fsm.request('Start', accountId)

    def playerCameOnline(self, accountId, avId, avatarName, playerName):
        self.account2avatar[accountId] = avId
        self.avatar2account[avId] = accountId

        account = self.getAccount(accountId)
        account['avatarId'] = avId
        account['avatarName'] = avatarName
        account['playerName'] = playerName
        self.storeAccount(accountId, account)

        self.addOfflinePostRemove(avId, accountId)

        for friendId in account['friends']:
            self.d_updatePlayerFriend(accountId, friendId)

        for friendId in account['friends']:
            if friendId in self.account2avatar:
                self.d_updatePlayerFriend(friendId, accountId)

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

        accountId = self.avatar2account.pop(avId, None)
        if accountId is None:
            return

        if self.account2avatar.get(accountId) == avId:
            del self.account2avatar[accountId]

        for inviterId, inviteeId in list(self.invitations):
            if inviterId == accountId:
                self.invitations.discard((inviterId, inviteeId))
                self.d_retractInvite(inviteeId, avId)
            elif inviteeId == accountId:
                self.invitations.discard((inviterId, inviteeId))
                self.d_rejectInvite(inviterId, avId, RejectCode.INVITEE_NOT_ONLINE)

        for friendId in self.getFriendIds(accountId):
            if friendId in self.account2avatar:
                self.d_updatePlayerFriend(friendId, accountId)

    def avatarDeleted(self, avId, accountId):
        # Called by the ClientServicesManager once an avatar has been deleted,
        # the player's friends should no longer see it as the last avatar
        # they played:
        self.goingOffline(avId)

        account = self.getAccount(accountId)
        if account['avatarId'] != avId:
            return

        account['avatarId'] = 0
        account['avatarName'] = ''
        self.storeAccount(accountId, account)

    def isOnline(self, accountId):
        return accountId in self.account2avatar

    def getOnlineFriendAvatarIds(self, accountId):
        return [self.account2avatar[friendId] for friendId in self.getFriendIds(accountId) if self.isOnline(friendId)]

    def declareFriend(self, accountId, friendId):
        # Teleport queries and responses are sent straight to the friend's
        # avatar object, which the client may not be able to see. Declare
        # the friend's avatar to the client so the Client Agent lets those
        # field updates through.
        dclass = self.air.dclassesByName[self.getAvatarClassName()]
        datagram = PyDatagram()
        datagram.addServerHeader(self.GetAccountConnectionChannel(accountId),
            self.air.ourChannel, CLIENTAGENT_DECLARE_OBJECT)
        datagram.addUint32(self.account2avatar[friendId])
        datagram.addUint16(dclass.getNumber())
        self.air.send(datagram)

    def undeclareFriend(self, accountId, friendId):
        datagram = PyDatagram()
        datagram.addServerHeader(self.GetAccountConnectionChannel(accountId),
            self.air.ourChannel, CLIENTAGENT_UNDECLARE_OBJECT)
        datagram.addUint32(self.account2avatar[friendId])
        self.air.send(datagram)

    def getFriendInfo(self, accountId):
        account = self.getAccount(accountId)
        online = self.isOnline(accountId)
        if online:
            location = 'Pirates'
        else:
            location = ''

        return (account['avatarName'],
                self.account2avatar.get(accountId, account['avatarId']),
                account['playerName'] or account['avatarName'],
                int(online),
                1,
                1,
                1,
                location,
                '',
                int(time.time()))

    # Friendships:

    def makeFriends(self, accountId, otherAccountId):
        for first, second in ((accountId, otherAccountId), (otherAccountId, accountId)):
            account = self.getAccount(first)
            if second not in account['friends']:
                account['friends'].append(second)
                self.storeAccount(first, account)

        self.air.writeServerEvent('playerFriendAdded', accountId=accountId, friendId=otherAccountId)
        self.d_updatePlayerFriend(accountId, otherAccountId)
        self.d_updatePlayerFriend(otherAccountId, accountId)

    def breakFriends(self, accountId, otherAccountId):
        for first, second in ((accountId, otherAccountId), (otherAccountId, accountId)):
            account = self.getAccount(first)
            if second in account['friends']:
                account['friends'].remove(second)
                self.storeAccount(first, account)

        self.air.writeServerEvent('playerFriendRemoved', accountId=accountId, friendId=otherAccountId)
        self.d_removePlayerFriend(accountId, otherAccountId)
        self.d_removePlayerFriend(otherAccountId, accountId)
        if self.isOnline(accountId) and self.isOnline(otherAccountId):
            self.undeclareFriend(accountId, otherAccountId)
            self.undeclareFriend(otherAccountId, accountId)

    def avatarNameChanged(self, avId, accountId, name):
        # Called once an avatar's new name has been written to the database.
        # The account remembers the name of the avatar it last played:
        account = self.getAccount(accountId)
        if account['avatarId'] != avId or account['avatarName'] == name:
            return

        account['avatarName'] = name
        self.storeAccount(accountId, account)
        for friendId in account['friends']:
            self.d_updatePlayerFriend(friendId, accountId)

    def getSenderAccountId(self):
        accountId = self.air.getAccountIdFromSender()
        if accountId not in self.account2avatar:
            self.notify.warning('Request from account %d who has no avatar online!' % accountId)
            return 0

        return accountId

    def requestInvite(self, senderId, otherAvId, secretYesNo):
        accountId = self.getSenderAccountId()
        if not accountId:
            return

        otherAccountId = self.avatar2account.get(otherAvId)
        if otherAccountId is None:
            self.d_rejectInvite(accountId, otherAvId, RejectCode.INVITEE_NOT_ONLINE)
            return

        if otherAccountId == accountId:
            self.d_rejectInvite(accountId, otherAvId, RejectCode.ALREADY_FRIENDS_WITH_SELF)
            return

        avId = self.account2avatar[accountId]
        if (otherAccountId, accountId) in self.invitations:
            # They asked us first; this is our acceptance.
            self.invitations.discard((otherAccountId, accountId))
            if len(self.getFriendIds(accountId)) >= OTPGlobals.MaxPlayerFriends:
                self.d_rejectInvite(accountId, otherAvId, RejectCode.FRIENDS_LIST_FULL)
                self.d_rejectInvite(otherAccountId, avId, RejectCode.OTHER_FRIENDS_LIST_FULL)
                return

            if len(self.getFriendIds(otherAccountId)) >= OTPGlobals.MaxPlayerFriends:
                self.d_rejectInvite(accountId, otherAvId, RejectCode.OTHER_FRIENDS_LIST_FULL)
                self.d_rejectInvite(otherAccountId, avId, RejectCode.FRIENDS_LIST_FULL)
                return

            self.makeFriends(accountId, otherAccountId)
            return

        if self.isFriend(accountId, otherAccountId):
            self.d_rejectInvite(accountId, otherAvId, RejectCode.ALREADY_YOUR_FRIEND)
            return

        if len(self.getFriendIds(accountId)) >= OTPGlobals.MaxPlayerFriends:
            self.d_rejectInvite(accountId, otherAvId, RejectCode.FRIENDS_LIST_FULL)
            return

        if len(self.getFriendIds(otherAccountId)) >= OTPGlobals.MaxPlayerFriends:
            self.d_rejectInvite(accountId, otherAvId, RejectCode.OTHER_FRIENDS_LIST_FULL)
            return

        if (accountId, otherAccountId) in self.invitations:
            self.d_rejectInvite(accountId, otherAvId, RejectCode.ALREADY_INVITED)
            return

        # The invitee answers with our avatar's id, so that's what we give them:
        self.invitations.add((accountId, otherAccountId))
        self.d_invitationFrom(otherAccountId, avId, self.getAccount(accountId)['avatarName'])

    def requestDecline(self, senderId, otherAvId):
        accountId = self.getSenderAccountId()
        if not accountId:
            return

        otherAccountId = self.avatar2account.get(otherAvId)
        if (otherAccountId, accountId) not in self.invitations:
            return

        self.invitations.discard((otherAccountId, accountId))
        self.d_rejectInvite(otherAccountId, self.account2avatar[accountId], RejectCode.INVITATION_DECLINED)

    def requestRemove(self, senderId, otherAccountId):
        accountId = self.getSenderAccountId()
        if not accountId:
            return

        if not self.isFriend(accountId, otherAccountId):
            self.d_rejectRemove(accountId, otherAccountId, RejectCode.ALREADY_NOT_YOUR_FRIEND)
            return

        self.breakFriends(accountId, otherAccountId)

    # Secrets:

    def makeSecret(self):
        while True:
            secret = ''.join([random.choice(SecretChars) for i in range(SecretLength)])
            if self.__load('secret-%s' % secret) is None:
                return secret

    def normalizeSecret(self, secret):
        return ''.join(secret.lower().split())

    def getSecret(self, secret):
        entry = self.__load('secret-%s' % secret)
        if entry is None:
            return None

        if entry['expires'] < time.time():
            self.__erase('secret-%s' % secret)
            return None

        return entry

    def requestUnlimitedSecret(self, senderId):
        accountId = self.getSenderAccountId()
        if not accountId:
            return

        self.__requestSecret(accountId)

    def requestLimitedSecret(self, senderId, parentUsername, parentPassword):
        # There are no parent accounts here; treat this as unlimited.
        accountId = self.getSenderAccountId()
        if not accountId:
            return

        self.__requestSecret(accountId)

    def __requestSecret(self, accountId):
        account = self.getAccount(accountId)
        account['secrets'] = [secret for secret in account['secrets'] if self.getSecret(secret)]
        if len(account['secrets']) >= self.MaxSecrets:
            self.storeAccount(accountId, account)
            self.d_rejectSecret(accountId, 'too many secrets')
            return

        secret = self.makeSecret()
        self.__store('secret-%s' % secret, {'accountId': accountId,
                                            'expires': int(time.time()) + self.SecretLifetime})
        account['secrets'].append(secret)
        self.storeAccount(accountId, account)

        self.air.writeServerEvent('playerFriendSecretCreated', accountId=accountId)
        self.d_secretResponse(accountId, '%s %s' % (secret[:3], secret[3:]))

    def requestUseUnlimitedSecret(self, senderId, secret):
        accountId = self.getSenderAccountId()
        if not accountId:
            return

        self.__useSecret(accountId, secret)

    def requestUseLimitedSecret(self, senderId, secret, parentUsername, parentPassword):
        accountId = self.getSenderAccountId()
        if not accountId:
            return

        if not secret:
            # The client is only checking the parent password.
            return

        self.__useSecret(accountId, secret)

    def __useSecret(self, accountId, secret):
        secret = self.normalizeSecret(secret)
        entry = self.getSecret(secret)
        if entry is None:
            self.d_rejectUseSecret(accountId, 'unknown secret')
            return

        otherAccountId = entry['accountId']
        if otherAccountId == accountId:
            self.d_rejectUseSecret(accountId, 'own secret')
            return

        if self.isFriend(accountId, otherAccountId):
            self.d_rejectUseSecret(accountId, 'already friends')
            return

        if len(self.getFriendIds(accountId)) >= OTPGlobals.MaxPlayerFriends or \
           len(self.getFriendIds(otherAccountId)) >= OTPGlobals.MaxPlayerFriends:
            self.d_rejectUseSecret(accountId, 'friends list full')
            return

        # Secrets are good for one use only:
        self.__erase('secret-%s' % secret)
        otherAccount = self.getAccount(otherAccountId)
        if secret in otherAccount['secrets']:
            otherAccount['secrets'].remove(secret)
            self.storeAccount(otherAccountId, otherAccount)

        self.makeFriends(accountId, otherAccountId)

    # Whispers:

    def __getWhisperTarget(self, playerId):
        accountId = self.getSenderAccountId()
        if not accountId:
            return 0

        if not self.isFriend(accountId, playerId) or not self.isOnline(playerId):
            return 0

        return accountId

    def whisperTo(self, senderId, playerId, message):
        accountId = self.__getWhisperTarget(playerId)
        message = ChatFilter.cleanMessage(message)
        if accountId and message:
            self.sendUpdateToAccountId(playerId, 'whisperFrom', [accountId, message])

    def whisperWLTo(self, senderId, playerId, message):
        accountId = self.__getWhisperTarget(playerId)
        message = ChatFilter.cleanMessage(message)
        if accountId and message:
            message = ChatFilter.filterWhiteList(message)
            self.sendUpdateToAccountId(playerId, 'whisperWLFrom', [accountId, message])

    def __whisperSpeedChat(self, playerId, fieldName, msgIndex):
        # SpeedChat whispers arrive on the recipient's avatar.
        accountId = self.__getWhisperTarget(playerId)
        if not accountId or msgIndex > 0xFFFF:
            return

        avId = self.account2avatar[accountId]
        recipientId = self.account2avatar[playerId]
        dclass = self.air.dclassesByName[self.getAvatarClassName()]
        datagram = dclass.aiFormatUpdate(fieldName, recipientId,
            self.GetPuppetConnectionChannel(recipientId), self.air.ourChannel, [avId, msgIndex])
        self.air.send(datagram)

    def whisperSCTo(self, senderId, playerId, msgIndex):
        self.__whisperSpeedChat(playerId, 'setWhisperSCFrom', msgIndex)

    def whisperSCCustomTo(self, senderId, playerId, msgIndex):
        self.__whisperSpeedChat(playerId, 'setWhisperSCCustomFrom', msgIndex)

    def whisperSCEmoteTo(self, senderId, playerId, msgIndex):
        self.__whisperSpeedChat(playerId, 'setWhisperSCEmoteFrom', msgIndex)

    # Senders:

    def d_invitationFrom(self, accountId, avId, avatarName):
        self.sendUpdateToAccountId(accountId, 'invitationFrom', [avId, avatarName])

    def d_retractInvite(self, accountId, avId):
        if self.isOnline(accountId):
            self.sendUpdateToAccountId(accountId, 'retractInvite', [avId])

    def d_rejectInvite(self, accountId, otherId, reason):
        if self.isOnline(accountId):
            self.sendUpdateToAccountId(accountId, 'rejectInvite', [otherId, reason])

    def d_rejectRemove(self, accountId, otherAccountId, reason):
        self.sendUpdateToAccountId(accountId, 'rejectRemove', [otherAccountId, reason])

    def d_secretResponse(self, accountId, secret):
        self.sendUpdateToAccountId(accountId, 'secretResponse', [secret])

    def d_rejectSecret(self, accountId, reason):
        self.sendUpdateToAccountId(accountId, 'rejectSecret', [reason])

    def d_rejectUseSecret(self, accountId, reason):
        self.sendUpdateToAccountId(accountId, 'rejectUseSecret', [reason])

    def d_updatePlayerFriend(self, accountId, friendId):
        if not self.isOnline(accountId):
            return

        if self.isOnline(friendId):
            self.declareFriend(accountId, friendId)

        self.sendUpdateToAccountId(accountId, 'updatePlayerFriend', [friendId, self.getFriendInfo(friendId)])

    def d_removePlayerFriend(self, accountId, friendId):
        if self.isOnline(accountId):
            self.sendUpdateToAccountId(accountId, 'removePlayerFriend', [friendId])
