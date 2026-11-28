import random
import time

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from otp.avatar.DistributedPlayerAI import DistributedPlayerAI
from otp.otpbase import OTPGlobals


class FriendManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendManagerAI')

    SecretChars = 'abcdefghijkmnpqrstuvwxyz23456789'
    SecretLifetime = 60 * 60 * 48
    MaxSecrets = 20

    # Request states:
    PendingInvitee = 0
    Considering = 1

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.nextContext = 0
        self.requests = {}
        self.secrets = {}

    def delete(self):
        self.requests = {}
        self.secrets = {}
        DistributedObjectAI.delete(self)

    def getAvatar(self, avId):
        av = self.air.doId2do.get(avId)
        if not isinstance(av, DistributedPlayerAI):
            return None

        return av

    def newContext(self):
        self.nextContext = (self.nextContext + 1) & 0x7FFFFFFF
        return self.nextContext

    # Friend invitations:

    def friendQuery(self, inviteeId):
        inviterId = self.air.getAvatarIdFromSender()
        inviter = self.getAvatar(inviterId)
        if not inviter:
            self.air.writeServerEvent('suspicious', avId=inviterId,
                message='FriendManagerAI.friendQuery: unknown inviter')
            return

        invitee = self.getAvatar(inviteeId)
        if not invitee:
            # They're not on this district, so they can't be asked.
            self.d_friendConsidering(inviterId, 0, 0)
            return

        if inviterId == inviteeId:
            self.d_friendConsidering(inviterId, 3, 0)
            return

        if self.__isFriend(inviter, inviteeId):
            self.d_friendConsidering(inviterId, 2, 0)
            return

        if len(invitee.getFriendsList()) >= OTPGlobals.MaxFriends:
            self.d_friendConsidering(inviterId, 13, 0)
            return

        context = self.newContext()
        self.requests[context] = [inviterId, inviteeId, self.PendingInvitee]
        self.d_inviteeFriendQuery(inviteeId, inviterId, inviter.getName(), b'', context)

    def cancelFriendQuery(self, context):
        avId = self.air.getAvatarIdFromSender()
        request = self.requests.get(context)
        if not request or request[0] != avId:
            return

        self.d_inviteeCancelFriendQuery(request[1], context)

    def inviteeFriendConsidering(self, yesNo, context):
        avId = self.air.getAvatarIdFromSender()
        request = self.requests.get(context)
        if not request or request[1] != avId:
            return

        if request[2] != self.PendingInvitee:
            return

        if yesNo == 1:
            request[2] = self.Considering
        else:
            del self.requests[context]

        self.d_friendConsidering(request[0], yesNo, context)

    def inviteeFriendResponse(self, yesNoMaybe, context):
        avId = self.air.getAvatarIdFromSender()
        request = self.requests.get(context)
        if not request or request[1] != avId:
            return

        if request[2] != self.Considering:
            return

        del self.requests[context]
        inviterId, inviteeId = request[0], request[1]
        if yesNoMaybe == 1:
            inviter = self.getAvatar(inviterId)
            invitee = self.getAvatar(inviteeId)
            if not inviter or not invitee:
                yesNoMaybe = 0
            elif len(inviter.getFriendsList()) >= OTPGlobals.MaxFriends or \
                 len(invitee.getFriendsList()) >= OTPGlobals.MaxFriends:
                yesNoMaybe = 3
            else:
                self.makeFriends(inviter, invitee)

        self.d_friendResponse(inviterId, yesNoMaybe, context)

    def inviteeAcknowledgeCancel(self, context):
        avId = self.air.getAvatarIdFromSender()
        request = self.requests.get(context)
        if request and request[1] == avId:
            del self.requests[context]

    def __isFriend(self, av, friendId):
        for entry in av.getFriendsList():
            if entry[0] == friendId:
                return True

        return False

    def makeFriends(self, av, otherAv):
        av.extendFriendsList(otherAv.doId, 0)
        av.d_setFriendsList(av.getFriendsList())
        otherAv.extendFriendsList(av.doId, 0)
        otherAv.d_setFriendsList(otherAv.getFriendsList())
        self.air.writeServerEvent('friendsMade', avId=av.doId, friendId=otherAv.doId)

    # Secrets:

    def __pruneSecrets(self):
        now = time.time()
        for secret, (avId, expires) in list(self.secrets.items()):
            if expires < now:
                del self.secrets[secret]

    def requestSecret(self):
        avId = self.air.getAvatarIdFromSender()
        if not self.getAvatar(avId):
            return

        self.__pruneSecrets()
        count = len([1 for owner, expires in self.secrets.values() if owner == avId])
        if count >= self.MaxSecrets:
            self.d_requestSecretResponse(avId, 0, '')
            return

        while True:
            secret = ''.join([random.choice(self.SecretChars) for i in range(6)])
            if secret not in self.secrets:
                break

        self.secrets[secret] = (avId, time.time() + self.SecretLifetime)
        self.d_requestSecretResponse(avId, 1, '%s %s' % (secret[:3], secret[3:]))

    def submitSecret(self, secret):
        avId = self.air.getAvatarIdFromSender()
        av = self.getAvatar(avId)
        if not av:
            return

        self.__pruneSecrets()
        secret = ''.join(secret.lower().split())
        if secret not in self.secrets:
            self.d_submitSecretResponse(avId, 0, 0)
            return

        friendId = self.secrets[secret][0]
        if friendId == avId:
            self.d_submitSecretResponse(avId, 3, 0)
            return

        friend = self.getAvatar(friendId)
        if not friend:
            # The owner of the secret has to be on this district.
            self.d_submitSecretResponse(avId, 0, 0)
            return

        if len(av.getFriendsList()) >= OTPGlobals.MaxFriends:
            self.d_submitSecretResponse(avId, 2, avId)
            return

        if len(friend.getFriendsList()) >= OTPGlobals.MaxFriends:
            self.d_submitSecretResponse(avId, 2, friendId)
            return

        del self.secrets[secret]
        self.makeFriends(av, friend)
        self.d_submitSecretResponse(avId, 1, friendId)

    # Senders:

    def d_friendConsidering(self, avId, yesNoAlready, context):
        self.sendUpdateToAvatarId(avId, 'friendConsidering', [yesNoAlready, context])

    def d_friendResponse(self, avId, yesNoMaybe, context):
        self.sendUpdateToAvatarId(avId, 'friendResponse', [yesNoMaybe, context])

    def d_inviteeFriendQuery(self, avId, inviterId, inviterName, inviterDna, context):
        self.sendUpdateToAvatarId(avId, 'inviteeFriendQuery', [inviterId, inviterName, inviterDna, context])

    def d_inviteeCancelFriendQuery(self, avId, context):
        self.sendUpdateToAvatarId(avId, 'inviteeCancelFriendQuery', [context])

    def d_requestSecretResponse(self, avId, result, secret):
        self.sendUpdateToAvatarId(avId, 'requestSecretResponse', [result, secret])

    def d_submitSecretResponse(self, avId, result, friendId):
        self.sendUpdateToAvatarId(avId, 'submitSecretResponse', [result, friendId])
